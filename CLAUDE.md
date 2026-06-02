# Projet : Générateur de CCTP IA avec DTU à jour

## Vision produit

SaaS permettant à un architecte de **générer automatiquement un CCTP (Cahier des Clauses Techniques Particulières) complet et à jour réglementairement** pour chaque lot d'un projet de construction, en quelques minutes au lieu de plusieurs jours.

Le problème : les architectes utilisent des modèles de CCTP qui datent de 5-10 ans, avec des références DTU et normes NF obsolètes. Mettre à jour manuellement est un travail de juriste technique. Les éditeurs existants (Le Moniteur, Ediliconstruct) proposent des bases statiques chères et non adaptées à l'IA.

---

## Contexte réglementaire français

### Qu'est-ce qu'un CCTP ?
Document contractuel joint au marché de travaux qui décrit pour chaque lot :
- Les matériaux et produits exigés
- Les modes d'exécution
- Les références aux normes et DTU applicables
- Les contrôles et essais à réaliser
- Les tolérances admises

### Structure type d'un CCTP par lot

```
CCTP — LOT 02 CHARPENTE BOIS
1. OBJET ET DOMAINE D'APPLICATION
2. DOCUMENTS DE RÉFÉRENCE
   - DTU 31.1 : Charpente et escaliers en bois
   - DTU 31.2 : Construction de maisons et bâtiments en ossature bois
   - NF EN 1995 (Eurocode 5)
   - ...
3. PROVENANCE ET QUALITÉ DES MATÉRIAUX
4. MODE D'EXÉCUTION DES TRAVAUX
5. PRESCRIPTIONS TECHNIQUES PARTICULIÈRES
6. CONTRÔLES ET ESSAIS
7. DOCUMENTS À FOURNIR PAR L'ENTREPRISE
```

### Les lots principaux d'un projet de construction
01 - Démolition / Terrassement
02 - Gros Œuvre / Maçonnerie
03 - Charpente Bois
04 - Couverture / Étanchéité
05 - Menuiseries Extérieures (aluminium, PVC, bois)
06 - Menuiseries Intérieures
07 - Isolation (ITI / ITE)
08 - Cloisons / Doublages / Faux-plafonds
09 - Revêtements de sol
10 - Carrelage / Faïence
11 - Peinture / Enduits
12 - Plomberie / Sanitaires
13 - Chauffage / VMC / Climatisation (CVC)
14 - Électricité CFO/CFA
15 - VRD / Espaces extérieurs

---

## Sources réglementaires

### DTU (Documents Techniques Unifiés)
- Publiés par le **CSTB** (Centre Scientifique et Technique du Bâtiment) et l'**AFNOR**
- ~200 DTU couvrant tous les corps d'état
- **Accès payant** : abonnement AFNOR ~2000€/an (incontournable pour la source officielle)
- Alternative légale : les DTU sont résumés dans de nombreuses ressources professionnelles (revues, formations)
- Option : partenariat CSTB ou accord de licence pour accès API

### Autres sources importantes
- **Eurocodes** : normes de calcul structurel européennes (EN 1990 à EN 1999)
- **RE2020** : Réglementation Environnementale 2020 (thermique + carbone)
- **Accessibilité PMR** : arrêté du 20 avril 2017 + loi du 11 février 2005
- **Sécurité incendie ERP** : arrêté du 25 juin 1980 (établissements recevant du public)
- **NF DTU** : déclinés par domaine (ex: NF DTU 20.1 pour maçonnerie)

### Stratégie d'accès aux sources (par ordre de préférence)
1. **Abonnement AFNOR/CSTB** (~2000€/an) → accès officiel et complet
2. **Partenariat CSTB** → accord commercial pour intégration dans un SaaS
3. **Sources publiques** : textes de loi, arrêtés, eurocodes (gratuits sur Légifrance et EUR-Lex)
4. **Base propriétaire construite progressivement** : résumés structurés des DTU principaux

---

## Architecture technique

### Pipeline

