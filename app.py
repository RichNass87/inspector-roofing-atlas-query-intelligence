import csv
import io
import json
import re
from collections import Counter
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
            "This demo uses labels and aggregate concepts only. It does not expose the private 38k-image corpus.",
        ]
    )
    return markdown, json.dumps(payload, indent=2)


def build_demo():
    if gr is None:
        raise RuntimeError("gradio is not installed. Run `pip install -r requirements.txt` first.")

    with gr.Blocks(title="Inspector Roofing Atlas Query Intelligence") as demo:
        gr.Markdown(
            """
            # Inspector Roofing Atlas Query Intelligence

            Public-safe technical demo for mapping sanitized AI-query observations to homeowner education themes and privacy-safe proof-gallery concepts.

            This app does **not** scrape AI tools, does **not** expose customer data, and does **not** publish proprietary scoring.
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

        gr.Markdown(
            """
            ## Public Boundary

            The private 38k-image corpus stays private. Public releases should use aggregate counts, label taxonomy, sanitized examples, and documentation boundaries only.
            """
        )

    return demo


if __name__ == "__main__":
    build_demo().launch()
