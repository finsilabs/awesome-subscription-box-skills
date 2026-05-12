# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31.0"]
# ///
"""POST local files to Shopify staged-upload targets (multipart/form-data)."""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent


def upload_one(target: dict) -> tuple[str, str, str]:
    local = ROOT / target["local"]
    fields = {p["name"]: p["value"] for p in target["parameters"]}
    with local.open("rb") as fh:
        files = {"file": (target["filename"], fh, "image/png")}
        resp = requests.post(target["url"], data=fields, files=files, timeout=60)
    if resp.status_code != 201:
        return ("error", target["local"], f"HTTP {resp.status_code}: {resp.text[:200]}")
    return ("ok", target["local"], target["resourceUrl"])


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: upload_staged.py <staged_targets.json>", file=sys.stderr)
        return 1
    targets = json.loads(Path(sys.argv[1]).read_text())
    results: list[dict] = []
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(upload_one, t): t for t in targets}
        for fut in as_completed(futs):
            status, local, detail = fut.result()
            if status != "ok":
                print(f"FAILED {local}: {detail}", file=sys.stderr)
                failures.append(local)
            else:
                print(f"OK     {local}", flush=True)
                results.append({"local": local, "resourceUrl": detail})
    out_path = ROOT / "scripts" / "uploaded_resources.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {out_path.relative_to(ROOT)} with {len(results)} entries.")
    return 2 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
