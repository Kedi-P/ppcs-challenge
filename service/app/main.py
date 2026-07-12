"""PPCS API — submit a promo, get a compliance verdict."""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.rules import Promo, discount_pct, is_was_now_compliant

app = FastAPI(title="Promotional Pricing Compliance Service")
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class PromoIn(BaseModel):
    sku: str
    was_price: float
    now_price: float


@app.get("/", include_in_schema=False)
def workbench() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/validate")
def validate(promo: PromoIn) -> dict:
    p = Promo(promo.sku, promo.was_price, promo.now_price)
    return {
        "sku": p.sku,
        "discount_pct": discount_pct(p),
        "was_now_compliant": is_was_now_compliant(p),
    }


def _execute_sql(statement: str) -> dict:
    from databricks.sdk import WorkspaceClient

    warehouse_id = os.environ.get("PPCS_SQL_WAREHOUSE_ID", "71ac669a24f4a7a7")
    client = WorkspaceClient()
    response = client.statement_execution.execute_statement(
        warehouse_id=warehouse_id,
        statement=statement,
        wait_timeout="30s",
    )
    return response.as_dict()


def _workspace_client():
    from databricks.sdk import WorkspaceClient

    return WorkspaceClient()


def _summarise_sql_result(result: dict) -> dict:
    status = result.get("status", {})
    summary = {
        "state": status.get("state"),
        "statement_id": result.get("statement_id"),
    }
    if "error" in status:
        summary["error_code"] = status["error"].get("error_code")
        summary["message"] = status["error"].get("message")
    if "result" in result:
        summary["data_array"] = result["result"].get("data_array")
    return summary


def _safe_execute_sql(statement: str) -> dict:
    try:
        return _summarise_sql_result(_execute_sql(statement))
    except Exception as exc:  # pragma: no cover - diagnostic endpoint only
        return {"state": "EXCEPTION", "message": str(exc)}


@app.get("/platform/uc-check")
def platform_uc_check() -> dict:
    allowed_table = os.environ.get(
        "PPCS_ALLOWED_EVENTS_TABLE",
        "workshop_ppcs.team04.ppcs_validation_events",
    )
    denied_table = os.environ.get(
        "PPCS_DENIED_MARGIN_OBJECT",
        "pricing_prod.margins.current_margin_by_sku",
    )

    return {
        "identity_model": "databricks-app-service-principal",
        "allowed_table": allowed_table,
        "denied_table": denied_table,
        "session": _safe_execute_sql(
            "select current_user(), current_catalog(), current_schema()"
        ),
        "catalogs": _safe_execute_sql("show catalogs"),
        "schemas_in_main": _safe_execute_sql("show schemas in main"),
        "allowed": _safe_execute_sql(
            f"select current_user(), count(*) from {allowed_table}"
        ),
        "denied": _safe_execute_sql(
            f"select sku, margin_pct from {denied_table} limit 10"
        ),
    }


@app.get("/platform/lakebase-check")
def platform_lakebase_check() -> dict:
    import psycopg

    lakebase_target = os.environ.get(
        "PPCS_LAKEBASE_TARGET",
        "projects/ppcs-coda-challenge/branches/production/endpoints/primary",
    )
    lakebase_host = os.environ.get(
        "PPCS_LAKEBASE_HOST",
        "ep-sweet-mud-e4rrnat1.database.australiaeast.azuredatabricks.net",
    )
    team_schema = os.environ.get("PPCS_TEAM_SCHEMA", "team04")

    client = _workspace_client()
    credential = client.api_client.do(
        "POST",
        "/api/2.0/postgres/credentials",
        body={"endpoint": lakebase_target},
    )
    token = credential["token"]

    # The Postgres role is the identity that minted the credential — for an app
    # service principal that's its application-id UUID, which the SDK surfaces
    # as current_user.user_name. DATABRICKS_CLIENT_ID is unset in the app
    # runtime (SP self-auth via apiKeyHelper), so deriving it from the client is
    # the only reliable source.
    db_user = os.environ.get("PPCS_LAKEBASE_USER") or client.current_user.me().user_name

    with psycopg.connect(
        host=lakebase_host,
        dbname="databricks_postgres",
        user=db_user,
        password=token,
        sslmode="require",
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                insert into {team_schema}.app_identity_evidence (id)
                values ('app-dry-run')
                on conflict (id) do update set checked_at = now()
                """
            )
            cur.execute(
                f"""
                select current_user, current_database(), id, checked_at
                from {team_schema}.app_identity_evidence
                where id = 'app-dry-run'
                """
            )
            row = cur.fetchone()

    return {
        "identity_model": "databricks-app-service-principal",
        "lakebase_target": lakebase_target,
        "team_schema": team_schema,
        "current_user": row[0],
        "current_database": row[1],
        "row_id": row[2],
        "checked_at": row[3].isoformat(),
    }
