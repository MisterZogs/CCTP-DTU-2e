from src.rag.indexer import get_collection
from src.config import settings


def retrieve_dtu_context(lot_key: str, query: str, n_results: int | None = None) -> str:
    collection = get_collection()
    n = n_results or settings.rag_n_results

    results = collection.query(
        query_texts=[query],
        n_results=min(n, collection.count()),
    )

    docs = results["documents"][0] if results["documents"] else []
    return "\n\n---\n\n".join(docs)
