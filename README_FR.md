🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

Un skill d'agent IA portable et autonome pour le [Global Change Analysis Model (GCAM)](https://github.com/JGCRI/gcam-core). Fournit une expertise GCAM complète et tenant compte des versions, sans nécessiter d'installation locale du modèle.

## Fonctionnalités

Ce skill dote les agents IA (Claude, etc.) d'une connaissance approfondie de l'ensemble de l'écosystème GCAM :

- **Structure du modèle** -- systèmes énergétiques, fonciers, hydrauliques, économiques, d'émissions et climatiques
- **22 versions de GCAM** (v3.2 à v8.7) avec routage par version et documentation spécifique à chaque version
- **Configuration de scénarios** -- édition XML, conception de politiques, mode target-finder, exécutions par lots
- **Extraction de données** -- références API Python (`gcamreader`) et R (`gcamextractor`) avec plus de 83 paramètres d'extraction documentés
- **Analyse de scénarios** -- flux de travail de comparaison multi-scénarios, modèles de visualisation, modèles d'analyse courants
- **Compilation et installation** -- téléchargement de versions, compilation depuis les sources, gestion de l'espace de travail

## Installation

Envoyez le message suivant à votre agent IA (Claude Code, Codex, Cursor, etc.) :

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

## Démarrage Rapide

Une fois installé, posez simplement des questions relatives à GCAM dans votre agent :

```
> How do I set up a carbon tax scenario in GCAM v8.2?
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> What changed in the land system between v5.4 and v7.1?
```

Le skill s'active automatiquement sur les requêtes liées à GCAM et redirige vers la documentation de la version appropriée.

### Pour les Développeurs

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

Vérifier l'intégrité du skill :

```bash
python skills/gacm/scripts/validate_all.py
```

## Architecture

```
skills/gacm/
├── SKILL.md                    # SOP -- workflow de l'agent, routage par version, divulgation progressive
├── scripts/                    # 28 scripts Python (2 runtime, 3 générateurs, 23 validateurs)
│   ├── doc_search.py           # Runtime : recherche dans les références par version/motif
│   ├── version_catalog.py      # Runtime : registre des versions et métadonnées des familles
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # Suite de validation en une commande
└── reference/                  # 33 documents thématiques + 22 bundles de versions
    ├── overview.md             # Structure du modèle et concepts fondamentaux
    ├── energy_system.md        # Ressources, électricité, hydrogène, CCS, demande
    ├── land_system.md          # AgLU, imbrication GLU, Moirai, comptabilité carbone
    ├── water_system.md         # 235 bassins, technologies de refroidissement, nexus eau-énergie-alimentation
    ├── economy.md              # PIB, KLEM, GCAM-macro, calibration SAM
    ├── emissions_climate.md    # CO2/non-CO2, courbes MAC, Hector, GWP, IAMC
    ├── policies_scenarios.md   # Taxe carbone, RES, target finder, exemples XML
    ├── trade.md                # Armington, Heckscher-Ohlin, affectation des matières premières
    ├── scenario_analysis.md    # Flux de travail de comparaison multi-scénarios Python/R
    ├── gcamreader_api.md       # Référence API Python Query/Connection
    ├── gcamextractor_api.md    # R readgcam() avec 83+ paramètres, 14 groupes
    ├── ssp.md                  # Narratifs SSP1-5, hypothèses quantitatives
    ├── gcam_usa.md             # Extension infranationale à 51 États
    ├── versions/               # 22 fichiers de routage par version (v3.2--v8.7)
    └── version_pages/          # 614 fichiers Markdown de pages de versions
```

### Divulgation Progressive

Le skill utilise un système de chargement à trois niveaux pour minimiser la consommation de la fenêtre de contexte :

| Niveau | Contenu | Moment du chargement | Coût en tokens |
|--------|---------|----------------------|----------------|
| **1** | `name` + `description` | Toujours chargé | ~130 tokens |
| **2** | Workflow SKILL.md | Au déclenchement du skill | ~2 800 tokens |
| **3** | Documents thématiques, scripts, pages de versions | À la demande | Illimité |

Trois **portes d'arrêt de chargement** explicites empêchent l'accumulation inutile de contexte.

## Couverture

### Systèmes GCAM

| Système | Sujets couverts |
|---------|-----------------|
| Énergie | Ressources fossiles/renouvelables, électricité (segments de charge, refroidissement), hydrogène (12 technologies), CCS, raffinage, intégration de l'intermittence |
| Foncier | AgLU logit imbriqué, GLU, prétraitement Moirai, comptabilité carbone, bioénergie, élevage, gestion forestière |
| Eau | 6 secteurs de demande, 235 bassins, compétition des technologies de refroidissement, eaux souterraines (Superwell), dessalement |
| Économie | PIB exogène/endogène, production CES KLEM, calibration SAM, rétroaction du prix du carbone |
| Émissions | 30+ espèces, courbes MAC, Hector v3.2.0 (pergélisol), GWP AR4/AR5, marchés GES liés |
| Politique | Taxe/contrainte carbone, RES/CES, target finder (7 types d'objectifs), protection des terres, empilement multi-politiques |
| Commerce | Heckscher-Ohlin, Armington (21 secteurs avec paramètres logit), commerce fixe, commerce inter-États GCAM-USA |

### APIs des Outils

| Outil | Couverture |
|-------|-----------|
| `gcamreader` (Python) | `Query`, `LocalDBConn`, `RemoteDBConn`, `runQuery`, `parse_batch_query`, modes CLI |
| `gcamextractor` (R) | `readgcam()` 16 paramètres, 83+ valeurs `paramsSelect` réparties en 14 groupes, mise en cache `.Proj`, agrégation régionale |
| `rgcam` (R) | Résumé conceptuel ; pas de source dans le projet |
| ModelInterface | Génération XML de commandes par lots en mode headless |

### Support des Versions

22 versions de **v3.2** à **v8.7**, organisées par famille de documentation :

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1, v8.2 baseline)
- `delta-only` (v7.2--v7.4, v8.0--v8.1, v8.3--v8.7)

## Validation

Le skill comprend 22 validateurs automatisés couvrant :

- Conformité aux contrats documentaires (phrases requises, prise en compte des versions)
- Intégrité des bundles de pages et parité de contenu
- Hygiène du système de fichiers et portabilité multi-plateforme
- Alignement de la divulgation progressive
- Couverture des contrats sémantiques (chaque document dispose d'un validateur)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## Documentation du Projet

La mémoire persistante pour les contributeurs se trouve dans `docs/` :

- `PROJECT.md` -- périmètre, décisions, tâches en cours
- `DEVELOPMENT.md` -- guide de workflow, taxonomie des scripts, portes de validation
- `CHANGELOG.md` -- journal des jalons
- `KNOWN_ISSUES.md` -- limitations connues et dette technique

## Licence

[MIT](LICENSE)

## Remerciements

Ce skill synthétise le contenu de l'écosystème GCAM open source :

- [GCAM](https://github.com/JGCRI/gcam-core) -- le Global Change Analysis Model (PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- documentation officielle de GCAM
- [gcamreader](https://github.com/JGCRI/gcamreader) -- interface de requêtes Python
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- package d'extraction R
