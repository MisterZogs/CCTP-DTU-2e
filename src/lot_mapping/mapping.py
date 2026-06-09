from pathlib import Path

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge_base"

LOT_TO_FILES: dict[str, list[str]] = {
    "gros_oeuvre":       ["dtu_gros_oeuvre.json"],
    "charpente_bois":    ["dtu_charpente.json"],
    "couverture":        ["dtu_charpente.json"],
    "menuiseries_ext":   ["dtu_menuiseries_ext.json"],
    "menuiseries_int":   ["dtu_menuiseries_bois.json"],
    "menuiseries_bois":  ["dtu_menuiseries_bois.json"],
    "isolation":         ["dtu_cvc.json"],
    "cloisons":          ["dtu_platrerie.json"],
    "platrerie":         ["dtu_platrerie.json"],
    "revetements_sol":   ["dtu_carrelage.json"],
    "carrelage":         ["dtu_carrelage.json"],
    "peinture":          ["dtu_peinture.json"],
    "plomberie":         [],
    "chauffage_cvc":     ["dtu_cvc.json"],
    "electricite":       ["dtu_electricite.json"],
    "vrd":               [],
}

LOT_TO_DTU_REFS: dict[str, list[str]] = {
    "gros_oeuvre":      ["NF DTU 20.1", "NF DTU 13.1", "NF DTU 13.2", "NF DTU 13.3"],
    "charpente_bois":   ["NF DTU 31.1", "NF DTU 31.2", "NF EN 1995-1-1 (Eurocode 5)"],
    "couverture":       ["NF DTU 40.1", "NF DTU 40.21", "NF DTU 40.35", "NF DTU 43.1"],
    "menuiseries_ext":  ["NF DTU 36.5", "NF EN 14351-1"],
    "menuiseries_int":  ["NF DTU 36.2", "NF DTU 36.3"],
    "menuiseries_bois": ["NF DTU 36.2", "NF EN 942", "NF B 52-001"],
    "isolation":        ["NF DTU 55.2", "RE2020"],
    "cloisons":         ["NF DTU 25.41", "NF DTU 25.42"],
    "platrerie":        ["NF DTU 25.41", "NF DTU 25.42"],
    "revetements_sol":  ["NF DTU 51.1", "NF DTU 51.2", "NF DTU 52.1"],
    "carrelage":        ["NF DTU 52.2", "NF DTU 52.4", "NF EN 14411", "NF EN 12004"],
    "peinture":         ["NF DTU 59.1", "NF DTU 59.2"],
    "plomberie":        ["NF DTU 60.1", "NF DTU 60.11", "NF DTU 65.10"],
    "chauffage_cvc":    ["NF DTU 65.11", "NF DTU 65.14", "RE2020"],
    "electricite":      ["NF C 15-100", "NF C 14-100"],
    "vrd":              ["NF DTU 70.1", "NF EN 752"],
}

LOT_LABELS: dict[str, str] = {
    "gros_oeuvre":      "Gros Œuvre / Maçonnerie",
    "charpente_bois":   "Charpente Bois",
    "couverture":       "Couverture / Étanchéité",
    "menuiseries_ext":  "Menuiseries Extérieures",
    "menuiseries_int":  "Menuiseries Intérieures",
    "menuiseries_bois": "Menuiserie et Aménagements Bois",
    "isolation":        "Isolation",
    "cloisons":         "Cloisons / Doublages / Faux-plafonds",
    "platrerie":        "Plâtrerie",
    "revetements_sol":  "Revêtements de Sol",
    "carrelage":        "Carrelage / Faïence",
    "peinture":         "Peinture / Enduits",
    "plomberie":        "Plomberie / Sanitaires",
    "chauffage_cvc":    "Chauffage / VMC / Climatisation",
    "electricite":      "Électricité CFO/CFA",
    "vrd":              "VRD / Espaces Extérieurs",
}

