from __future__ import annotations

import json
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from src.config import settings

_client = None
_collection = None
_examples_collection = None


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return _client


def _get_embedding_function():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=settings.embedding_model
    )


def get_collection():
    global _collection
    if _collection is not None:
        return _collection

    client = _get_client()
    ef = _get_embedding_function()
    _collection = client.get_or_create_collection(
        name="dtu_knowledge_base",
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )
    return _collection


def get_examples_collection():
    global _examples_collection
    if _examples_collection is not None:
        return _examples_collection

    client = _get_client()
    ef = _get_embedding_function()
    _examples_collection = client.get_or_create_collection(
        name="cctp_exemples",
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )
    return _examples_collection


def index_knowledge_base(force: bool = False) -> int:
    collection = get_collection()

    if collection.count() > 0 and not force:
        return collection.count()

    kb_dir = Path(__file__).parent.parent / "knowledge_base"
    ids, documents, metadatas = [], [], []

    for json_file in sorted(kb_dir.glob("*.json")):
        with open(json_file, encoding="utf-8") as f:
            dtu_list = json.load(f)

        for dtu in dtu_list:
            for i, point in enumerate(dtu.get("points_cles", [])):
                doc_id = f"{json_file.stem}__{dtu['reference'].replace(' ', '_')}_{i}"
                content = (
                    f"DTU: {dtu['reference']} — {dtu['titre']}\n"
                    f"Édition: {dtu.get('date_edition', '')} | Statut: {dtu.get('statut', '')}\n"
                    f"Article {point.get('article', '')} — {point.get('sujet', '')}\n"
                    f"{point.get('contenu', '')}\n"
                    f"Exigences: {'; '.join(point.get('exigences', []))}"
                )
                ids.append(doc_id)
                documents.append(content)
                metadatas.append({
                    "reference": dtu["reference"],
                    "titre": dtu["titre"],
                    "lots": ",".join(dtu.get("lots_concernes", [])),
                    "article": str(point.get("article", "")),
                    "statut": dtu.get("statut", ""),
                })

    if ids:
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    return len(ids)
