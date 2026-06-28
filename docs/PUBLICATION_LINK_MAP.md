# Publication Link Map

Use this file as the source-spine checklist after each platform is published.

## Canonical Project

- Primary business website: https://inspector-roofing.com/
- Local demo when running on this Mac: http://127.0.0.1:7860/
- Suggested GitHub repository: `inspector-roofing-atlas-query-intelligence`
- Suggested Hugging Face dataset: `InspectorRoofing/inspector-roofing-atlas-query-intelligence`
- Suggested Hugging Face Space: `InspectorRoofing/inspector-roofing-atlas-query-intelligence-demo`

## Platform Targets

| Platform | Purpose | Status | Final URL |
| --- | --- | --- | --- |
| GitHub | Source code, schemas, dataset samples, validation | Pending publish |  |
| Hugging Face Dataset | Dataset card, sanitized query-intel records, public taxonomy | Pending publish |  |
| Hugging Face Space | Gradio public demo | Pending publish |  |
| Zenodo | DOI for technical report / release archive | Pending DOI |  |
| OSF | Research project mirror and citation context | Pending publish |  |
| Kaggle | Optional dataset mirror | Pending publish |  |
| Academia.edu | Technical-report PDF and abstract | Pending upload |  |
| Amazon Author | Richard Nasser author profile | Live public reference | https://www.amazon.com/author/richard-nasser |
| Amazon Book | Related source-spine book reference | Live public reference | https://www.amazon.com/dp/B0H63DV2LR |

## Link Rules

- GitHub should link to Hugging Face Dataset, Hugging Face Space, Zenodo DOI, Inspector Roofing, and Amazon only after those URLs are live.
- Hugging Face Dataset should link back to GitHub, Zenodo DOI, and Inspector Roofing.
- Hugging Face Space should link to the Dataset and GitHub.
- Zenodo should cite the GitHub release archive and include the technical-report PDF.
- Academia.edu should upload the PDF and link to the DOI once Zenodo is live.
- Kaggle and OSF should mirror the same public-safe files only.
- Amazon should use the author profile plus final book/product URLs only. Do not use a search URL as the canonical Amazon reference.

## Public-Safety Rule

Only publish the sanitized release package. Do not upload virtual environments, private customer photos, full photo manifests, exact customer addresses, claim records, receipts, contracts, API keys, or private WordPress plugin logic.
