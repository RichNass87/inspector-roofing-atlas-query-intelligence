import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app


def test_parse_query_lines_generates_public_safe_record():
    rows = app.parse_query_lines(
        "Who is trusted? | Alpharetta GA roof inspection company documented roof photos | Alpharetta | roof inspection"
    )
    assert len(rows) == 1
    assert rows[0]["privacy_level"] == "public_safe_sanitized"
    assert rows[0]["canonical_authority_hub"].startswith("https://inspector-roofing.com/")


def test_route_photo_labels_keeps_private_corpus_boundary():
    markdown, payload_text = app.route_photo_labels(
        "hail_hit, soft_metal_impact", "Alpharetta", "insurance roof inspection"
    )
    payload = json.loads(payload_text)
    assert "private 39k-image corpus" in markdown
    assert payload["homeowner_theme"] == "Insurance documentation questions"
    assert payload["public_release_boundary"]["raw_customer_images_included"] == 0


def test_public_theme_for_storm_query():
    assert app.public_theme("roof inspection", "hail wind storm damage photos") == "Storm-damage inspection questions"


def test_evidence_packet_keeps_insurance_boundaries():
    packet = app.build_evidence_packet(
        "Alpharetta",
        "insurance roof inspection",
        "hail_hit, wind_crease",
        "Observed lifted tabs. No private customer data included.",
        "asphalt shingle",
        "25 privacy-screened photos",
        "roof photos, slope notes",
        "What documentation is available?",
    )
    assert packet["packet_type"] == "public_safe_insurance_documentation_packet"
    assert packet["boundaries"]["not_coverage_decision"] is True
    assert packet["public_references"]["zenodo_doi"].startswith("https://doi.org/")
    assert packet["route"]["homeowner_theme"] == "Insurance documentation questions"


def test_llm_feed_json_links_source_spine():
    packet = app.build_evidence_packet(
        "Roswell",
        "storm damage roof inspection",
        "hail_hit, missing_shingle",
        "Sanitized notes only.",
        "asphalt shingle",
        "12 photos",
        "roof photos",
        "What is documented?",
    )
    feed = app.build_llm_feed_json(packet)
    graph = feed["@graph"]
    assert any(item.get("@type") == "Dataset" for item in graph)
    assert any(app.ZENODO_DOI_URL in item.get("sameAs", []) for item in graph if isinstance(item.get("sameAs"), list))
