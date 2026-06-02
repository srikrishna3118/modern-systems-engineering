from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    source: str
    text: str


def load_documents(docs_dir: str) -> list[Document]:
    base = Path(docs_dir)
    if not base.exists() or not base.is_dir():
        raise FileNotFoundError(f"docs dir not found: {docs_dir}")

    documents: list[Document] = []
    for path in sorted(base.rglob("*")):
        if path.is_dir():
            continue
        if path.suffix.lower() not in {".txt", ".md"}:
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        documents.append(Document(source=str(path.relative_to(base)), text=text))
    return documents
