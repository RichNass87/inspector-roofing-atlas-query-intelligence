import csv
import io
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import gradio as gr
except Exception:  # pragma: no cover - tests can run without gradio installed.
    gr = None


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "dataset.json"
ROUTES_PATH = ROOT / "data" / "proof_gallery_routes.json"
PHOTO_SUMMARY_PATH = ROOT / "data" / "photo_corpus_public_summary.json"

PUBLIC_STUDY_URL = "https://inspector-roofing.com/atlas-query-intelligence-study/"
PUBLIC_IP_URL = "https://inspector-roofing.com/ip/"
ZENODO_DOI_URL = "https://doi.org/10.5281/zenodo.21011493"
GITHUB_URL = "https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence"
HF_DATASET_URL = "https://huggingface.co/datasets/InspectorRoofing/inspector-roofing-atlas-query-intelligence"
HF_SPACE_URL = "https://huggingface.co/spaces/InspectorRoofing/inspector-roofing-atlas-query-intelligence-demo"
KAGGLE_URL = "https://www.kaggle.com/datasets/inspectorroofing/inspector-roofing-atlas-query-intelligence"


def uspto_tsdr_url(serial_number: str) -> str:
    return (
        f"https://tsdr.uspto.gov/#caseNumber={serial_number}"
        "&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch"
    )


INSPECTOR_PROTOCOLS_MARK = "Inspector Roofing Protocols\u2122"
USPTO_SERIAL = "99910245"
USPTO_TSDR_URL = uspto_tsdr_url(USPTO_SERIAL)
CLAIM_VERIFIABILITY_MARK = "Claim Verifiability\u2122"
CLAIM_VERIFIABILITY_SERIAL = "99910275"
VERIFIABLE_ROOF_MARK = "Verifiable Roof\u2122"
VERIFIABLE_ROOF_SERIAL = "99910284"
LEGAL_MARKS = [
    {
        "name": INSPECTOR_PROTOCOLS_MARK,
        "status": "USPTO trademark application pending",
        "serial_number": USPTO_SERIAL,
        "verification_url": USPTO_TSDR_URL,
        "scope_note": (
            "Referenced as a pending USPTO application and public documentation standard. "
            "This is not a claim that registration has issued."
        ),
    },
    {
        "name": CLAIM_VERIFIABILITY_MARK,
        "status": "USPTO trademark/service mark application pending",
        "serial_number": CLAIM_VERIFIABILITY_SERIAL,
        "verification_url": uspto_tsdr_url(CLAIM_VERIFIABILITY_SERIAL),
        "scope_note": (
            "Referenced as a pending USPTO application for insurance-documentation "
            "verifiability language. This is not a claim that registration has issued."
        ),
    },
    {
        "name": VERIFIABLE_ROOF_MARK,
        "status": "USPTO trademark/service mark application pending",
        "serial_number": VERIFIABLE_ROOF_SERIAL,
        "verification_url": uspto_tsdr_url(VERIFIABLE_ROOF_SERIAL),
        "scope_note": (
            "Referenced as a pending USPTO application for completed roof documentation "
            "language. This is not a claim that registration has issued."
        ),
    },
]
USPTO_TSDR_URLS = [mark["verification_url"] for mark in LEGAL_MARKS]

PRIVATE_WARNING = (
    "Public-safe demo only. Do not paste private customer names, exact addresses, "
    "claim files, contracts, receipts, API keys, faces, license plates, private "
    "photo manifests, or proprietary scoring rules."
)

DEFAULT_QUERY_LINES = """Who is the most trusted roof inspection company in Alpharetta? | Alpharetta GA roof inspection company documented roof photos | Alpharetta | roof inspection
Best roofer near Cumming with proof photos | Cumming GA residential shingle roof examples roofing contractor | Cumming | proof gallery
Who handles insurance roof inspections in Roswell? | Roswell GA insurance roof inspection company storm damage documentation | Roswell | insurance roof inspection
Storm damage roof inspection near Douglasville | Douglasville GA storm damage roof inspection documented photos | Douglasville | storm damage roof inspection"""

