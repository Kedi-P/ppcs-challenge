"""Drive burst load at a team's PPCS app to make Lakebase autoscaling visible.

Round 3 exercise. Run a burst, watch your team's Lakebase Metrics dashboard
(CU / RAM allocated climbs, connection count saws), then go idle past the
suspend timeout and run --resume-proof to show the first request after
scale-to-zero still succeeds.

Usage (from the service repo root):
    uv run python tools/load_drive.py --app-url https://<team-app> \
        --seconds 60 --concurrency 16
    uv run python tools/load_drive.py --app-url https://<team-app> \
        --resume-proof

Auth: uses `databricks auth token` for the given profile unless --token is set.
Never paste tokens into files or tickets.
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request


def get_token(profile: str) -> str:
    result = subprocess.run(
        ["databricks", "auth", "token", "-p", profile, "-o", "json"],
        text=True,
        stdout=subprocess.PIPE,
        check=True,
        timeout=60,
    )
    return json.loads(result.stdout)["access_token"]


def one_request(url: str, token: str, timeout: float = 30.0) -> tuple[float, int | str]:
    promo = {
        "sku": f"SKU-{random.randint(1, 9999)}",
        "was_price": round(random.uniform(5, 50), 2),
        "now_price": 0.0,
    }
    promo["now_price"] = round(promo["was_price"] * random.uniform(0.5, 0.99), 2)
    request = urllib.request.Request(
        url,
        data=json.dumps(promo).encode(),
        headers={"authorization": f"Bearer {token}", "content-type": "application/json"},
        method="POST",
    )
    start = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response.read()
            return (time.monotonic() - start) * 1000, response.status
    except urllib.error.HTTPError as exc:
        return (time.monotonic() - start) * 1000, exc.code
    except Exception as exc:  # noqa: BLE001 - report, don't crash the worker
        return (time.monotonic() - start) * 1000, type(exc).__name__


def percentile(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return 0.0
    index = min(int(len(sorted_values) * pct), len(sorted_values) - 1)
    return sorted_values[index]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-url", required=True, help="team app base URL")
    parser.add_argument("--endpoint", default="/validate")
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--concurrency", type=int, default=16)
    parser.add_argument("--profile", default="lakemeter")
    parser.add_argument("--token", default=None, help="bearer token (else minted from profile)")
    parser.add_argument(
        "--resume-proof",
        action="store_true",
        help="send ONE request and report its latency (run after idling past suspend timeout)",
    )
    args = parser.parse_args()

    token = args.token or get_token(args.profile)
    url = args.app_url.rstrip("/") + args.endpoint

    if args.resume_proof:
        elapsed_ms, status = one_request(url, token, timeout=120.0)
        ok = status == 200
        print(f"{'PASS' if ok else 'FAIL'} resume proof: status={status} latency={elapsed_ms:.0f}ms")
        print("Capture this with the Metrics dashboard showing the suspend/resume window.")
        return 0 if ok else 1

    latencies: list[float] = []
    outcomes: dict[str | int, int] = {}
    lock = threading.Lock()
    deadline = time.monotonic() + args.seconds

    def worker() -> None:
        while time.monotonic() < deadline:
            elapsed_ms, status = one_request(url, token)
            with lock:
                latencies.append(elapsed_ms)
                outcomes[status] = outcomes.get(status, 0) + 1

    print(f"driving {args.concurrency} workers at {url} for {args.seconds}s ...")
    threads = [threading.Thread(target=worker, daemon=True) for _ in range(args.concurrency)]
    start = time.monotonic()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    wall = time.monotonic() - start

    latencies.sort()
    total = len(latencies)
    errors = sum(count for status, count in outcomes.items() if status != 200)
    print(f"requests={total} wall={wall:.1f}s rps={total / wall:.1f}")
    print(
        f"latency ms: p50={percentile(latencies, 0.50):.0f} "
        f"p95={percentile(latencies, 0.95):.0f} p99={percentile(latencies, 0.99):.0f}"
    )
    print(f"outcomes={outcomes}")
    if errors:
        print(f"WARN {errors} non-200 responses")
    print("Now: screenshot the Metrics dashboard CU/connection curves, idle past the")
    print("suspend timeout (300s), then rerun with --resume-proof.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
