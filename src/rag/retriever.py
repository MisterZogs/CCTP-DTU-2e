from src.rag.indexer import get_collection, get_examples_collection
from src.config import settings


def retrieve_dtu_context(lot_key: str, query: str, n_results: int | None = None) -> str:
    """Retourne le contexte DTU + les exemples CCTP réels pour un lot donné."""
    n = n_results or settings.rag_n_results

    dtu_context = _query_collection(get_collection(), query, n)
    examples_context = _query_examples(lot_key, query, n_results=2)

    parts = []
    if dtu_context:
        parts.append("## Extraits base réglementaire DTU\n\n" + dtu_context)
    if examples_context:
        parts.append("## Exemples CCTP réels (architecture)\n\n" + examples_context)

    return "\n\n" + "\n\n---\n\n".join(parts) if parts else ""


def _query_collection(collection, query: str, n: int) -> str:
    if collection.count() == 0:
        return ""
    results = collection.query(
        query_texts=[query],
        n_results=min(n, collection.count()),
    )
    docs = results["documents"][0] if results["documents"] else []
    return "\n\n---\n\n".join(docs)


def _query_examples(lot_key: str, query: str, n_results: int = 2) -> str:
    collection = get_examples_collection()
    if collection.count() == 0:
        return ""

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
        where={"lot_key": lot_key} if lot_key != "inconnu" else None,
    )
    docs = results["documents"][0] if results["documents"] else []

    # Fallback sans filtre lot si aucun résultat
    if not docs and lot_key != "inconnu":
        results = collection.query(
            query_texts=[query],
            n_results=min(n_results, collection.count()),
        )
        docs = results["documents"][0] if results["documents"] else []

    return "\n\n---\n\n".join(docs)
