from src.llm.base import CCTPParams
from src.lot_mapping.mapping import get_dtu_refs, get_lot_structure


def build_user_prompt(params: CCTPParams, dtu_context: str) -> str:
    dtu_refs = "\n".join(f"- {ref}" for ref in get_dtu_refs(params.lot_nom.lower().replace(" ", "_")))
    lot_key = _lot_nom_to_key(params.lot_nom)
    structure = get_lot_structure(lot_key)
    structure_str = "\n".join(f"  {s}" for s in structure)
    pmr_str = "Oui" if params.pmr else "Non"
    type_erp_str = f" type {params.type_erp}" if params.type_erp else ""

    return f"""Génère le CCTP complet pour le lot suivant :

**Lot : {params.lot_numero} — {params.lot_nom}**
- Type de projet : {params.type_projet}
- Usage : {params.usage}{type_erp_str}
- Zone climatique : {params.zone_climatique}
- Zone sismique : {params.zone_sismique}
- Accessibilité PMR : {pmr_str}
- Spécificités : {params.specificites or "Aucune"}

**DTU et normes de référence applicables :**
{dtu_refs or "Voir contexte réglementaire ci-dessous"}

**Contexte réglementaire et exemples CCTP réels :**
{dtu_context}

---

## Règles de rédaction

1. **Structure adaptée au lot** — respecte la structure ci-dessous (chapitres numérotés comme dans un vrai CCTP, PAS les 7 articles génériques sauf si indiqué)
2. **Article 0 Généralités** — commence TOUJOURS par une section Généralités qui présente l'objet du lot, le maître d'ouvrage fictif, le projet, et la liste complète des normes et DTU applicables
3. **Spécifications produits** — cite des produits et marques de référence réels (ex: "Rigips BA13", "Mapei Ultralite S1", "Sikkens Rubbol") avec la mention "ou équivalent agréé"
4. **Prescriptions précises** — donne des dimensions, épaisseurs, entraxes, résistances et tolérances chiffrées
5. **Formulations normatives** — utilise "doit", "devra", "est exigé", "il est prescrit"
6. **Références réglementaires** — cite les articles et dates d'édition des DTU ; si incertain, écris [À VÉRIFIER AVEC LE CSTB]

## Structure attendue pour ce lot

{structure_str}

---

Génère maintenant le CCTP complet :

## CCTP — LOT {params.lot_numero} — {params.lot_nom.upper()}
"""


def _lot_nom_to_key(lot_nom: str) -> str:
    """Convertit un nom de lot lisible en clé de mapping."""
    nom = lot_nom.lower()
    mappings = [
        (["plâtrerie", "platrerie", "cloison", "doublage", "faux-plafond"], "platrerie"),
        (["carrelage", "faïence", "faience", "céramique", "ceramique"], "carrelage"),
        (["peinture", "enduit"], "peinture"),
        (["menuiserie ext", "menuiseries ext", "aluminium", "store", "screen"], "menuiseries_ext"),
        (["menuiserie bois", "menuiseries bois", "aménagement bois", "amenagement bois", "aménagements bois", "amenagements bois"], "menuiseries_bois"),
        (["menuiserie int", "menuiseries int"], "menuiseries_int"),
        (["gros œuvre", "gros oeuvre", "maçonnerie", "maconnerie"], "gros_oeuvre"),
        (["charpente"], "charpente_bois"),
        (["couverture", "étanchéité", "etancheite"], "couverture"),
        (["isolation"], "isolation"),
        (["plomberie", "sanitaire"], "plomberie"),
        (["chauffage", "cvc", "vmC", "climatisation"], "chauffage_cvc"),
        (["électricité", "electricite", "cfo", "cfa"], "electricite"),
        (["vrd", "espaces extérieurs", "espaces exterieurs"], "vrd"),
    ]
    for keywords, key in mappings:
        if any(kw in nom for kw in keywords):
            return key
    return "inconnu"
