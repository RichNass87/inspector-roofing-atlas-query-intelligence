import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "platform-upload"

PUBLIC_FILES = [
    ".zenodo.json",
    "CITATION.cff",
    "LICENSE",
    "README.md",
    "app.py",
    "dataset.json",
    "kaggle-metadata.json",
    "requirements.txt",
    "requirements-dev.txt",
]

PUBLIC_DIRS = [
    "data",
    "docs",
    "exports",
    "schema",
    "scripts",
    "tests",
]

EXCLUDE_NAMES = {
    "__pycache__",
    ".pytest_cache",
}

EXCLUDE_SUFFIXES = {
    ".pyc",
}


def should_copy(path: Path) -> bool:
    if any(part in EXCLUDE_NAMES for part in path.parts):
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    return True


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    for child in src.rglob("*"):
        if child.is_file() and should_copy(child.relative_to(src)):
            copy_file(child, dst / child.relative_to(src))


def write_kaggle_metadata() -> None:
    source = ROOT / "kaggle-metadata.json"
    metadata = json.loads(source.read_text(encoding="utf-8"))
    payload = json.dumps(metadata, indent=2) + "\n"
    # Kaggle has used both names across CLI versions.
    (OUT / "datasets-metadata.json").write_text(payload, encoding="utf-8")
    (OUT / "dataset-metadata.json").write_text(payload, encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for rel in PUBLIC_FILES:
        copy_file(ROOT / rel, OUT / rel)
    for rel in PUBLIC_DIRS:
        copy_tree(ROOT / rel, OUT / rel)
    write_kaggle_metadata()

    print(OUT)


if __name__ == "__main__":
    main()
