🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

Ein portabler, eigenständiger AI-Agent-Skill für das [Global Change Analysis Model (GCAM)](https://github.com/JGCRI/gcam-core). Bietet umfassende, versionsbewusste GCAM-Expertise ohne lokale Modellinstallationen.

## Funktionsübersicht

Dieser Skill stattet AI-Agenten (Claude usw.) mit tiefgehendem Wissen über das gesamte GCAM-Ökosystem aus:

- **Modellstruktur** -- Energie-, Land-, Wasser-, Wirtschafts-, Emissions- und Klimasysteme
- **22 GCAM-Versionen** (v3.2 bis v8.7) mit versionsspezifischem Routing und Dokumentation
- **Szenariokonfiguration** -- XML-Bearbeitung, Politikdesign, Target-Finder-Modus, Batch-Läufe
- **Datenextraktion** -- Python (`gcamreader`) und R (`gcamextractor`) API-Referenzen mit 83+ dokumentierten Extraktionsparametern
- **Szenarioanalyse** -- Multi-Szenario-Vergleichsworkflows, Visualisierungsmuster, gängige Analysevorlagen
- **Build & Installation** -- Release-Download, Quellcode-Kompilierung, Workspace-Verwaltung

## Installation

Sende Folgendes an deinen AI-Agenten (Claude Code, Codex, Cursor usw.):

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

## Schnellstart

Nach der Installation kannst du GCAM-bezogene Fragen direkt an deinen Agenten stellen:

```
> Set up a carbon tax scenario in GCAM v8.2
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> Analyze land system changes between v5.4 and v7.1
```

Der Skill aktiviert sich automatisch bei GCAM-bezogenen Anfragen und leitet zur korrekten Versionsdokumentation weiter.

### Für Entwickler

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

Skill-Integrität überprüfen:

```bash
python skills/gacm/scripts/validate_all.py
```

## Architektur

```
skills/gacm/
├── SKILL.md                    # SOP -- Agent-Workflow, Versionsrouting, Progressive Disclosure
├── scripts/                    # 28 Python-Skripte (2 Runtime, 3 Generatoren, 23 Validatoren)
│   ├── doc_search.py           # Runtime: gebündelte Referenzen nach Version/Muster durchsuchen
│   ├── version_catalog.py      # Runtime: Versionsregister und Familien-Metadaten
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # Komplette Validierungssuite
└── reference/                  # 33 Themendokumente + 22 Versionsbündel
    ├── overview.md             # Modellstruktur und Kernkonzepte
    ├── energy_system.md        # Ressourcen, Strom, Wasserstoff, CCS, Nachfrage
    ├── land_system.md          # AgLU, GLU-Verschachtelung, Moirai, Kohlenstoffbilanzierung
    ├── water_system.md         # 235 Einzugsgebiete, Kühltechnologien, Wasser-Energie-Nahrung-Nexus
    ├── economy.md              # GDP, KLEM, GCAM-macro, SAM-Kalibrierung
    ├── emissions_climate.md    # CO2/Nicht-CO2, MAC-Kurven, Hector, GWP, IAMC
    ├── policies_scenarios.md   # Kohlenstoffsteuer, RES, Target Finder, XML-Beispiele
    ├── trade.md                # Armington, Heckscher-Ohlin, Güterzuordnungen
    ├── scenario_analysis.md    # Python/R Multi-Szenario-Vergleichsworkflows
    ├── gcamreader_api.md       # Python Query/Connection API-Referenz
    ├── gcamextractor_api.md    # R readgcam() mit 83+ Parametern, 14 Gruppen
    ├── ssp.md                  # SSP1-5 Narrative, quantitative Annahmen
    ├── gcam_usa.md             # 51-Staaten subnationale Erweiterung
    ├── versions/               # 22 versionsspezifische Routendateien (v3.2--v8.7)
    └── version_pages/          # 614 gebündelte Versionsseitendateien (Markdown)
```

### Progressive Disclosure

Der Skill verwendet ein dreistufiges Ladesystem, um den Kontextfensterverbrauch zu minimieren:

| Stufe | Inhalt | Ladezeitpunkt | Token-Kosten |
|-------|--------|---------------|--------------|
| **1** | `name` + `description` | Immer geladen | ~130 Tokens |
| **2** | SKILL.md-Workflow | Bei Skill-Aktivierung | ~2.800 Tokens |
| **3** | Themendokumente, Skripte, Versionsseiten | Bei Bedarf | Unbegrenzt |

Drei explizite **Stop-Loading-Gates** verhindern unnötige Kontextakkumulation.

## Abdeckung

### GCAM-Systeme

| System | Abgedeckte Themen |
|--------|-------------------|
| Energie | Fossile/erneuerbare Ressourcen, Strom (Lastsegmente, Kühlung), Wasserstoff (12 Technologien), CCS, Raffination, Intermittenz-Integration |
| Land | AgLU Nested Logit, GLUs, Moirai-Vorverarbeitung, Kohlenstoffbilanzierung, Bioenergie, Viehwirtschaft, Forstwirtschaft |
| Wasser | 6 Nachfragesektoren, 235 Einzugsgebiete, Kühltechnologie-Wettbewerb, Grundwasser (Superwell), Entsalzung |
| Wirtschaft | Exogenes/endogenes GDP, KLEM CES-Produktionsfunktion, SAM-Kalibrierung, Kohlenstoffpreis-Rückkopplung |
| Emissionen | 30+ Spezies, MAC-Kurven, Hector v3.2.0 (Permafrost), GWP AR4/AR5, verknüpfte GHG-Märkte |
| Politik | Kohlenstoffsteuer/-beschränkung, RES/CES, Target Finder (7 Zieltypen), Landschaftsschutz, Multi-Policy-Stacking |
| Handel | Heckscher-Ohlin, Armington (21 Sektoren mit Logit-Parametern), Fixed Trade, GCAM-USA Interstate |

### Begleitende Tool-APIs

| Tool | Abdeckung |
|------|-----------|
| `gcamreader` (Python) | `Query`, `LocalDBConn`, `RemoteDBConn`, `runQuery`, `parse_batch_query`, CLI-Modi |
| `gcamextractor` (R) | `readgcam()` 16 Parameter, 83+ `paramsSelect`-Werte in 14 Gruppen, `.Proj`-Caching, Regionenaggregation |
| `rgcam` (R) | Konzeptuelle Zusammenfassung; keine Quelldaten im Projekt |
| ModelInterface | Headless Batch-Command XML-Generierung |

### Versionsunterstützung

22 Versionen von **v3.2** bis **v8.7**, organisiert nach Dokumentationsfamilie:

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1, v8.2 Baseline)
- `delta-only` (v7.2--v7.4, v8.0--v8.1, v8.3--v8.7)

