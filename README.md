---
license: apache-2.0
task_categories:
- text-classification
- feature-extraction
- object-detection
tags:
- local-seo
- geo-optimization
- ai-visibility
- natural-language-processing
- computer-vision
- roof-inspection
- query-intelligence
- privacy-preserving-data
dataset_info:
  features:
  - name: user_prompt
    dtype: string
  - name: ai_observed_query
    dtype: string
  - name: semantic_theme
    dtype: string
  - name: structural_h2_template
    dtype: string
  - name: suggested_faq
    dtype: string
  - name: canonical_authority_hub
    dtype: string
  splits:
  - name: train
    num_bytes: 24500
    num_examples: 20
---

# A Public-Safe Demonstration Framework for Local Roofing AI Query Intelligence, Proof-Gallery Routing, and Homeowner Education

**Author / Organization:** Richard Nasser, Inspector Roofing and Restoration, Alpharetta, Georgia  
**Project type:** open-source research framework and technical demonstration  
**Public release:** v1.1.1
**License:** Apache-2.0 for public templates, code, schemas, and documentation

## Abstract

Local service businesses increasingly need to communicate clearly to homeowners, search engines, and AI-assisted answer systems. This repository describes a public-safe demonstration framework for organizing manually observed AI-search query language into broad local roofing education themes.

The framework does **not** scrape private sessions, expose customer records, publish proprietary scoring, or claim ranking outcomes. Instead, it demonstrates how sanitized query observations can be grouped by city, service intent, homeowner question type, and privacy-safe proof concepts.

The Inspector Roofing Atlas Query Intelligence System is positioned as a public research and education artifact that supports better local roofing communication. It includes sanitized templates, sample query-intel records, JSON schemas, photo-label taxonomy examples, a working Gradio demo app, a public-safe insurance evidence packet builder, an LLM-feed JSON-LD export, and a reference OpenAPI schema. The production implementation, private customer data, exact page-routing rules, operational scoring, and private photo manifests remain proprietary.

## Plain-English Summary

People ask AI systems questions differently than the web searches those systems may perform. A homeowner may ask, "Who is the most trusted roof inspector near me?" while an AI system may search for terms closer to "documented roof photos," "roof inspection company," and the city name.

Observing that gap can help a local business write clearer homeowner education pages. This public demo shows the concept without giving away private systems, customer data, or the complete production photo library.

## Method Overview

1. Manually record a sanitized homeowner prompt and observed AI-search query.
2. Add broad city and service intent when appropriate.
3. Group the query into a homeowner education theme.
4. Generate safe, generic H2, FAQ, schema-theme, and anchor-text examples.
5. Connect query themes to privacy-safe proof-gallery concepts from roof-photo label categories.
6. Keep all private implementation, scoring, customer records, full photo manifests, exact customer locations, and production routing rules out of the public release.

## How the 39k Labeled Roof-Photo System Is Used Safely

Inspector Roofing maintains a private production corpus of approximately **39,000 labeled roof-inspection images**. That corpus is not included in this public repository.

This public project uses the photo system correctly by publishing only:

- the public label taxonomy,
- privacy-safe proof concepts,
- aggregate corpus metadata,
- sample records with no customer identifiers,
- schema definitions for future sanitized releases,
- demo routing logic that maps labels to homeowner education themes.

The public demo does **not** publish exact customer addresses, faces, license plates, private claims files, receipts, contracts, full photo manifests, private folder paths, or operational scoring rules.

## Legal And Public Authority References

This public source-spine references the following marks as pending USPTO applications only:

- Inspector Roofing Protocols™: pending USPTO trademark application, **Serial No. 99910245**.
- Claim Verifiability™: pending USPTO trademark/service mark application, **Serial No. 99910275**.
- Verifiable Roof™: pending USPTO trademark/service mark application, **Serial No. 99910284**.

Public verification links:

- https://tsdr.uspto.gov/#caseNumber=99910245&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch
- https://tsdr.uspto.gov/#caseNumber=99910275&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch
- https://tsdr.uspto.gov/#caseNumber=99910284&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch

These records should not be described as registered trademarks unless the USPTO status later changes.

## Repository Layout

```text
README.md                              Hugging Face dataset card + project overview
dataset.json                           20 sanitized query-intelligence sample records
app.py                                 Gradio demo app
requirements.txt                       Python dependencies for the demo
LICENSE                                Apache-2.0 license
CITATION.cff                           Citation metadata
.zenodo.json                           Zenodo metadata
data/photo_label_taxonomy.json          Roof-photo label taxonomy
data/photo_corpus_public_summary.json   Public-safe corpus summary
data/proof_gallery_routes.json          Label-to-proof routing examples
data/query_intelligence_sample.jsonl    JSONL copy of sample records
data/platform_links.csv                 Public source-spine platform links
data/orcid_works.bib                    ORCID BibTeX import for current works
data/orcid_works.json                   ORCID structured work list
data/public_project_inventory.csv       Project-wide GitHub/ORCID/Kaggle/OSF inventory
data/legal_authority_references.json     Public legal/source-spine authority references
schema/query_intelligence_record.schema.json
schema/photo_label_record.schema.json
schema/insurance_evidence_packet.schema.json
schema/legal_authority_reference.schema.json
docs/TECHNICAL_WHITEPAPER.md
docs/INSPECTOR_ROOFING_RESEARCH_PAGE.md
docs/INSPECTOR_ROOFING_IP_PAGE.md
docs/ZENODO_ACADEMIA_ABSTRACT.md
docs/PUBLISHING_GUIDE.md
docs/ORCID_UPDATE_NOTES.md
docs/ALL_PROJECTS_PLATFORM_ROLLOUT.md
exports/inspector-roofing-atlas-query-intelligence-study-page.html
exports/inspector-roofing-legal-ip-page.html
exports/insurance-llm-feed-template.json
exports/openapi.json
scripts/build_platform_uploads.py
scripts/validate_release.py
scripts/kaggle_publish.sh
scripts/osf_publish.sh
tests/test_app_logic.py
```

