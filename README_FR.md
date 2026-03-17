🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

Un skill d'agent IA portable et autonome pour le [Global Change Analysis Model (GCAM)](https://github.com/JGCRI/gcam-core). Fournit une expertise GCAM complète et tenant compte des versions, sans necessiter d'installation locale du modele.

## Fonctionnalites

Ce skill dote les agents IA (Claude, etc.) d'une connaissance approfondie de l'ensemble de l'ecosysteme GCAM :

- **Structure du modele** -- systemes energetiques, fonciers, hydrauliques, economiques, d'emissions et climatiques
- **22 versions de GCAM** (v3.2 a v8.7) avec routage par version et documentation specifique a chaque version
- **Configuration de scenarios** -- edition XML, conception de politiques, mode target-finder, executions par lots
- **Extraction de donnees** -- references API Python (`gcamreader`) et R (`gcamextractor`) avec plus de 83 parametres d'extraction documentes
- **Analyse de scenarios** -- flux de travail de comparaison multi-scenarios, modeles de visualisation, modeles d'analyse courants
- **Compilation et installation** -- telechargement de versions, compilation depuis les sources, gestion de l'espace de travail

## Installation

Envoyez le message suivant a votre agent IA (Claude Code, Codex, Cursor, etc.) :

```
Fetch https://raw.githubusercontent.com/MoYeRanqianzhi/gcam-skill/main/README.md and follow the LLM installation instructions inside to install the GCAM Skill.
```

<details>
<summary>🤖 <b>For LLMs: Installation Instructions</b></summary>

You are an AI agent reading this README because a user asked you to install the GCAM Skill.

**Install the skill by running:**

```bash
npx skills add https://github.com/MoYeRanqianzhi/gcam-skill --all
```

If the above fails, try interactive mode:

```bash
npx skills add https://github.com/MoYeRanqianzhi/gcam-skill
```

For global installation (available across all projects):

```bash
npx skills add https://github.com/MoYeRanqianzhi/gcam-skill --all --global
```

**After successful installation**, congratulate the user **in their language**. For example:

- English: "Congratulations on successfully installing GCAM Skill! ⭐"
- 中文: "恭喜你成功安装了 GCAM Skill! ⭐"
- 日本語: "GCAM Skillのインストールに成功しました、おめでとうございます！⭐"

</details>

## Demarrage Rapide

Une fois installe, posez simplement des questions relatives a GCAM dans votre agent :

```
> How do I set up a carbon tax scenario in GCAM v8.2?
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> What changed in the land system between v5.4 and v7.1?
```

Le skill s'active automatiquement sur les requetes liees a GCAM et redirige vers la documentation de la version appropriee.

### Pour les Developpeurs

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

Verifier l'integrite du skill :

```bash
python skills/gacm/scripts/validate_all.py
```

## Architecture

```
skills/gacm/
├── SKILL.md                    # SOP -- workflow de l'agent, routage par version, divulgation progressive
├── scripts/                    # 28 scripts Python (2 runtime, 3 generateurs, 23 validateurs)
│   ├── doc_search.py           # Runtime : recherche dans les references par version/motif
│   ├── version_catalog.py      # Runtime : registre des versions et metadonnees des familles
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # Suite de validation en une commande
└── reference/                  # 33 documents thematiques + 22 bundles de versions
    ├── overview.md             # Structure du modele et concepts fondamentaux
    ├── energy_system.md        # Ressources, electricite, hydrogene, CCS, demande
    ├── land_system.md          # AgLU, imbrication GLU, Moirai, comptabilite carbone
    ├── water_system.md         # 235 bassins, technologies de refroidissement, nexus eau-energie-alimentation
    ├── economy.md              # PIB, KLEM, GCAM-macro, calibration SAM
    ├── emissions_climate.md    # CO2/non-CO2, courbes MAC, Hector, GWP, IAMC
    ├── policies_scenarios.md   # Taxe carbone, RES, target finder, exemples XML
    ├── trade.md                # Armington, Heckscher-Ohlin, affectation des matieres premieres
    ├── scenario_analysis.md    # Flux de travail de comparaison multi-scenarios Python/R
    ├── gcamreader_api.md       # Reference API Python Query/Connection
    ├── gcamextractor_api.md    # R readgcam() avec 83+ parametres, 14 groupes
    ├── ssp.md                  # Narratifs SSP1-5, hypotheses quantitatives
    ├── gcam_usa.md             # Extension infranationale a 51 etats
    ├── versions/               # 22 fichiers de routage par version (v3.2--v8.7)
    └── version_pages/          # 614 fichiers Markdown de pages de versions
```