## Validierung

Der Skill enthält 22 automatisierte Validatoren, die Folgendes abdecken:

- Dokumentvertragstreue (erforderliche Phrasen, Versionsbewusstsein)
- Seitenbündel-Integrität und Inhaltsparität
- Dateisystem-Hygiene und plattformübergreifende Portabilität
- Progressive-Disclosure-Ausrichtung
- Semantische Vertragsabdeckung (jedes Dokument hat einen Validator)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## Projektdokumentation

Die persistente Dokumentation für Mitwirkende befindet sich in `docs/`:

- `PROJECT.md` -- Umfang, Entscheidungen, offene Aufgaben
- `DEVELOPMENT.md` -- Workflow-Leitfaden, Skript-Taxonomie, Validierungsgates
- `CHANGELOG.md` -- Meilensteinprotokoll
- `KNOWN_ISSUES.md` -- Bekannte Einschränkungen und technische Schulden

## Lizenz

[MIT](LICENSE)

## Danksagungen

Dieser Skill fasst Inhalte aus dem Open-Source-GCAM-Ökosystem zusammen:

- [GCAM](https://github.com/JGCRI/gcam-core) -- das Global Change Analysis Model (PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- offizielle GCAM-Dokumentation
- [gcamreader](https://github.com/JGCRI/gcamreader) -- Python-Abfrageschnittstelle
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- R-Extraktionspaket
