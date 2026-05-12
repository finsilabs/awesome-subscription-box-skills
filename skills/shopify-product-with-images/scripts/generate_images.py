# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-genai>=0.3.0",
#   "python-dotenv>=1.0.0",
# ]
# ///
"""Generate images with Nano Banana (gemini-2.5-flash-image).

Usage:
    uv run scripts/generate_images.py scripts/prompts/<file>.json

Where the JSON file is a list of jobs:
    [
      {"prompt": "...", "output": "generated/hero.png", "aspect_ratio": "16:9"},
      ...
    ]

aspect_ratio is optional. Supported values: "1:1", "3:4", "4:3", "9:16", "16:9", "21:9", "2:3", "3:2", "5:4", "4:5".
"""

from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
MODEL = "gemini-2.5-flash-image"


def generate_one(client: genai.Client, job: dict, idx: int, total: int) -> tuple[str, str]:
    prompt = job["prompt"]
    output = ROOT / job["output"]
    output.parent.mkdir(parents=True, exist_ok=True)

    config_kwargs = {"response_modalities": ["IMAGE"]}
    if "aspect_ratio" in job:
        config_kwargs["image_config"] = types.ImageConfig(aspect_ratio=job["aspect_ratio"])

    label = f"[{idx}/{total}] {output.relative_to(ROOT)}"
    print(f"{label}: generating...", flush=True)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.data:
            output.write_bytes(part.inline_data.data)
            print(f"{label}: saved ({len(part.inline_data.data) // 1024} KB)", flush=True)
            return ("ok", str(output))

    text_fallback = " ".join(
        p.text for p in response.candidates[0].content.parts if getattr(p, "text", None)
    )
    return ("error", f"No image returned. Model said: {text_fallback[:200]}")


def main() -> int:
    load_dotenv(ROOT / ".env")
    if "GOOGLE_API_KEY" not in os.environ:
        print("ERROR: GOOGLE_API_KEY not found in environment or .env", file=sys.stderr)
        return 1

    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 1

    jobs_path = Path(sys.argv[1])
    if not jobs_path.is_absolute():
        jobs_path = ROOT / jobs_path
    jobs = json.loads(jobs_path.read_text())
    if not isinstance(jobs, list):
        print("ERROR: jobs file must be a JSON array", file=sys.stderr)
        return 1

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(generate_one, client, job, i + 1, len(jobs)): job
            for i, job in enumerate(jobs)
        }
        for fut in as_completed(futures):
            status, detail = fut.result()
            if status != "ok":
                failures.append(detail)
                print(f"FAILED: {detail}", file=sys.stderr)

    if failures:
        print(f"\n{len(failures)} of {len(jobs)} jobs failed", file=sys.stderr)
        return 2
    print(f"\nAll {len(jobs)} images generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