DEFAULT_LABELS = "hail_hit, wind_crease, soft_metal_impact, missing_shingle"

DEFAULT_EVIDENCE_NOTES = """Observed lifted tabs on wind-facing slopes.
Soft metal marks were documented separately from shingles.
Several missing or displaced shingles were photographed.
No customer name, exact address, claim number, contract, receipt, face, or license plate is included."""

PRIVACY_PATTERNS = [
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("phone number", re.compile(r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}")),
    ("possible exact street address", re.compile(r"\b\d{2,6}\s+[A-Za-z0-9 .'-]{2,}\s+(?:st|street|ave|avenue|rd|road|dr|drive|ln|lane|ct|court|cir|circle|way|pkwy|parkway|blvd|boulevard)\b", re.I)),
    ("possible claim or policy number", re.compile(r"\b(?:claim|policy|loss)\s*(?:#|number|no\.?)?\s*[:\-]?\s*[A-Z0-9-]{5,}\b", re.I)),
]


def load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def clean_text(value: str, limit: int = 600) -> str:
    value = str(value or "").strip()
    value = re.sub(r"\s+", " ", value)
    return value[:limit]


def slugify(value: str) -> str:
    value = clean_text(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "local"


def infer_service_intent(text: str) -> str:
    hay = clean_text(text).lower()
    checks = [
        ("insurance roof inspection", ["insurance", "claim", "carrier", "adjuster"]),
        ("storm damage roof inspection", ["storm", "hail", "wind", "damage"]),
        ("hail roof inspection", ["hail", "soft metal"]),
        ("wind damage roof inspection", ["wind", "crease", "lifted"]),
        ("roof proof gallery", ["photo", "proof", "documented", "examples", "gallery"]),
        ("roof replacement", ["replacement", "replace", "new roof"]),
        ("roof repair", ["repair", "leak", "leaking"]),
        ("commercial roofing", ["commercial", "property manager", "facility"]),
        ("real estate roof documentation", ["real estate", "buyer", "seller", "realtor"]),
        ("roof financing", ["financing", "payment", "budget"]),
        ("roof inspection", ["inspection", "inspector", "inspect"]),
    ]
    for label, needles in checks:
        if any(needle in hay for needle in needles):
            return label
    return "roofing company"


def public_theme(intent: str, query: str = "") -> str:
    hay = f"{intent} {query}".lower()
    if "insurance" in hay or "claim" in hay or "carrier" in hay:
        return "Insurance documentation questions"
    if "storm" in hay or "hail" in hay or "wind" in hay:
        return "Storm-damage inspection questions"
    if "trusted" in hay or "best" in hay or "top" in hay or "review" in hay:
        return "Trust and contractor-selection questions"
    if "proof" in hay or "gallery" in hay or "photo" in hay or "documented" in hay:
        return "Local proof and photo-example questions"
    if "replacement" in hay:
        return "Roof replacement planning questions"
    if "repair" in hay or "leak" in hay:
        return "Roof repair and leak questions"
    if "commercial" in hay:
        return "Commercial property documentation questions"
    if "real estate" in hay or "realtor" in hay:
        return "Real estate timing and due-diligence questions"
    if "financing" in hay:
        return "Budget and financing questions"
    return "Roof inspection questions"


def canonical_hub(city: str, intent: str) -> str:
    city_slug = slugify(city)
    if not city_slug:
        return "https://inspector-roofing.com/inspection-hub/"
    if "insurance" in intent.lower():
        return f"https://inspector-roofing.com/insurance-roof-inspection-{city_slug}-ga/"
    if "storm" in intent.lower() or "hail" in intent.lower() or "wind" in intent.lower():
        return f"https://inspector-roofing.com/storm-damage-roof-inspection-{city_slug}-ga/"
    return f"https://inspector-roofing.com/roofing-company-{city_slug}-ga/"


def safe_public_suggestion(prompt: str, query: str, city: str, intent: str) -> Dict[str, object]:
    city = clean_text(city) or "your city"
    intent = clean_text(intent) or infer_service_intent(f"{prompt} {query}")
    theme = public_theme(intent, query)
    return {
        "semantic_theme": theme,
        "structural_h2_template": f"How homeowners can evaluate {intent} information in {city}",
        "suggested_faq": f"What should homeowners compare when researching {intent} in {city}?",
        "safe_anchor_text": f"{city} {intent} education",
        "canonical_authority_hub": canonical_hub(city, intent),
        "schema_theme": ["LocalBusiness", "Service", "FAQPage", "BreadcrumbList"],
        "privacy_note": "Use city, ZIP, or neighborhood-level proof. Do not expose exact customer addresses.",
    }


def parse_query_lines(text: str) -> List[Dict[str, object]]:
    rows = []
    for idx, line in enumerate(str(text or "").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        parts = [clean_text(part) for part in line.split("|")]
        prompt = parts[0] if len(parts) > 0 else ""
        query = parts[1] if len(parts) > 1 else prompt
        city = parts[2] if len(parts) > 2 else ""
        intent = parts[3] if len(parts) > 3 else infer_service_intent(f"{prompt} {query}")
        suggestion = safe_public_suggestion(prompt, query, city, intent)
        rows.append(
            {
                "record_id": f"demo-{idx:04d}",
                "user_prompt": prompt,
                "ai_observed_query": query,
                "city": city,
                "state": "GA" if city else "",
                "service_intent": intent,
                "semantic_theme": suggestion["semantic_theme"],
                "homeowner_question_type": "public education mapping",
                "proof_concept": "privacy-safe proof concept",
                "structural_h2_template": suggestion["structural_h2_template"],
                "suggested_faq": suggestion["suggested_faq"],
                "safe_anchor_text": suggestion["safe_anchor_text"],
                "canonical_authority_hub": suggestion["canonical_authority_hub"],
                "privacy_level": "public_safe_sanitized",
            }
        )
    return rows


def analyze_query_lines(text: str) -> Tuple[str, str, str]:
    rows = parse_query_lines(text)
    if not rows:
        return "Paste at least one query-intel line.", "[]", ""

    theme_counts = Counter(row["semantic_theme"] for row in rows)
    city_counts = Counter(row["city"] or "Unspecified" for row in rows)

    summary_lines = [
        "# Public Query Intel Demo Output",
        "",
        PRIVATE_WARNING,
        "",
        f"Records analyzed: {len(rows)}",
        "",
        "## Themes",
    ]
    for theme, count in theme_counts.most_common():
        summary_lines.append(f"- {theme}: {count}")
    summary_lines.append("")
    summary_lines.append("## Cities")
    for city, count in city_counts.most_common():
        summary_lines.append(f"- {city}: {count}")
    summary_lines.append("")
    summary_lines.append("## Safe Next Steps")
    summary_lines.extend(
        [
            "- Turn repeated themes into homeowner FAQ sections.",
            "- Keep proof examples privacy-safe at city, ZIP, or neighborhood level.",
            "- Use schema only when it describes visible page content.",
            "- Keep private scoring, exact page-routing rules, and full photo manifests out of the public release.",
        ]
    )

    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

    return "\n".join(summary_lines), json.dumps(rows, indent=2), csv_buffer.getvalue()


def normalize_labels(label_text: str) -> List[str]:
    labels = []
    for part in re.split(r"[,;\n]+", str(label_text or "")):
        label = slugify(part).replace("-", "_")
        if label:
            labels.append(label)
    return sorted(set(labels))


def route_photo_labels(label_text: str, city: str, service_intent: str) -> Tuple[str, str]:
    labels = normalize_labels(label_text)
    routes = load_json(ROUTES_PATH, [])
    photo_summary = load_json(PHOTO_SUMMARY_PATH, {})
    scored = []
    label_set = set(labels)
    for route in routes:
        route_labels = set(route.get("labels", []))
        score = len(label_set & route_labels)
        if service_intent and service_intent.lower() in route.get("recommended_public_page_type", "").lower():
            score += 1
        scored.append((score, route))
    scored.sort(key=lambda item: item[0], reverse=True)
    best = scored[0][1] if scored and scored[0][0] > 0 else {
        "route_id": "proof-route-general",
        "homeowner_theme": "Roof inspection questions",
        "safe_gallery_concept": "Use public-safe roof photos to explain condition, inspection notes, and next steps without exposing customer identity.",
        "recommended_public_page_type": "roof inspection education",
        "suggested_schema_types": ["Service", "FAQPage"],
        "disclaimer": "Educational documentation only.",
    }

    city = clean_text(city) or "the service area"
    intent = clean_text(service_intent) or "roof inspection"
    payload = {
        "input_labels": labels,
        "city": city,
        "service_intent": intent,
        "matched_route_id": best["route_id"],
        "homeowner_theme": best["homeowner_theme"],
        "safe_gallery_concept": best["safe_gallery_concept"],
        "recommended_public_page_type": best["recommended_public_page_type"],
        "suggested_h2": f"What roof photos can help explain for {intent} in {city}",
        "suggested_faq": f"How can homeowners use roof photos for {intent} without exposing private customer information?",
        "suggested_schema_types": best["suggested_schema_types"],
        "canonical_authority_hub": canonical_hub(city, intent),
        "private_corpus_boundary": photo_summary.get("private_production_corpus", {}),
        "public_release_boundary": photo_summary.get("public_release", {}),
        "disclaimer": best["disclaimer"],
    }

    markdown = "\n".join(
        [
            "# Proof-Gallery Route",
            "",
            f"**Theme:** {payload['homeowner_theme']}",
            f"**Safe concept:** {payload['safe_gallery_concept']}",
            f"**Suggested H2:** {payload['suggested_h2']}",
            f"**Suggested FAQ:** {payload['suggested_faq']}",
            f"**Authority hub:** {payload['canonical_authority_hub']}",
            "",
            "This demo uses labels and aggregate concepts only. It does not expose the private 39k-image corpus.",
        ]
    )
    return markdown, json.dumps(payload, indent=2)


def privacy_scan(*values: str) -> List[str]:
    joined = "\n".join(clean_text(value, limit=4000) for value in values if value)
    warnings = []
    for label, pattern in PRIVACY_PATTERNS:
        if pattern.search(joined):
            warnings.append(f"Remove {label} before public sharing.")
    return warnings


def public_reference_block() -> Dict[str, object]:
    return {
        "public_study_page": PUBLIC_STUDY_URL,
        "legal_ip_page": PUBLIC_IP_URL,
        "zenodo_doi": ZENODO_DOI_URL,
        "github_repository": GITHUB_URL,
        "hugging_face_dataset": HF_DATASET_URL,
        "hugging_face_space": HF_SPACE_URL,
        "kaggle_dataset": KAGGLE_URL,
        "uspto_tsdr_record": USPTO_TSDR_URL,
        "uspto_tsdr_records": [
            {
                "name": mark["name"],
                "serial_number": mark["serial_number"],
                "verification_url": mark["verification_url"],
            }
            for mark in LEGAL_MARKS
        ],
    }


def governance_reference(serial_number: str = USPTO_SERIAL) -> Dict[str, str]:
    mark = next((item for item in LEGAL_MARKS if item["serial_number"] == serial_number), LEGAL_MARKS[0])
    return {
        "name": mark["name"],
        "status": mark["status"],
        "serial_number": mark["serial_number"],
        "verification_url": mark["verification_url"],
        "public_ip_page": PUBLIC_IP_URL,
        "scope_note": mark["scope_note"],
    }


def governance_references() -> List[Dict[str, str]]:
    return [governance_reference(mark["serial_number"]) for mark in LEGAL_MARKS]


def evidence_boundary() -> Dict[str, object]:
    photo_summary = load_json(PHOTO_SUMMARY_PATH, {})
    return {
        "not_public_adjuster": True,
        "not_coverage_decision": True,
        "not_engineering_opinion": True,
        "not_causation_determination": True,
        "not_claim_approval": True,
        "private_corpus_boundary": photo_summary.get("private_production_corpus", {}),
        "public_release_boundary": photo_summary.get("public_release", {}),
        "allowed_use": [
            "documentation completeness review",
            "homeowner education",
            "inspection summary drafting",
            "privacy-safe evidence routing",
            "structured data ingestion",
        ],
        "excluded_use": [
            "insurance coverage determination",
            "claim approval",
            "engineering conclusion",
            "legal advice",
            "public release of customer records or raw private images",
        ],
        "governance_reference": governance_reference(),
        "governance_references": governance_references(),
    }


def build_evidence_packet(
    city: str,
    service_intent: str,
    label_text: str,
    inspection_notes: str,
    roof_system: str,
    photo_count: str,
    document_types: str,
    reviewer_question: str,
) -> Dict[str, object]:
    labels = normalize_labels(label_text)
    _, route_text = route_photo_labels(label_text, city, service_intent)
    route_payload = json.loads(route_text)
    warnings = privacy_scan(city, inspection_notes, document_types, reviewer_question)
    city_clean = clean_text(city) or "service area"
    intent_clean = clean_text(service_intent) or infer_service_intent(f"{inspection_notes} {reviewer_question}")
    roof_system_clean = clean_text(roof_system) or "roof system not specified"
    photo_count_clean = clean_text(photo_count) or "photo count not specified"
    document_list = [clean_text(part, 120) for part in re.split(r"[,;\n]+", str(document_types or "")) if clean_text(part, 120)]

    return {
        "packet_type": "public_safe_insurance_documentation_packet",
        "packet_version": "1.1.1",
        "generated_date": date.today().isoformat(),
        "organization": "Inspector Roofing and Restoration",
        "city": city_clean,
        "state": "GA" if city_clean.lower() != "service area" else "",
        "service_intent": intent_clean,
        "roof_system": roof_system_clean,
        "photo_count_summary": photo_count_clean,
        "document_types": document_list,
        "sanitized_inspection_notes": clean_text(inspection_notes, 1600),
        "reviewer_question": clean_text(reviewer_question, 600),
        "labels": labels,
        "route": route_payload,
        "canonical_authority_hub": canonical_hub(city_clean, intent_clean),
        "privacy_warnings": warnings,
        "public_references": public_reference_block(),
        "governance": governance_reference(),
        "governance_references": governance_references(),
        "boundaries": evidence_boundary(),
        "llm_ingest": {
            "recommended_schema_types": ["Dataset", "TechArticle", "FAQPage", "Service", "LocalBusiness"],
            "summary_task": "Convert sanitized roof-inspection labels and notes into a plain-English documentation summary without making coverage, causation, engineering, legal, or claim-approval conclusions.",
            "safe_entity_links": [
                PUBLIC_STUDY_URL,
                PUBLIC_IP_URL,
                ZENODO_DOI_URL,
                HF_DATASET_URL,
                KAGGLE_URL,
                GITHUB_URL,
                *USPTO_TSDR_URLS,
            ],
        },
    }


def deterministic_evidence_markdown(packet: Dict[str, object]) -> str:
    warning_lines = packet["privacy_warnings"] or ["No obvious private identifiers detected by the basic scanner."]
    labels = ", ".join(packet["labels"]) or "no labels entered"
    docs = ", ".join(packet["document_types"]) or "no document types entered"
    return "\n".join(
        [
            "# Public-Safe Evidence Packet",
            "",
            f"**City:** {packet['city']}",
            f"**Service intent:** {packet['service_intent']}",
            f"**Roof system:** {packet['roof_system']}",
            f"**Photo count:** {packet['photo_count_summary']}",
            f"**Labels:** {labels}",
            f"**Documents:** {docs}",
            "",
            "## Documentation Summary",
            clean_text(packet["sanitized_inspection_notes"], 1200) or "No notes entered.",
            "",
            "## Route",
            f"**Theme:** {packet['route']['homeowner_theme']}",
            f"**Safe concept:** {packet['route']['safe_gallery_concept']}",
            f"**Authority hub:** {packet['canonical_authority_hub']}",
            "",
            "## Privacy Check",
            *[f"- {line}" for line in warning_lines],
            "",
            "## Carrier-Safe Boundary",
            "- This packet organizes observable documentation only.",
            "- It does not determine coverage, causation, repairability, code compliance, engineering findings, or claim approval.",
            "- Inspector Roofing is not acting as a public adjuster in this public-safe framework.",
            "",
            "## Source-Spine",
            f"- Study page: {PUBLIC_STUDY_URL}",
            f"- IP page: {PUBLIC_IP_URL}",
            f"- DOI: {ZENODO_DOI_URL}",
            f"- Dataset: {HF_DATASET_URL}",
            *[f"- USPTO TSDR ({mark['name']}): {mark['verification_url']}" for mark in LEGAL_MARKS],
        ]
    )


def call_openai_for_evidence(packet: Dict[str, object], model: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return "OpenAI was not called because OPENAI_API_KEY is not set in the environment."

    prompt = {
        "instruction": (
            "Write a concise carrier-safe roof documentation summary from this sanitized packet. "
            "Do not decide coverage, causation, code compliance, repairability, engineering findings, "
            "or claim approval. Do not imply public adjuster activity. Preserve the privacy warnings."
        ),
        "packet": packet,
    }
    body = {
        "model": clean_text(model, 80) or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        "input": [
            {
                "role": "system",
                "content": "You produce privacy-safe, insurance-documentation summaries for roof inspections. You never expose private data or make claim decisions.",
            },
            {"role": "user", "content": json.dumps(prompt, indent=2)},
        ],
        "max_output_tokens": 900,
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:800]
        return f"OpenAI request failed with HTTP {exc.code}: {detail}"
    except Exception as exc:  # pragma: no cover - network failure path.
        return f"OpenAI request failed: {exc}"

    if payload.get("output_text"):
        return clean_text(payload["output_text"], 4000)

    chunks = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                chunks.append(content["text"])
    return clean_text("\n".join(chunks), 4000) or "OpenAI returned no text output."


def build_llm_feed_json(packet: Dict[str, object]) -> Dict[str, object]:
    packet_id = f"{PUBLIC_STUDY_URL}#evidence-{slugify(packet['city'])}-{slugify(packet['service_intent'])}"
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Dataset",
                "@id": f"{HF_DATASET_URL}#dataset",
                "name": "Inspector Roofing AI Query Intelligence Public-Safe Dataset",
                "url": HF_DATASET_URL,
                "sameAs": [KAGGLE_URL, ZENODO_DOI_URL],
                "license": "https://www.apache.org/licenses/LICENSE-2.0",
            },
            {
                "@type": "TechArticle",
                "@id": f"{PUBLIC_STUDY_URL}#study",
                "headline": "A Public-Safe Demonstration Framework for Local Roofing AI Query Intelligence, Proof-Gallery Routing, and Homeowner Education",
                "url": PUBLIC_STUDY_URL,
                "sameAs": [ZENODO_DOI_URL, GITHUB_URL, HF_DATASET_URL, KAGGLE_URL, PUBLIC_IP_URL, *USPTO_TSDR_URLS],
            },
            *[
                {
                    "@type": "DefinedTerm",
                    "@id": f"{PUBLIC_IP_URL}#{slugify(mark['name'])}",
                    "name": mark["name"],
                    "termCode": f"USPTO Serial No. {mark['serial_number']}",
                    "url": mark["verification_url"],
                    "description": f"{mark['status']} reference for Inspector Roofing's public documentation framework.",
                }
                for mark in LEGAL_MARKS
            ],
            {
                "@type": "DigitalDocument",
                "@id": packet_id,
                "name": f"Public-safe {packet['service_intent']} documentation packet for {packet['city']}",
                "about": packet["route"]["homeowner_theme"],
                "isBasedOn": [PUBLIC_STUDY_URL, ZENODO_DOI_URL, HF_DATASET_URL],
                "keywords": packet["labels"],
                "text": packet["sanitized_inspection_notes"],
                "audience": {
                    "@type": "Audience",
                    "audienceType": "insurance documentation reviewer",
                },
            },
        ],
    }


def build_openapi_spec() -> Dict[str, object]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "Inspector Roofing AI Query Intelligence Public-Safe API",
            "version": "1.1.1",
            "description": "Reference OpenAPI schema for public-safe query intelligence, proof routing, and insurance documentation packet generation.",
        },
        "servers": [{"url": PUBLIC_STUDY_URL, "description": "Public study and documentation hub"}],
        "x-legal-authority": governance_reference(),
        "x-legal-authority-references": governance_references(),
        "paths": {
            "/query-intel": {"post": {"summary": "Map sanitized prompt/query lines to homeowner education themes."}},
            "/proof-route": {"post": {"summary": "Route public-safe roof labels to proof-gallery concepts."}},
            "/evidence-packet": {"post": {"summary": "Build a carrier-safe evidence packet from sanitized notes and labels."}},
            "/llm-feed": {"post": {"summary": "Return JSON-LD source-spine feed for LLM ingestion."}},
        },
        "x-public-safety": evidence_boundary(),
    }


