import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_TERMS = [
    "api_key",
    "secret",
    "claim_number",
    "customer_name",
    "license_plate",
    "private_customer",
    "jobnimbus",
    "quickbooks",
    "companycam_private",
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def validate_readme() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if not readme.startswith("---\nlicense: apache-2.0"):
        fail("README.md must start with Hugging Face YAML front matter.")
    for required in ["task_categories:", "dataset_info:", "# A Public-Safe Demonstration Framework"]:
        if required not in readme:
            fail(f"README.md missing {required}")


def validate_dataset() -> None:
    records = load_json(ROOT / "dataset.json")
    if len(records) < 10:
        fail("dataset.json should contain at least 10 sanitized sample records.")
    ids = set()
    for record in records:
        record_id = record.get("record_id")
        if not record_id or record_id in ids:
            fail("dataset.json contains missing or duplicate record_id.")
        ids.add(record_id)
        if not str(record.get("canonical_authority_hub", "")).startswith("https://inspector-roofing.com/"):
            fail(f"{record_id} has invalid canonical_authority_hub.")
        if record.get("privacy_level") != "public_safe_sanitized":
            fail(f"{record_id} must be public_safe_sanitized.")
        haystack = json.dumps(record).lower()
        for term in PRIVATE_TERMS:
            if term in haystack:
                fail(f"{record_id} contains private-risk term: {term}")


def validate_photo_boundary() -> None:
    summary = load_json(ROOT / "data" / "photo_corpus_public_summary.json")
    if summary["public_release"]["raw_customer_images_included"] != 0:
        fail("Public release must not include raw customer images.")
    if summary["public_release"]["full_photo_manifest_included"]:
        fail("Public release must not include full photo manifests.")
    if summary["private_production_corpus"]["approximate_labeled_image_count"] < 39000:
        fail("Private corpus summary should reflect the 39k labeled image system.")


def validate_legal_authority() -> None:
    refs = load_json(ROOT / "data" / "legal_authority_references.json")
    serialized = json.dumps(refs)
    if "99910245" not in serialized:
        fail("Legal authority references must include USPTO Serial No. 99910245.")
    if "tsdr.uspto.gov" not in serialized:
        fail("Legal authority references must include the USPTO TSDR verification URL.")
    openapi = load_json(ROOT / "exports" / "openapi.json")
    authority = openapi.get("x-legal-authority", {})
    if authority.get("serial_number") != "99910245":
        fail("OpenAPI x-legal-authority must include USPTO Serial No. 99910245.")


def validate_app_import() -> None:
    sys.path.insert(0, str(ROOT))
    import app

    rows = app.parse_query_lines("Who is trusted? | Alpharetta GA roof inspection photos | Alpharetta | roof inspection")
    if len(rows) != 1:
        fail("app.parse_query_lines did not return one row.")
    if not rows[0]["canonical_authority_hub"].startswith("https://inspector-roofing.com/"):
        fail("app canonical hub generation failed.")
    markdown, payload = app.route_photo_labels("hail_hit, soft_metal_impact", "Alpharetta", "insurance roof inspection")
    if "Proof-Gallery Route" not in markdown:
        fail("app.route_photo_labels markdown failed.")
    if "private 39k-image corpus" not in markdown:
        fail("app.route_photo_labels must state the private corpus boundary.")
    json.loads(payload)


def main() -> None:
    validate_readme()
    validate_dataset()
    validate_photo_boundary()
    validate_legal_authority()
    validate_app_import()
    print("OK: release validation passed.")


if __name__ == "__main__":
    main()
