from pathlib import Path

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge_base"

LOT_TO_FILES: dict[str, list[str]] = {
    "gros_oeuvre":      ["dtu_gros_oeuvre.json"],
    "charpente_bois":   ["dtu_charpente.json"],
    "couverture":       ["dtu_charpente.json"],
    "menuiseries_ext":  ["dtu_menuiseries_ext.json"],
    "menuiseries_int":  [],
    "isolation":        ["dtu_cvc.json"],
    "cloisons":         [],
    "revetements_sol":  ["dtu_cvc.json"],
    "carrelage":        [],
    "peinture":         [],
    "plomberie":        [],
    "chauffage_cvc":    ["dtu_cvc.json"],
    "electricite":      ["dtu_electricite.json"],
    "vrd":              [],
}

LOT_TO_DTU_REFS: dict[str, list[str]] = {
    "gros_oeuvre":     ["NF DTU 20.1", "NF DTU 13.1", "NF DTU 13.2", "NF DTU 13.3"],
    "charpente_bois":  ["NF DTU 31.1", "NF DTU 31.2", "NF EN 1995-1-1 (Eurocode 5)"],
    "couverture":      ["NF DTU 40.1", "NF DTU 40.21", "NF DTU 40.35", "NF DTU 43.1"],
    "menuiseries_ext": ["NF DTU 36.5", "NF EN 14351-1"],
    "menuiseries_int": ["NF DTU 36.2", "NF DTU 36.3"],
    "isolation":       ["NF DTU 55.2", "RE2020"],
    "cloisons":        ["NF DTU 25.41", "NF DTU 25.42"],
    "revetements_sol": ["NF DTU 51.1", "NF DTU 51.2", "NF DTU 52.1"],
    "carrelage":       ["NF DTU 52.2", "NF DTU 52.4"],
    "peinture":        ["NF DTU 59.1", "NF DTU 59.2"],
    "plomberie":       ["NF DTU 60.1", "NF DTU 60.11", "NF DTU 65.10"],
    "chauffage_cvc":   ["NF DTU 65.11", "NF DTU 65.14", "RE2020"],
    "electricite":     ["NF C 15-100", "NF C 14-100"],
    "vrd":             ["NF DTU 70.1", "NF EN 752"],
}

LOT_LABELS: dict[str, str] = {
    "gros_oeuvre":     "Gros Œuvre / Maçonnerie",
    "charpente_bois":  "Charpente Bois",
    "couverture":      "Couverture / Étanchéité",
    "menuiseries_ext": "Menuiseries Extérieures",
    "menuiseries_int": "Menuiseries Intérieures",
    "isolation":       "Isolation",
    "cloisons":        "Cloisons / Doublages / Faux-plafonds",
    "revetements_sol": "Revêtements de Sol",
    "carrelage":       "Carrelage / Faïence",
    "peinture":        "Peinture / Enduits",
    "plomberie":       "Plomberie / Sanitaires",
    "chauffage_cvc":   "Chauffage / VMC / Climatisation",
    "electricite":     "Électricité CFO/CFA",
    "vrd":             "VRD / Espaces Extérieurs",
}


def get_lot_label(lot_key: str) -> str:
    return LOT_LABELS.get(lot_key, lot_key)


def get_dtu_files(lot_key: str) -> list[Path]:
    filenames = LOT_TO_FILES.get(lot_key, [])
    return [KNOWLEDGE_BASE_DIR / f for f in filenames if (KNOWLEDGE_BASE_DIR / f).exists()]


def get_dtu_refs(lot_key: str) -> list[str]:
    return LOT_TO_DTU_REFS.get(lot_key, [])
