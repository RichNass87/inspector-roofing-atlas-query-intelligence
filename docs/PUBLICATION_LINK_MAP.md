# Publication Link Map

Use this file as the source-spine checklist after each platform is published.

## Canonical Project

- Primary business website: https://inspector-roofing.com/
- Suggested public study page: https://inspector-roofing.com/atlas-query-intelligence-study/
- Suggested public IP page: https://inspector-roofing.com/ip/
- USPTO TSDR record for Inspector Roofing Protocols™ Serial No. 99910245: https://tsdr.uspto.gov/#caseNumber=99910245&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch
- Local demo when running on this Mac: http://127.0.0.1:7860/
- Suggested GitHub repository: `inspector-roofing-atlas-query-intelligence`
- Suggested Hugging Face dataset: `InspectorRoofing/inspector-roofing-atlas-query-intelligence`
- Suggested Hugging Face Space: `InspectorRoofing/inspector-roofing-atlas-query-intelligence-demo`

## Platform Targets

| Platform | Purpose | Status | Final URL |
| --- | --- | --- | --- |
| Inspector Roofing Study Page | Website authority hub for the public-safe study and source-spine links | Ready to publish | https://inspector-roofing.com/atlas-query-intelligence-study/ |
| Inspector Roofing IP Page | Legal and research verification hub | Ready to publish | https://inspector-roofing.com/ip/ |
| USPTO TSDR | Pending trademark application verification for Inspector Roofing Protocols™ Serial No. 99910245 | Live | https://tsdr.uspto.gov/#caseNumber=99910245&caseSearchType=US_APPLICATION&caseType=DEFAULT&searchType=statusSearch |
| GitHub | Source code, schemas, dataset samples, validation | Live | https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence |
| GitHub Release | Versioned v1.1.1 archive and PDF assets | Live | https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence/releases/tag/v1.1.1 |
| Hugging Face Dataset | Dataset card, sanitized query-intel records, public taxonomy | Live | https://huggingface.co/datasets/InspectorRoofing/inspector-roofing-atlas-query-intelligence |
| Hugging Face Space | Gradio public demo | Live | https://huggingface.co/spaces/InspectorRoofing/inspector-roofing-atlas-query-intelligence-demo |
| ORCID | Richard Nasser researcher identifier and works list | Ready for work import | https://orcid.org/0009-0000-2980-7543 |
| Zenodo | DOI for technical report / release archive | Live | https://doi.org/10.5281/zenodo.21011493 |
| OSF | Research project mirror and citation context | Needs OSF review | https://osf.io/pqvwf/ |
| Kaggle | Public-safe dataset mirror | Live | https://www.kaggle.com/datasets/inspectorroofing/inspector-roofing-atlas-query-intelligence |
| Academia.edu | Technical-report PDF and abstract | Pending upload |  |
| Amazon Author | Richard Nasser author profile | Live public reference | https://www.amazon.com/author/richard-nasser |
| Amazon Book | Related source-spine book reference | Live public reference | https://www.amazon.com/dp/B0H63DV2LR |

Project-wide cleanup inventory: `data/public_project_inventory.csv`.

## Link Rules

- GitHub should link to Hugging Face Dataset, Hugging Face Space, Zenodo DOI, Inspector Roofing, and Amazon only after those URLs are live.
- The Inspector Roofing study page should link to the public dataset, demo, GitHub release, ORCID profile, Amazon references, and final DOI/mirror URLs as they go live.
- The Inspector Roofing IP page should link to the USPTO TSDR record, Zenodo DOI, GitHub, Hugging Face, Kaggle, ORCID, and Amazon references.
- Hugging Face Dataset should link back to GitHub, Zenodo DOI, and Inspector Roofing.
- Hugging Face Space should link to the Dataset and GitHub.
- Zenodo should cite the GitHub release archive and include the technical-report PDF.
- ORCID should list the technical report, public-safe dataset, demo app, and source repository using `data/orcid_works.bib`.
- Academia.edu should upload the PDF and link to the DOI once Zenodo is live.
- Kaggle and OSF should mirror the same public-safe files only. OSF project `pqvwf` needs platform review/restoration before it should be used publicly.
- Amazon should use the author profile plus final book/product URLs only. Do not use a search URL as the canonical Amazon reference.

## Public-Safety Rule

Only publish the sanitized release package. Do not upload virtual environments, private customer photos, full photo manifests, exact customer addresses, claim records, receipts, contracts, API keys, or private WordPress plugin logic.