## Example Record

```json
{
  "user_prompt": "Who is the most trusted roof inspection company in Alpharetta?",
  "ai_observed_query": "Alpharetta GA roof inspection company documented roof photos",
  "semantic_theme": "Trust and contractor-selection questions",
  "structural_h2_template": "How homeowners can evaluate roof inspection information in Alpharetta",
  "suggested_faq": "What should homeowners compare when researching roof inspection companies in Alpharetta?",
  "canonical_authority_hub": "https://inspector-roofing.com/roofing-company-alpharetta-ga/"
}
```

## Privacy Position

This framework intentionally excludes:

- exact customer addresses,
- private claims files,
- contracts,
- receipts,
- faces,
- license plates,
- private customer names,
- API keys,
- full photo manifests,
- proprietary WordPress plugin logic,
- production scoring rules,
- private CompanyCam, JobNimbus, QuickBooks, or CRM records.

## Limitations

AI-search query observations are directional market research. They do not guarantee rankings, AI citations, search traffic, lead volume, or model behavior. Search engines and answer systems change over time, and public demos should be treated as educational artifacts rather than deterministic ranking systems.

The object-detection and proof-gallery components are documentation-support concepts only. They do not determine insurance coverage, causation, code compliance, repairability, engineering conclusions, or claim approval.

## Practical Use

For Inspector Roofing, this public framework supports:

- homeowner education,
- public trust and transparency,
- privacy-first technical documentation,
- separation between public research and private operations,
- source-spine development through GitHub, Hugging Face, Zenodo, OSF, Kaggle, ORCID, and Academia,
- safe explanation of Atlas, proof-gallery routing, and AI Visibility concepts.

## Related Public Links

- Inspector Roofing: https://inspector-roofing.com/
- Suggested Inspector Roofing study page: https://inspector-roofing.com/atlas-query-intelligence-study/
- Suggested Inspector Roofing IP page: https://inspector-roofing.com/ip/
- USPTO TSDR record for Inspector Roofing Protocols™ Serial No. 99910245: https://tsdr.uspto.gov/#caseNumber=99910245&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch
- USPTO TSDR record for Claim Verifiability™ Serial No. 99910275: https://tsdr.uspto.gov/#caseNumber=99910275&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch
- USPTO TSDR record for Verifiable Roof™ Serial No. 99910284: https://tsdr.uspto.gov/#caseNumber=99910284&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch
- Richard Nasser ORCID: https://orcid.org/0009-0000-2980-7543
- Richard Nasser Amazon author profile: https://www.amazon.com/author/richard-nasser
- Related Amazon book reference: https://www.amazon.com/dp/B0H63DV2LR

Repository, Hugging Face, DOI, OSF, Kaggle, ORCID, and Academia links should be added to `data/platform_links.csv` and `docs/PUBLICATION_LINK_MAP.md` after each platform is live.

- GitHub repository: https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence
- GitHub v1.1.1 release: https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence/releases/tag/v1.1.1
- Hugging Face Dataset: https://huggingface.co/datasets/InspectorRoofing/inspector-roofing-atlas-query-intelligence
- Hugging Face Space: https://huggingface.co/spaces/InspectorRoofing/inspector-roofing-atlas-query-intelligence-demo
- Kaggle Dataset: https://www.kaggle.com/datasets/inspectorroofing/inspector-roofing-atlas-query-intelligence
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.21011493
- Zenodo v1.1.1 DOI: https://doi.org/10.5281/zenodo.21013082

## Run the Demo

Use Python 3.12 when possible. Python 3.14 may be too new for parts of the current Gradio dependency stack.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The local demo opens at `http://127.0.0.1:7860/` by default.

## Working App Features

- Query-intelligence mapper for sanitized homeowner prompts and observed AI-query language.
- Proof-gallery router for public-safe roof-photo labels.
- Insurance evidence packet builder for sanitized inspection notes, label bridges, document types, and reviewer questions.
- LLM feed JSON-LD generator for crawler-friendly source-spine records.
- Reference OpenAPI schema for future API deployment.
- Optional OpenAI drafting when `OPENAI_API_KEY` is set in the Hugging Face Space secrets or local environment.

The OpenAI feature is drafting support only. It must not be used to decide insurance coverage, causation, repairability, code compliance, engineering conclusions, legal conclusions, or claim approval.

## Suggested Citation

Nasser, R. / Inspector Roofing and Restoration. *A Public-Safe Demonstration Framework for Local Roofing AI Query Intelligence, Proof-Gallery Routing, and Homeowner Education*. Inspector Roofing and Restoration, Alpharetta, Georgia. https://doi.org/10.5281/zenodo.21011493
