"""
RAG Engine — ChromaDB-backed retrieval-augmented generation.

Pipeline:
  1. Ingest documents from a directory
  2. Chunk text
  3. Embed with sentence-transformers
  4. Store in ChromaDB
  5. Similarity search at query time → return top-k context chunks
"""

import os
from typing import Optional

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("[RAGEngine] chromadb not installed. RAG features disabled.")

try:
    from sentence_transformers import SentenceTransformer
    ST_AVAILABLE = True
except ImportError:
    ST_AVAILABLE = False
    print("[RAGEngine] sentence-transformers not installed. RAG features disabled.")

from rag.ingestion import load_documents, chunk_text


EMBED_MODEL = "all-MiniLM-L6-v2"   # fast, small, good quality
COLLECTION_NAME = "project_knowledge"


class RAGEngine:
    """
    Manages the ChromaDB collection and provides similarity search.
    Falls back gracefully when dependencies are missing.
    """

    def __init__(self, persist_dir: str = "./chroma_db"):
        self.available = CHROMA_AVAILABLE and ST_AVAILABLE
        self.persist_dir = persist_dir
        self._client = None
        self._collection = None
        self._embedder = None

        if self.available:
            self._init_chroma()
            # Lazy load embedder in background so UI opens immediately
            import threading
            threading.Thread(target=self._init_embedder, daemon=True).start()

    # ------------------------------------------------------------------ #
    #  Setup                                                               #
    # ------------------------------------------------------------------ #

    def _init_chroma(self):
        self._client = chromadb.PersistentClient(path=self.persist_dir)
        self._collection = self._client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        print(f"[RAGEngine] ChromaDB ready at '{self.persist_dir}' "
              f"({self._collection.count()} docs)")

    def _init_embedder(self):
        print(f"[RAGEngine] Loading embedding model '{EMBED_MODEL}'...")
        self._embedder = SentenceTransformer(EMBED_MODEL)
        print("[RAGEngine] Embedding model ready.")

    # ------------------------------------------------------------------ #
    #  Ingestion                                                           #
    # ------------------------------------------------------------------ #

    def ingest_directory(self, directory: str):
        """Load all documents from a directory and store in ChromaDB."""
        if not self.available:
            print("[RAGEngine] Dependencies missing — skipping ingestion.")
            return

        docs = load_documents(directory)
        if not docs:
            print("[RAGEngine] No documents found.")
            return

        all_chunks, all_ids, all_metas = [], [], []

        for doc in docs:
            chunks = chunk_text(doc["content"])
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc['id']}::chunk_{i}"
                all_chunks.append(chunk)
                all_ids.append(chunk_id)
                all_metas.append({"source": doc["source"], "doc_id": doc["id"]})

        # Embed in batches of 64
        batch_size = 64
        for i in range(0, len(all_chunks), batch_size):
            batch_chunks = all_chunks[i : i + batch_size]
            batch_ids    = all_ids[i : i + batch_size]
            batch_metas  = all_metas[i : i + batch_size]
            embeddings   = self._embedder.encode(batch_chunks).tolist()

            self._collection.upsert(
                ids=batch_ids,
                documents=batch_chunks,
                embeddings=embeddings,
                metadatas=batch_metas,
            )

        print(f"[RAGEngine] Ingested {len(all_chunks)} chunks from {len(docs)} documents.")

    # ------------------------------------------------------------------ #
    #  Query                                                               #
    # ------------------------------------------------------------------ #

    def query(self, text: str, n_results: int = 3) -> list[str]:
        """
        Embed the query and return the top-k most similar document chunks.

        Returns:
            List of text chunks (empty list if RAG unavailable or no results).
        """
        if not self.available or self._embedder is None or self._collection.count() == 0:
            return []

        query_embedding = self._embedder.encode([text]).tolist()
        results = self._collection.query(
            query_embeddings=query_embedding,
            n_results=min(n_results, self._collection.count()),
        )

        documents = results.get("documents", [[]])[0]
        return [doc for doc in documents if doc]

    def document_count(self) -> int:
        if not self.available or self._collection is None:
            return 0
        return self._collection.count()

    def clear(self):
        """Delete all documents from the collection."""
        if self.available and self._client:
            self._client.delete_collection(COLLECTION_NAME)
            self._collection = self._client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
            print("[RAGEngine] Knowledge base cleared.")
