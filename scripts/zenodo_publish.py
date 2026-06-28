from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZENODO_API = os.environ.get("ZENODO_API", "https://zenodo.org/api")
TOKEN = os.environ.get("ZENODO_ACCESS_TOKEN")

FILES = [
    ROOT / "docs" / "inspector-roofing-atlas-query-intelligence-technical-report-v1.1.1.pdf",
    ROOT.parent / "inspector-roofing-atlas-source-spine-v1.1.1.zip",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def request(method: str, path_or_url: str, *, body=None, headers=None):
    if not TOKEN:
        fail("Set ZENODO_ACCESS_TOKEN before running this script.")
    url = path_or_url if path_or_url.startswith("http") else f"{ZENODO_API}{path_or_url}"
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}{urllib.parse.urlencode({'access_token': TOKEN})}"
    data = None
    final_headers = headers or {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        final_headers = {"Content-Type": "application/json", **final_headers}
    req = urllib.request.Request(url, data=data, method=method, headers=final_headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            payload = response.read()
            if not payload:
                return {}
            return json.loads(payload.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        fail(f"Zenodo API {exc.code}: {detail}")


def put_file(bucket_url: str, path: Path) -> None:
    if not path.exists():
        fail(f"Missing file: {path}")
    url = f"{bucket_url}/{urllib.parse.quote(path.name)}?{urllib.parse.urlencode({'access_token': TOKEN})}"
    req = urllib.request.Request(url, data=path.read_bytes(), method="PUT")
    with urllib.request.urlopen(req, timeout=120) as response:
        if response.status not in (200, 201):
            fail(f"Upload failed for {path.name}: HTTP {response.status}")


def main() -> None:
    metadata = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    deposition = request("POST", "/deposit/depositions", body={})
    dep_id = deposition["id"]
    bucket = deposition["links"]["bucket"]
    print(f"Created Zenodo deposition {dep_id}")

    for path in FILES:
        print(f"Uploading {path.name}...")
        put_file(bucket, path)

    request("PUT", f"/deposit/depositions/{dep_id}", body={"metadata": metadata})
    print("Metadata saved.")

    publish = os.environ.get("ZENODO_PUBLISH", "").lower() in {"1", "true", "yes"}
    if publish:
        result = request("POST", f"/deposit/depositions/{dep_id}/actions/publish")
        doi = result.get("doi") or result.get("metadata", {}).get("doi")
        print(f"Published Zenodo record. DOI: {doi}")
    else:
        print("Draft created but not published. Set ZENODO_PUBLISH=1 to publish automatically.")
        print(f"Review at: https://zenodo.org/uploads/{dep_id}")


if __name__ == "__main__":
    main()
