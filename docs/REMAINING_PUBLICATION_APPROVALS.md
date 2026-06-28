# Remaining Publication Approvals

GitHub, Hugging Face, Kaggle, Zenodo, and the v1.1.1 ORCID work entry are live. OSF and Academia are blocked by platform/account review, not by missing local files.

## Live Links

- GitHub repo: https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence
- GitHub release: https://github.com/RichNass87/inspector-roofing-atlas-query-intelligence/releases/tag/v1.1.1
- Hugging Face Dataset: https://huggingface.co/datasets/InspectorRoofing/inspector-roofing-atlas-query-intelligence
- Hugging Face Space: https://huggingface.co/spaces/InspectorRoofing/inspector-roofing-atlas-query-intelligence-demo
- Kaggle Dataset: https://www.kaggle.com/datasets/inspectorroofing/inspector-roofing-atlas-query-intelligence
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.21011493
- Zenodo v1.1.1 DOI: https://doi.org/10.5281/zenodo.21013082
- ORCID: https://orcid.org/0009-0000-2980-7543
- Inspector Roofing: https://inspector-roofing.com/
- Amazon Author: https://www.amazon.com/author/richard-nasser
- Amazon Book: https://www.amazon.com/dp/B0H63DV2LR

## Files To Upload

- Technical report PDF: `/Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.0.1/docs/inspector-roofing-atlas-query-intelligence-technical-report-v1.1.1.pdf`
- Public-safe upload folder can be rebuilt with `python3 scripts/build_platform_uploads.py`.

## Zenodo DOI

Published:

https://doi.org/10.5281/zenodo.21011493

Latest v1.1.1 version:

https://doi.org/10.5281/zenodo.21013082

Published record:

https://zenodo.org/records/21013082

Future version path:

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
cd /Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.1.1
ZENODO_ACCESS_TOKEN="paste-token-here" ZENODO_PUBLISH=1 python3 scripts/zenodo_publish.py
```

## Kaggle

Published:

https://www.kaggle.com/datasets/inspectorroofing/inspector-roofing-atlas-query-intelligence

To publish a later version:

```bash
python3 -m pip install --user kaggle
cd /Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.1.1
KAGGLE_MODE=version bash scripts/kaggle_publish.sh
```

The script builds a public-safe staging folder at `build/platform-upload`, writes Kaggle's required `datasets-metadata.json`, and versions the existing Kaggle dataset automatically when possible. To force a mode:

```bash
KAGGLE_MODE=version bash scripts/kaggle_publish.sh
KAGGLE_MODE=create bash scripts/kaggle_publish.sh
```

## OSF

Status:

https://osf.io/pqvwf/ was created, but OSF immediately flagged it for platform spam review before files could be uploaded. Do not create duplicate OSF projects. Restore this project through OSF support or the OSF account interface first, then upload the public-safe files.

Manual path:

1. Open https://osf.io/dashboard
2. Create a project named `Inspector Roofing Atlas Query Intelligence Public-Safe Framework`.
3. Use `docs/OSF_PROJECT_DESCRIPTION.md`.
4. Upload the release zip and PDF.
5. Link to GitHub, Hugging Face Dataset, Hugging Face Space, Amazon Author, and Inspector Roofing.

CLI path after project creation:

```bash
cd /Users/richardnasser/Documents/inspector-roofing-atlas-source-spine-v1.1.1
OSF_PROJECT_ID="paste-project-id" bash scripts/osf_publish.sh
```

The OSF script uploads the release zip, report PDF, OSF description, platform links, project inventory, and ORCID BibTeX from the public-safe staging folder.

## ORCID

Status:

The v1.1.1 technical report DOI was added to ORCID on 2026-06-28 through "Add work with a DOI".

- Profile: https://orcid.org/0009-0000-2980-7543
- DOI added: https://doi.org/10.5281/zenodo.21013082
- Works count after add: 11

Future optional cleanup:

1. Review whether the Hugging Face dataset, Hugging Face Space demo, and GitHub source repository should be added as separate ORCID works.
2. If yes, import selected entries from `data/orcid_works.bib`.

API path requires an ORCID OAuth token with activity/work update permission. Do not use or share a password.

## Academia.edu

Status:

Academia.edu shows: "Your account was flagged as suspicious, and your reconsideration request is awaiting manual review." Do not create a duplicate account or try to force uploads while this review is pending.

After the account is restored:

1. Upload the technical report PDF.
2. Use `docs/ACADEMIA_UPLOAD_NOTES.md`.
3. Include the v1.1.1 DOI: https://doi.org/10.5281/zenodo.21013082.

## Website Update

Published website research page:

https://inspector-roofing.com/atlas-query-intelligence-study/

No `/ip/` page was published from this repo after the user requested information only. The prepared copy remains in `docs/INSPECTOR_ROOFING_IP_PAGE.md` and `exports/inspector-roofing-legal-ip-page.html`.

The page should keep these source-spine links current:

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
