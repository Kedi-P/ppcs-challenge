-- 0001_init.sql — PPCS baseline schema (idempotent, schema-parameterised)
--
-- Applied by ci/run_migrations.py, which substitutes :schema for the target
-- Postgres schema (a team schema in production, or the ci-* clone in CI).
--
-- These are the tables the PPCS backlog depends on:
--   app_identity_evidence  — identity-proof row for /platform/lakebase-check
--   ppcs_rule_config       — rule thresholds (PPCS-055)
--   ppcs_price_history     — historical SKU prices (PPCS-056)

CREATE SCHEMA IF NOT EXISTS :schema;

CREATE TABLE IF NOT EXISTS :schema.app_identity_evidence (
    id          text PRIMARY KEY,
    checked_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS :schema.ppcs_rule_config (
    rule_id      text NOT NULL,
    param_key    text NOT NULL,
    param_value  numeric NOT NULL,
    updated_at   timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (rule_id, param_key)
);

CREATE TABLE IF NOT EXISTS :schema.ppcs_price_history (
    sku          text NOT NULL,
    observed_on  date NOT NULL,
    price        numeric NOT NULL,
    PRIMARY KEY (sku, observed_on)
);
