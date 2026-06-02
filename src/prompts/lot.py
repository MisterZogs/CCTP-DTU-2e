from src.llm.base import CCTPParams
from src.lot_mapping.mapping import get_dtu_refs


def build_user_prompt(params: CCTPParams, dtu_context: str) -> str:
    dtu_refs = "\n".join(f"- {ref}" for ref in get_dtu_refs(params.lot_nom.lower().replace(" ", "_")))
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

**Extraits de la base réglementaire (DTU) :**
{dtu_context}

---

Génère un CCTP complet et professionnel structuré en 7 articles :

## CCTP — LOT {params.lot_numero} — {params.lot_nom.upper()}

### ARTICLE 1 — OBJET ET DOMAINE D'APPLICATION
### ARTICLE 2 — DOCUMENTS DE RÉFÉRENCE
(liste complète des DTU, normes NF, Eurocodes applicables avec dates d'édition)
### ARTICLE 3 — PROVENANCE ET QUALITÉ DES MATÉRIAUX
### ARTICLE 4 — MODE D'EXÉCUTION DES TRAVAUX
### ARTICLE 5 — PRESCRIPTIONS TECHNIQUES PARTICULIÈRES
(adapter selon le type de projet, zone climatique, zone sismique, PMR)
### ARTICLE 6 — CONTRÔLES ET ESSAIS
### ARTICLE 7 — DOCUMENTS À FOURNIR PAR L'ENTREPRISE
"""
