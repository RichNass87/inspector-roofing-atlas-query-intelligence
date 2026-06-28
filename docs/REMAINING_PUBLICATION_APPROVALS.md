# Remaining Publication Approvals

GitHub and Hugging Face are live. The remaining platforms require either API tokens or final browser upload approval.

## Live Links

- GitHub repo: https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence
- GitHub release: https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence/releases/tag/v1.0.1
- Hugging Face Dataset: https://huggingface.co/datasets/InspectorRoofing/inspector-roofing-atlas-query-intelligence
- Hugging Face Space: https://huggingface.co/spaces/InspectorRoofing/inspector-roofing-atlas-query-intelligence-demo
- Kaggle Dataset: https://www.kaggle.com/datasets/inspectorroofing/inspector-roofing-atlas-query-intelligence
- ORCID: https://orcid.org/0009-0000-2980-7543
- Inspector Roofing: https://inspector-roofing.com/
- Amazon Author: https://www.amazon.com/author/richard-nasser
- Amazon Book: https://www.amazon.com/dp/B0H63DV2LR

## Files To Upload

- Release zip: `/Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.0.1.zip`
- Technical report PDF: `/Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.0.1/docs/inspector-roofing-atlas-query-intelligence-technical-report-v1.0.1.pdf`

## Zenodo DOI

Option A - manual upload:

1. Open https://zenodo.org/uploads/new
2. Upload the release zip and technical report PDF.
3. Use metadata from `.zenodo.json`.
4. Resource type: publication / technical note.
5. Publish to create the DOI.
6. Add the DOI URL to `data/platform_links.csv`, `docs/PUBLICATION_LINK_MAP.md`, README, GitHub release notes, and Hugging Face Dataset README.

Option B - API:

1. Create a Zenodo access token.
2. Run:

```bash
cd /Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.0.1
ZENODO_ACCESS_TOKEN="paste-token-here" ZENODO_PUBLISH=1 python3 scripts/zenodo_publish.py
```

## Kaggle

Published:

https://www.kaggle.com/datasets/inspectorroofing/inspector-roofing-atlas-query-intelligence

To publish a later version:

```bash
python3 -m pip install --user kaggle
cd /Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.0.1
KAGGLE_MODE=version bash scripts/kaggle_publish.sh
```

The script builds a public-safe staging folder at `build/platform-upload`, writes Kaggle's required `datasets-metadata.json`, and versions the existing Kaggle dataset automatically when possible. To force a mode:

```bash
KAGGLE_MODE=version bash scripts/kaggle_publish.sh
KAGGLE_MODE=create bash scripts/kaggle_publish.sh
```

## OSF

Manual path:

1. Open https://osf.io/dashboard
2. Create a project named `Inspector Roofing Atlas Query Intelligence Public-Safe Framework`.
3. Use `docs/OSF_PROJECT_DESCRIPTION.md`.
4. Upload the release zip and PDF.
5. Link to GitHub, Hugging Face Dataset, Hugging Face Space, Amazon Author, and Inspector Roofing.

CLI path after project creation:

```bash
cd /Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.0.1
OSF_PROJECT_ID="paste-project-id" bash scripts/osf_publish.sh
```

The OSF script uploads the release zip, report PDF, OSF description, platform links, project inventory, and ORCID BibTeX from the public-safe staging folder.

## ORCID

Manual path:

1. Open https://orcid.org/0009-0000-2980-7543
2. Go to Works.
3. Import BibTeX from `data/orcid_works.bib`.
4. Confirm the technical report, Hugging Face dataset, Hugging Face Space demo, and GitHub source repository.

API path requires an ORCID OAuth token with activity/work update permission. Do not use or share a password.

## Academia.edu

1. Open https://www.academia.edu/
2. Upload the technical report PDF.
3. Use `docs/ACADEMIA_UPLOAD_NOTES.md`.
4. Add DOI after Zenodo is live.

## Website Update

After Zenodo DOI is live, add the final source-spine links to a public Inspector Roofing authority/research page:

- GitHub repo
- GitHub release
- Hugging Face Dataset
- Hugging Face Space
- Zenodo DOI
- OSF
- Kaggle
- Academia
- Amazon Author
- Amazon Book