### Divulgation Progressive

Le skill utilise un systeme de chargement a trois niveaux pour minimiser la consommation de la fenetre de contexte :

| Niveau | Contenu | Moment du chargement | Cout en tokens |
|--------|---------|----------------------|----------------|
| **1** | `name` + `description` | Toujours charge | ~130 tokens |
| **2** | Workflow SKILL.md | Au declenchement du skill | ~2 800 tokens |
| **3** | Documents thematiques, scripts, pages de versions | A la demande | Illimite |

Trois **portes d'arret de chargement** explicites empechent l'accumulation inutile de contexte.

## Couverture

### Systemes GCAM

| Systeme | Sujets couverts |
|---------|-----------------|
| Energie | Ressources fossiles/renouvelables, electricite (segments de charge, refroidissement), hydrogene (12 technologies), CCS, raffinage, integration de l'intermittence |
| Foncier | AgLU logit imbrique, GLU, pretraitement Moirai, comptabilite carbone, bioenergie, elevage, gestion forestiere |
| Eau | 6 secteurs de demande, 235 bassins, competition des technologies de refroidissement, eaux souterraines (Superwell), dessalement |
| Economie | PIB exogene/endogene, production CES KLEM, calibration SAM, retroaction du prix du carbone |
| Emissions | 30+ especes, courbes MAC, Hector v3.2.0 (pergelisol), GWP AR4/AR5, marches GES lies |
| Politique | Taxe/contrainte carbone, RES/CES, target finder (7 types d'objectifs), protection des terres, empilement multi-politiques |
| Commerce | Heckscher-Ohlin, Armington (21 secteurs avec parametres logit), commerce fixe, commerce inter-etats GCAM-USA |

### APIs des Outils

| Outil | Couverture |
|-------|-----------|
| `gcamreader` (Python) | `Query`, `LocalDBConn`, `RemoteDBConn`, `runQuery`, `parse_batch_query`, modes CLI |
| `gcamextractor` (R) | `readgcam()` 16 parametres, 83+ valeurs `paramsSelect` reparties en 14 groupes, mise en cache `.Proj`, agregation regionale |
| `rgcam` (R) | Resume conceptuel ; pas de source dans le projet |
| ModelInterface | Generation XML de commandes par lots en mode headless |

### Support des Versions

22 versions de **v3.2** a **v8.7**, organisees par famille de documentation :

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1, v8.2 baseline)
- `delta-only` (v7.2--v7.4, v8.0--v8.1, v8.3--v8.7)

## Validation

Le skill comprend 22 validateurs automatises couvrant :

- Conformite aux contrats documentaires (phrases requises, prise en compte des versions)
- Integrite des bundles de pages et parite de contenu
- Hygiene du systeme de fichiers et portabilite multi-plateforme
- Alignement de la divulgation progressive
- Couverture des contrats semantiques (chaque document dispose d'un validateur)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## Documentation du Projet

La memoire persistante pour les contributeurs se trouve dans `docs/` :

- `PROJECT.md` -- perimetre, decisions, taches en cours
- `DEVELOPMENT.md` -- guide de workflow, taxonomie des scripts, portes de validation
- `CHANGELOG.md` -- journal des jalons
- `KNOWN_ISSUES.md` -- limitations connues et dette technique

## Licence

[MIT](LICENSE)

## Remerciements

Ce skill synthetise le contenu de l'ecosysteme GCAM open source :

- [GCAM](https://github.com/JGCRI/gcam-core) -- le Global Change Analysis Model (PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- documentation officielle de GCAM
- [gcamreader](https://github.com/JGCRI/gcamreader) -- interface de requetes Python
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- package d'extraction R