# Structure-type par lot (chapitres principaux), inspirée des CCTPs réels
LOT_STRUCTURE: dict[str, list[str]] = {
    "menuiseries_ext": [
        "0) Généralités — Présentation et documents de référence",
        "1) Menuiseries aluminium — Dépose et pose",
        "2) Stores et protections solaires",
        "3) Grilles et volets de sécurité",
        "4) Études, levage, approvisionnement, DOE",
    ],
    "platrerie": [
        "0) Généralités — Présentation et documents de référence",
        "1) Doublages",
        "2) Cloisons de distribution",
        "3) Plafonds",
        "4) Divers",
    ],
    "cloisons": [
        "0) Généralités — Présentation et documents de référence",
        "1) Doublages",
        "2) Cloisons de distribution",
        "3) Plafonds",
        "4) Divers",
    ],
    "carrelage": [
        "0) Généralités — Présentation et documents de référence",
        "1) Ragréage et préparation des supports",
        "2) Carrelage sols",
        "3) Faïence murale",
        "4) Plinthes, seuils et divers",
    ],
    "menuiseries_bois": [
        "0) Généralités — Présentation et documents de référence",
        "1) Portes intérieures",
        "2) Habillages muraux et sous-tentures",
        "3) Plinthes",
        "4) Plafonds bois / Retombées bois",
        "5) Meubles et aménagements sur mesure",
        "6) Tables et gradins",
        "7) Divers",
    ],
    "menuiseries_int": [
        "0) Généralités — Présentation et documents de référence",
        "1) Portes intérieures",
        "2) Habillages muraux",
        "3) Plinthes et couvre-joints",
        "4) Divers",
    ],
    "peinture": [
        "0) Généralités — Présentation et documents de référence",
        "1) Travaux préparatoires murs et plafonds",
        "2) Peinture plafonds",
        "3) Peinture murs",
        "4) Boiseries et menuiseries",
        "5) Nettoyage de fin de chantier",
    ],
    "gros_oeuvre": [
        "0) Généralités — Présentation et documents de référence",
        "1) Terrassements et fouilles",
        "2) Fondations",
        "3) Structure béton armé",
        "4) Maçonnerie",
        "5) Divers",
    ],
    "electricite": [
        "0) Généralités — Présentation et documents de référence",
        "1) Distribution générale et tableaux",
        "2) Distribution terminale",
        "3) Éclairage",
        "4) Courants faibles",
        "5) Contrôle et essais",
    ],
    "chauffage_cvc": [
        "0) Généralités — Présentation et documents de référence",
        "1) Production de chaleur / froid",
        "2) Distribution",
        "3) Émetteurs",
        "4) Ventilation (VMC)",
        "5) Régulation",
        "6) Essais et mise en service",
    ],
}

# Structure par défaut (7 articles) pour les lots sans structure spécifique
DEFAULT_STRUCTURE = [
    "Article 1 — Objet et domaine d'application",
    "Article 2 — Documents de référence (DTU, normes NF, Eurocodes avec dates d'édition)",
    "Article 3 — Provenance et qualité des matériaux",
    "Article 4 — Mode d'exécution des travaux",
    "Article 5 — Prescriptions techniques particulières",
    "Article 6 — Contrôles et essais",
    "Article 7 — Documents à fournir par l'entreprise",
]


def get_lot_label(lot_key: str) -> str:
    return LOT_LABELS.get(lot_key, lot_key)


def get_lot_structure(lot_key: str) -> list[str]:
    return LOT_STRUCTURE.get(lot_key, DEFAULT_STRUCTURE)


def get_dtu_files(lot_key: str) -> list[Path]:
    filenames = LOT_TO_FILES.get(lot_key, [])
    return [KNOWLEDGE_BASE_DIR / f for f in filenames if (KNOWLEDGE_BASE_DIR / f).exists()]


def get_dtu_refs(lot_key: str) -> list[str]:
    return LOT_TO_DTU_REFS.get(lot_key, [])
