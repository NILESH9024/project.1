"""
Document Ingestion — reads files from the project knowledge base.
Supports: .txt, .md, .py, .js, .ts, .html, .css, .json, .csv, README
"""

import os
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts",
    ".html", ".css", ".json", ".csv",
    ".rst", ".yaml", ".yml", ".toml",
}


def load_documents(directory: str) -> list[dict]:
    """
    Recursively load all supported text files from a directory.

    Returns:
        List of {"id": str, "content": str, "source": str}
    """
    docs = []
    base = Path(directory)

    if not base.exists():
        print(f"[Ingestion] Directory not found: {directory}")
        return docs

    for path in base.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                if content.strip():
                    docs.append({
                        "id":      str(path.relative_to(base)),
                        "content": content,
                        "source":  str(path),
                    })
            except Exception as e:
                print(f"[Ingestion] Could not read {path}: {e}")

    print(f"[Ingestion] Loaded {len(docs)} documents from '{directory}'")
    return docs


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text:       Full document text.
        chunk_size: Approximate characters per chunk.
        overlap:    Characters to overlap between consecutive chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c.strip() for c in chunks if c.strip()]
