# ORCID Work Update Notes

ORCID profile:

https://orcid.org/0009-0000-2980-7543

## Works To Add

Use `data/orcid_works.bib` for a manual BibTeX import, or use `data/orcid_works.json` as the canonical project list for API mapping.

1. Technical report
2. Hugging Face public-safe dataset
3. Hugging Face Gradio demo
4. GitHub source repository

## Manual ORCID Path

1. Open the ORCID profile.
2. Go to Works.
3. Add works using BibTeX import.
4. Upload `data/orcid_works.bib`.
5. Review each work title, type, year, and URL.
6. Save.

## API Boundary

ORCID write access requires OAuth authorization with permission to update activities/works. The public ORCID read API can verify a record, but adding works requires an authorized token for the profile. Do not share an ORCID password. Use an OAuth token if API publishing is needed.