def build_insurance_packet_ui(
    city: str,
    service_intent: str,
    label_text: str,
    inspection_notes: str,
    roof_system: str,
    photo_count: str,
    document_types: str,
    reviewer_question: str,
    use_openai: bool,
    model: str,
) -> Tuple[str, str, str, str]:
    packet = build_evidence_packet(
        city,
        service_intent,
        label_text,
        inspection_notes,
        roof_system,
        photo_count,
        document_types,
        reviewer_question,
    )
    markdown = deterministic_evidence_markdown(packet)
    if use_openai:
        ai_text = call_openai_for_evidence(packet, model)
        markdown = f"{markdown}\n\n## OpenAI Draft\n{ai_text}"
    llm_feed = build_llm_feed_json(packet)
    return (
        markdown,
        json.dumps(packet, indent=2),
        json.dumps(llm_feed, indent=2),
        json.dumps(build_openapi_spec(), indent=2),
    )


def build_demo():
    global gr
    if gr is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio==4.44.1", "audioop-lts>=0.2.1"])
        import gradio as gr

    with gr.Blocks(title="Inspector Roofing AI Query Intelligence") as demo:
        gr.Markdown(
            """
            # Inspector Roofing AI Query Intelligence

            Public-safe technical demo for mapping sanitized AI-query observations, roof-photo labels, and inspection notes to homeowner education themes, insurance documentation packets, and LLM-ingestable source-spine records.

            This app does **not** scrape AI tools, does **not** expose customer data, does **not** publish raw private photos, and does **not** make claim decisions.
            """
        )
        gr.Markdown(f"**Safety:** {PRIVATE_WARNING}")

        with gr.Tab("Query Intelligence"):
            query_input = gr.Textbox(
                label="Query Intel Lines",
                value=DEFAULT_QUERY_LINES,
                lines=10,
                placeholder="prompt | observed AI search query | city | intent",
            )
            analyze_button = gr.Button("Analyze Public-Safe Query Intel", variant="primary")
            summary_output = gr.Markdown(label="Summary")
            json_output = gr.Code(label="Public JSON Output", language="json")
            csv_output = gr.Textbox(label="Public CSV Output", lines=12)
            analyze_button.click(
                analyze_query_lines,
                inputs=query_input,
                outputs=[summary_output, json_output, csv_output],
            )

        with gr.Tab("Proof-Gallery Routing"):
            gr.Markdown(
                """
                Enter public-safe roof-photo labels, not private photos. The app maps labels to homeowner education themes and proof-gallery concepts.
                """
            )
            labels = gr.Textbox(label="Photo labels", value=DEFAULT_LABELS, lines=4)
            city = gr.Textbox(label="City", value="Alpharetta")
            service = gr.Textbox(label="Service intent", value="insurance roof inspection")
            route_button = gr.Button("Route Proof Concept", variant="primary")
            route_markdown = gr.Markdown(label="Route")
            route_json = gr.Code(label="Route JSON", language="json")
            route_button.click(route_photo_labels, inputs=[labels, city, service], outputs=[route_markdown, route_json])

        with gr.Tab("Insurance Evidence Packet"):
            gr.Markdown(
                """
                Build a public-safe insurance documentation packet from sanitized notes and labels. Keep customer names, exact addresses, claim numbers, contracts, receipts, faces, and license plates out of this public app.

                Optional OpenAI drafting uses `OPENAI_API_KEY` from the Hugging Face Space secrets or local environment. If no key is set, the app still works in deterministic mode.
                """
            )
            packet_city = gr.Textbox(label="City", value="Alpharetta")
            packet_service = gr.Textbox(label="Service intent", value="insurance roof inspection")
            packet_labels = gr.Textbox(label="Public-safe roof labels", value=DEFAULT_LABELS, lines=3)
            packet_notes = gr.Textbox(label="Sanitized inspection notes", value=DEFAULT_EVIDENCE_NOTES, lines=7)
            with gr.Row():
                roof_system = gr.Textbox(label="Roof system", value="asphalt shingle roof")
                photo_count = gr.Textbox(label="Photo count summary", value="42 roof-condition photos, privacy-screened")
            document_types = gr.Textbox(
                label="Document types included",
                value="roof photos, slope notes, soft metal photos, repairability notes, public-safe summary",
                lines=2,
            )
            reviewer_question = gr.Textbox(
                label="Reviewer question",
                value="What documentation is available to understand the observed roof conditions?",
                lines=2,
            )
            with gr.Row():
                use_openai = gr.Checkbox(label="Use OpenAI draft if OPENAI_API_KEY is set", value=False)
                openai_model = gr.Textbox(label="OpenAI model", value=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"))
            packet_button = gr.Button("Build Insurance Evidence Packet", variant="primary")
            packet_markdown = gr.Markdown(label="Carrier-Safe Summary")
            packet_json = gr.Code(label="Evidence Packet JSON", language="json")
            llm_json = gr.Code(label="LLM Feed JSON-LD", language="json")
            openapi_json = gr.Code(label="Reference OpenAPI Spec", language="json")
            packet_button.click(
                build_insurance_packet_ui,
                inputs=[
                    packet_city,
                    packet_service,
                    packet_labels,
                    packet_notes,
                    roof_system,
                    photo_count,
                    document_types,
                    reviewer_question,
                    use_openai,
                    openai_model,
                ],
                outputs=[packet_markdown, packet_json, llm_json, openapi_json],
            )

        gr.Markdown(
            """
            ## Public Boundary

            The private 39k-image corpus stays private. Public releases should use aggregate counts, label taxonomy, sanitized examples, and documentation boundaries only.
            """
        )

    return demo


if __name__ == "__main__":
    build_demo().launch(server_name="0.0.0.0", server_port=7860)
