# Publishing Guide

## GitHub

1. Create a new repository, suggested name:
   `inspector-roofing-atlas-query-intelligence`
2. Upload the full folder contents.
3. Keep the repository public only if no private customer files, images, keys, or manifests are added.
4. Add repository topics:
   `local-seo`, `ai-visibility`, `query-intelligence`, `information-retrieval`, `roof-inspection`, `privacy-preserving-data`.

## Hugging Face Dataset

1. Create a new Dataset repo under `InspectorRoofing`.
2. Upload `README.md`, `dataset.json`, `data/`, `schema/`, `docs/`, `CITATION.cff`, and `LICENSE`.
3. Keep the YAML front matter at the absolute top of `README.md`.
4. Do not upload private image manifests or customer photos.

## Hugging Face Space

1. Create a new Space under `InspectorRoofing`.
2. Choose Gradio.
3. Upload `app.py`, `requirements.txt`, `dataset.json`, `data/`, and `README.md`.
4. Confirm the app opens and both tabs run.

## Zenodo

1. Link the GitHub repository to Zenodo or upload the release zip manually.
2. Use resource type `Technical Report` or `Project Deliverable`.
3. Use the abstract in `docs/ZENODO_ACADEMIA_ABSTRACT.md`.
4. Use keywords:
   `Generative Engine Optimization`, `Local Search Architecture`, `Local SEO Entity Graphs`, `Information Retrieval`, `Roof Inspection Documentation`, `AI Visibility`, `Privacy-Preserving Data`.

## Important Boundary

Do not publish:

- private customer records,
- exact customer addresses,
- claim numbers,
- receipts,
- contracts,
- faces,
- license plates,
- API keys,
- full photo manifests,
- private storage paths,
- proprietary scoring rules,
- private WordPress plugin code.
