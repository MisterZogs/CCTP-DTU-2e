"""
Indexe les CCTPs exemples (PDFs) dans une collection ChromaDB séparée.
Usage: python scripts/index_exemples.py [--force]

Les CCTPs exemples servent de few-shot context dans les prompts de génération.
"""
import argparse
import re
import sys
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

sys.path.insert(0, str(Path(__file__).parent.parent))

EXAMPLES_DIR = Path(__file__).parent.parent / "cctp-gauthier"
CHROMA_DIR = str(Path(__file__).parent.parent / "chroma_data")
COLLECTION_NAME = "cctp_exemples"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Mots-clés extraits du TITRE du CCTP (ligne "CCTP LOT N°X <NOM>")
TITLE_TO_LOT: list[tuple[str, str]] = [
    ("peinture",                     "peinture"),
    ("plâtrerie",                    "platrerie"),
    ("platrerie",                    "platrerie"),
    ("carrelage",                    "carrelage"),
    ("faïence",                      "carrelage"),
    ("menuiserie ext",               "menuiseries_ext"),
    ("menuiseries ext",              "menuiseries_ext"),
    ("aluminium",                    "menuiseries_ext"),
    ("menuiserie et aménagement",    "menuiseries_bois"),
    ("menuiserie et amenagement",    "menuiseries_bois"),
    ("menuiserie bois",              "menuiseries_bois"),
    ("aménagement bois",             "menuiseries_bois"),
    ("amenagement bois",             "menuiseries_bois"),
    ("menuiserie int",               "menuiseries_int"),
    ("menuiseries int",              "menuiseries_int"),
    ("gros œuvre",                   "gros_oeuvre"),
    ("maçonnerie",                   "gros_oeuvre"),
    ("plomberie",                    "plomberie"),
    ("chauffage",                    "chauffage_cvc"),
    ("électricité",                  "electricite"),
    ("electricite",                  "electricite"),
    ("cloison",                      "platrerie"),
    ("doublage",                     "platrerie"),
]


def detect_lot(text: str) -> str:
    """Détecte le lot depuis la ligne de titre 'CCTP LOT N°X <NOM>'."""
    # Cherche la ligne de titre du CCTP
    title_match = re.search(
        r"CCTP\s+LOT\s+N[°O]?\s*\d+\s+(.+)",
        text,
        re.IGNORECASE,
    )
    search_text = title_match.group(1).lower() if title_match else text[:500].lower()

    for keyword, lot_key in TITLE_TO_LOT:
        if keyword in search_text:
            return lot_key
    return "inconnu"


def detect_lot_number(text: str) -> str:
    match = re.search(r"lot\s*n[°o]?\s*(\d+)", text, re.IGNORECASE)
    return match.group(1) if match else "?"


def split_into_sections(text: str) -> list[dict]:
    """Découpe le texte en sections par chapitres numérotés."""
    pattern = re.compile(r"\n\s*(\d+[\).]?\s+[A-ZÉÈÀÂ][^\n]{5,})\n", re.MULTILINE)
    sections = []
    positions = list(pattern.finditer(text))

    for i, match in enumerate(positions):
        title = match.group(1).strip()
        start = match.end()
        end = positions[i + 1].start() if i + 1 < len(positions) else len(text)
        content = text[start:end].strip()
        if len(content) > 100:
            sections.append({"title": title, "content": content})

    if not sections:
        chunk_size = 1500
        for j in range(0, len(text), chunk_size):
            chunk = text[j : j + chunk_size].strip()
            if chunk:
                sections.append({"title": f"Extrait {j // chunk_size + 1}", "content": chunk})

    return sections


def index_examples(force: bool = False) -> int:
    try:
        import pdfplumber
    except ImportError:
        print("pdfplumber non installé. Lance: pip install pdfplumber")
        sys.exit(1)

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    if collection.count() > 0 and not force:
        print(f"Collection '{COLLECTION_NAME}' déjà remplie ({collection.count()} chunks). Utilise --force pour réindexer.")
        return collection.count()

    if force and collection.count() > 0:
        collection.delete(ids=collection.get()["ids"])
        print("Collection vidée pour réindexation.")

    pdf_files = list(EXAMPLES_DIR.glob("*.pdf")) + list(EXAMPLES_DIR.glob("*.PDF"))
    if not pdf_files:
        print(f"Aucun PDF trouvé dans {EXAMPLES_DIR}")
        return 0

    ids, documents, metadatas = [], [], []

    for pdf_path in sorted(pdf_files):
        print(f"  Traitement: {pdf_path.name}")
        with pdfplumber.open(pdf_path) as pdf:
            full_text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

        lot_key = detect_lot(full_text)
        lot_num = detect_lot_number(full_text)
        sections = split_into_sections(full_text)

        for i, section in enumerate(sections):
            doc_id = f"exemple_{pdf_path.stem}_{i}"
            content = (
                f"[EXEMPLE CCTP RÉEL — LOT {lot_num} — {lot_key.upper()}]\n"
                f"Section: {section['title']}\n\n"
                f"{section['content']}"
            )
            ids.append(doc_id)
            documents.append(content)
            metadatas.append({
                "source": pdf_path.name,
                "lot_key": lot_key,
                "lot_numero": lot_num,
                "section": section["title"],
                "type": "exemple_reel",
            })

        print(f"    → Lot {lot_num} ({lot_key}), {len(sections)} sections")

    if ids:
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        print(f"\nIndexation terminée : {len(ids)} chunks dans '{COLLECTION_NAME}'")

    return len(ids)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexe les CCTPs exemples en PDF")
    parser.add_argument("--force", action="store_true", help="Réindexe même si déjà fait")
    args = parser.parse_args()

    print(f"Indexation des CCTPs exemples depuis {EXAMPLES_DIR}")
    count = index_examples(force=args.force)
    print(f"Total: {count} chunks indexés")