```
1. Saisie projet par l'architecte
   - Type de projet (neuf / rénovation / ERP / logement / tertiaire)
   - Lots concernés (sélection multiple)
   - Spécificités (zone climatique, zone sismique, contexte PMR, etc.)
        ↓
2. Sélection des sources réglementaires applicables
   - Mapping automatique : type de projet × lot → DTU applicables
   - Vérification des mises à jour récentes (amendements, nouvelles éditions)
        ↓
3. Génération LLM par lot
   - RAG sur base de connaissances DTU structurée
   - Prompt spécialisé par lot (voir section Prompts)
   - Output : CCTP complet par lot en Markdown
        ↓
4. Revue et édition par l'architecte
   - Interface d'édition rich text
   - Suggestions d'ajustements selon spécificités projet
        ↓
5. Export
   - Word (.docx) avec mise en forme professionnelle
   - PDF signé
   - Pack complet tous lots en un ZIP
```

### Stack recommandée MVP

```
Backend    : Python + FastAPI
Frontend   : React + TipTap (éditeur rich text)
LLM        : Claude claude-sonnet-4-20250514 (long context pour CCTP complets)
RAG        : LlamaIndex ou LangChain + ChromaDB (vector store)
Sources    : Base de connaissances DTU structurée (JSON/Markdown)
Export     : python-docx + Jinja2 templates
Auth       : Magic link email
BDD        : PostgreSQL (Supabase)
Hébergement: Railway ou Render
```

---

## Base de connaissances DTU (structure)

Chaque DTU est stocké comme un document structuré :

```json
{
  "reference": "NF DTU 31.2",
  "titre": "Construction de maisons et bâtiments à ossature en bois",
  "date_edition": "2019-03",
  "derniere_mise_a_jour": "2023-01",
  "lots_concernes": ["charpente", "ossature bois"],
  "domaine_application": "...",
  "points_cles": [
    {
      "article": "4.1",
      "sujet": "Qualité des bois",
      "contenu": "...",
      "exigences": ["..."]
    }
  ],
  "normes_associees": ["NF EN 1995-1-1", "NF B 52-001"],
  "remplace": "DTU 31.2 édition 2011",
  "statut": "en_vigueur"
}
```

---

## Prompts

### Prompt système

```
Tu es un expert en réglementation de la construction française, spécialisé dans la rédaction de CCTP (Cahiers des Clauses Techniques Particulières).

Tu maîtrises parfaitement :
- Les DTU (Documents Techniques Unifiés) et leurs éditions en vigueur
- Les normes NF et Eurocodes applicables à la construction
- La RE2020 et les exigences thermiques/environnementales
- Les règles d'accessibilité PMR
- La réglementation sécurité incendie ERP

Règles de rédaction :
- Toujours citer les références réglementaires exactes avec leur date d'édition
- Indiquer si une norme a été mise à jour récemment
- Adapter le niveau de détail au type de projet (neuf vs rénovation, logement vs ERP)
- Utiliser le vocabulaire technique français standard du BTP
- Ne jamais inventer une référence réglementaire
- Si une exigence est incertaine, indiquer [À VÉRIFIER AVEC LE CSTB]
```

### Prompt utilisateur par lot

```
Génère le CCTP complet pour le lot suivant :

Lot : {numero_lot} - {nom_lot}
Type de projet : {type_projet}
Usage : {usage} (logement / ERP type {type_erp} / tertiaire / industrie)
Zone climatique : {zone_climatique} (H1a / H1b / H1c / H2a / H2b / H2c / H3)
Zone sismique : {zone_sismique} (0 / 1 / 2 / 3 / 4)
Accessibilité PMR : {oui/non}
Spécificités : {spécificités_particulières}

DTU de référence disponibles pour ce lot :
{liste_dtu_applicables_depuis_rag}

Génère un CCTP complet avec :
1. Objet et domaine d'application
2. Documents de référence (avec dates d'édition)
3. Provenance et qualité des matériaux
4. Mode d'exécution
5. Prescriptions techniques particulières
6. Contrôles et essais
7. Documents à fournir par l'entreprise
```

---

## Mapping Lot → DTU principaux (à compléter)

```python
LOT_TO_DTU = {
    "gros_oeuvre": ["NF DTU 20.1", "NF DTU 13.1", "NF DTU 13.2", "NF DTU 13.3"],
    "charpente_bois": ["NF DTU 31.1", "NF DTU 31.2", "NF EN 1995"],
    "couverture": ["NF DTU 40.1", "NF DTU 40.21", "NF DTU 40.35", "NF DTU 43.1"],
    "menuiseries_ext": ["NF DTU 36.5", "NF DTU 37.1", "NF EN 14351"],
    "isolation_ite": ["NF DTU 55.2", "Avis techniques CSTB"],
    "cloisons": ["NF DTU 25.41", "NF DTU 25.42"],
    "revetements_sol": ["NF DTU 51.1", "NF DTU 51.2", "NF DTU 52.1"],
    "carrelage": ["NF DTU 52.2", "NF DTU 52.4"],
    "peinture": ["NF DTU 59.1", "NF DTU 59.2"],
    "plomberie": ["NF DTU 60.1", "NF DTU 60.11", "NF DTU 65.10"],
    "chauffage_cvc": ["NF DTU 65.11", "NF DTU 65.14", "RE2020"],
    "electricite": ["NF C 15-100", "NF C 14-100"],
    "vrd": ["NF DTU 70.1", "NF EN 752"],
}
```

