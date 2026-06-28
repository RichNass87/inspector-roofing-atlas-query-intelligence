# All Projects Platform Rollout

This inventory keeps the public source-spine projects coordinated across GitHub, ORCID, Kaggle, OSF, Zenodo, Hugging Face, Academia, Amazon, and Inspector Roofing.

## Current Public Project Count

- Public GitHub repos found under `RichNass87`: 14
- ORCID profile checked: https://orcid.org/0009-0000-2980-7543
- Public ORCID work groups currently visible: 10
- Current package-ready project: `inspector-roofing-atlas-query-intelligence`

## Files

- Project inventory: `data/public_project_inventory.csv`
- Current ORCID import file: `data/orcid_works.bib`
- Current ORCID structured work file: `data/orcid_works.json`
- Kaggle publish helper: `scripts/kaggle_publish.sh`
- OSF upload helper: `scripts/osf_publish.sh`

## Platform Rules

- GitHub remains the source of truth for source code and release assets.
- ORCID should list scholarly/report/software/dataset works, not every tiny operational file.
- Kaggle should be used for sanitized datasets only, not private images, claim data, customer details, or plugin internals.
- OSF should mirror the public-safe report, release zip, schemas, and public metadata.
- Zenodo should be the DOI anchor for stable release archives and reports.
- Hugging Face should carry runnable demos and dataset cards.

## Next Project-Wide Cleanup Order

1. Keep the current Atlas Query Intelligence Kaggle mirror versioned at https://www.kaggle.com/datasets/inspectorroofing/inspector-roofing-atlas-query-intelligence.
2. Create or select the matching OSF project, then run `OSF_PROJECT_ID="..." bash scripts/osf_publish.sh`.
3. Import `data/orcid_works.bib` into ORCID for the current Atlas Query Intelligence package.
4. Review `data/public_project_inventory.csv` and decide which remaining projects deserve Kaggle/OSF mirrors versus ORCID-only work entries.
5. Add final Kaggle, OSF, ORCID, Zenodo DOI, and Academia URLs back into `data/platform_links.csv`, `docs/PUBLICATION_LINK_MAP.md`, README, GitHub release notes, and Hugging Face.

## Credential Boundary

Publishing cannot be completed from this repo without platform authorization:

- Kaggle requires `~/.kaggle/kaggle.json` for future version uploads.
- OSF requires `osf init`, `~/.osfcli.config`, or an authenticated environment.
- ORCID writes require OAuth work-update permission.

Do not share passwords. Use API tokens or the platform's approved OAuth flow.
