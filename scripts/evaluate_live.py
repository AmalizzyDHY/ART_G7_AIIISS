"""Run the g07 examples against a running API in local mode and append the results
to docs/model-evaluation.md. Manual use only, never in CI."""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()
api = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
fixtures = Path("tests/fixtures")
cases = json.loads((fixtures / "g07.json").read_text()) + json.loads(
    (fixtures / "g07_extra.json").read_text()
)

rows = []
for case in cases:
    started = time.perf_counter()
    try:
        response = httpx.post(
            f"{api}/api/analyze",
            json={"subject": case["subject"], "text": case["text"]},
            timeout=120,
            trust_env=False,
        )
        status, body = response.status_code, response.json()
    except (httpx.HTTPError, ValueError) as exc:
        status, body = "error", {"detail": type(exc).__name__}
    latency = round((time.perf_counter() - started) * 1000)
    analysis = body.get("analysis", {}) if status == 200 else {}
    rows.append(
        [
            case["subject"],
            case["expected_category"],
            analysis.get("category", "-"),
            case["expected_priority"],
            analysis.get("priority", "-"),
            status == 200,
            analysis.get("category") == case["expected_category"],
            latency,
            "" if status == 200 else f"{status} {str(body.get('detail'))[:60]}",
        ]
    )

valid = sum(row[5] for row in rows)
agree = sum(row[6] for row in rows)
lines = [
    f"\n## Run {datetime.now().astimezone():%Y-%m-%d %H:%M} · model {os.getenv('LLM_MODEL', '?')}\n",
    "| Case | Expected | Got | Expected priority | Got priority | Valid | Agrees | Latency (ms) | Error |",
    "|---|---|---|---|---|---|---|---|---|",
]
lines += ["| " + " | ".join(str(value) for value in row) + " |" for row in rows]
lines.append(f"\nValid: {valid}/{len(rows)}. Category agreement: {agree}/{len(rows)}.\n")
report = Path("docs/model-evaluation.md")
report.parent.mkdir(exist_ok=True)
with report.open("a", encoding="utf-8") as handle:
    handle.write("\n".join(lines))
print("\n".join(lines))