---

## Fonctionnalités MVP (v1)

- [ ] Création de projet (type, usage, zone climatique, zone sismique, PMR)
- [ ] Sélection des lots à traiter
- [ ] Génération CCTP par lot via LLM + RAG sur base DTU
- [ ] Affichage et édition inline du CCTP généré
- [ ] Export Word (.docx) par lot ou pack complet
- [ ] Historique des CCTP par projet
- [ ] Base initiale : 5 lots principaux (GO, charpente, menuiseries ext, élec, CVC)

## Fonctionnalités v2

- [ ] 15 lots couverts
- [ ] Mise à jour automatique : notification quand un DTU est révisé
- [ ] Comparaison avec version précédente du CCTP (suivi des évolutions réglementaires)
- [ ] Clauses particulières personnalisables par cabinet (bibliothèque de clauses favorites)
- [ ] Génération du CCAP (Clauses Administratives Particulières) associé
- [ ] Import d'un CCTP existant → mise à jour automatique des références obsolètes

## Fonctionnalités v3

- [ ] API pour intégration dans les logiciels de gestion de cabinet existants
- [ ] Génération automatique des DPGF (Décomposition du Prix Global et Forfaitaire)
- [ ] Module BIM : extraction des données du modèle Revit/IFC pour pré-remplir le projet

---

## Modèle économique

- **Par lot généré** : 15€/lot (modèle à l'usage, no subscription friction)
- **Abonnement mensuel** : 79€/mois pour lots illimités
- **Abonnement annuel** : 690€/an (= 2 mois offerts)
- **Cabinet** : 149€/mois pour 5 utilisateurs

Un projet standard a 8-12 lots → valeur d'un projet = 120-180€ à l'usage.
Un architecte fait 5-15 projets/an nécessitant un CCTP complet.

## Pricing de référence marché
- Ediliconstruct : ~1200€/an (base statique, pas d'IA)
- Le Moniteur Pro : ~800€/an (documentation technique)
- Valeur perçue : 2-3 jours de travail économisés par projet × 150€/h = 2400-3600€/projet

---

## Go-To-Market

### Phase 1 — Validation (0-10 clients)
- Contact direct architectes (réseau, Ordre des Architectes local)
- Gratuit en échange de feedback sur qualité des CCTP générés
- Valider : est-ce que le CCTP est utilisable sans réécriture majeure ?

### Phase 2 — Croissance (10-100 clients)
- Contenu LinkedIn : "J'ai généré le CCTP lot électricité en 4 minutes"
- Partenariat avec écoles d'architecture (ENSA)
- SEO : "modèle CCTP lot [X] gratuit"

### Phase 3 — Scale
- Partenariat CSTB ou Le Moniteur (distribution via leur réseau)
- Intégration dans logiciels de gestion de cabinet (ArchiSnapper, Archidoc)

---

## Obstacles et risques

| Obstacle | Mitigation |
|----------|-----------|
| Accès aux DTU (payants AFNOR) | Commencer avec sources publiques + abonnement AFNOR dès premiers revenus |
| Responsabilité si CCTP erroné | Disclaimer clair "à valider par un professionnel" ; l'architecte reste responsable |
| LLM qui hallucine des références | RAG strict + vérification systématique des références citées dans la base |
| Mise à jour des normes | Veille réglementaire automatisée (scraping AFNOR/CSTB) + alertes utilisateurs |

---

## Fichiers du projet

```
CLAUDE.md           Ce fichier
src/
  api/              Backend FastAPI
  frontend/         React app + éditeur TipTap
  rag/              Indexation et requêtes base DTU
  knowledge_base/   Documents DTU structurés (JSON/Markdown)
  export/           Génération Word/PDF
  lot_mapping/      Mapping lot → DTU applicables
```
