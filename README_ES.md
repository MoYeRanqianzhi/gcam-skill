🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

Un skill de agente IA portable y autosuficiente para el [Modelo de Análisis del Cambio Global (GCAM)](https://github.com/JGCRI/gcam-core). Proporciona conocimiento experto completo y consciente de versiones sobre GCAM sin necesidad de instalaciones locales del modelo.

## Funcionalidades

Este skill equipa a los agentes IA (Claude, etc.) con un conocimiento profundo de todo el ecosistema GCAM:

- **Estructura del modelo** -- sistemas de energía, tierra, agua, economía, emisiones y clima
- **22 versiones de GCAM** (v3.2 a v8.7) con enrutamiento específico por versión y documentación dedicada
- **Configuración de escenarios** -- edición XML, diseño de políticas, modo target-finder, ejecuciones por lotes
- **Extracción de datos** -- referencias de API para Python (`gcamreader`) y R (`gcamextractor`) con más de 83 parámetros de extracción documentados
- **Análisis de escenarios** -- flujos de trabajo para comparación multi-escenario, patrones de visualización, plantillas de análisis comunes
- **Compilación e instalación** -- descarga de versiones publicadas, compilación desde código fuente, gestión del espacio de trabajo

## Instalación

Envía lo siguiente a tu agente IA (Claude Code, Codex, Cursor, etc.):

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

## Inicio Rápido

Una vez instalado, simplemente haz preguntas relacionadas con GCAM en tu agente:

```
> How do I set up a carbon tax scenario in GCAM v8.2?
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> What changed in the land system between v5.4 and v7.1?
```

El skill se activa automáticamente en consultas relacionadas con GCAM y dirige a la documentación de la versión correcta.

### Para Desarrolladores

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

Valida la integridad del skill:

```bash
python skills/gacm/scripts/validate_all.py
```

## Arquitectura

```
skills/gacm/
├── SKILL.md                    # SOP -- agent workflow, version routing, progressive disclosure
├── scripts/                    # 28 Python scripts (2 runtime, 3 generators, 23 validators)
│   ├── doc_search.py           # Runtime: search bundled references by version/pattern
│   ├── version_catalog.py      # Runtime: version registry and family metadata
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # One-shot validation suite
└── reference/                  # 33 topic docs + 22 version bundles
    ├── overview.md             # Model structure and core concepts
    ├── energy_system.md        # Resources, electricity, hydrogen, CCS, demand
    ├── land_system.md          # AgLU, GLU nesting, Moirai, carbon accounting
    ├── water_system.md         # 235 basins, cooling tech, water-energy-food nexus
    ├── economy.md              # GDP, KLEM, GCAM-macro, SAM calibration
    ├── emissions_climate.md    # CO2/non-CO2, MACs, Hector, GWP, IAMC
    ├── policies_scenarios.md   # Carbon tax, RES, target finder, XML examples
    ├── trade.md                # Armington, Heckscher-Ohlin, commodity assignments
    ├── scenario_analysis.md    # Python/R multi-scenario comparison workflows
    ├── gcamreader_api.md       # Python Query/Connection API reference
    ├── gcamextractor_api.md    # R readgcam() with 83+ params, 14 groups
    ├── ssp.md                  # SSP1-5 narratives, quantitative assumptions
    ├── gcam_usa.md             # 51-state sub-national extension
    ├── versions/               # 22 version-specific route files (v3.2--v8.7)
    └── version_pages/          # 614 bundled version-page markdown files
```

### Divulgación Progresiva

El skill utiliza un sistema de carga de tres niveles para minimizar el consumo de la ventana de contexto:

| Nivel | Contenido | Momento de carga | Coste en tokens |
|-------|-----------|-------------------|-----------------|
| **1** | `name` + `description` | Siempre | ~130 tokens |
| **2** | Flujo de trabajo de SKILL.md | Al activarse el skill | ~2.800 tokens |
| **3** | Documentos temáticos, scripts, páginas de versiones | Bajo demanda | Ilimitado |

Tres **puertas de parada de carga** explícitas evitan la acumulación innecesaria de contexto.

## Cobertura

### Sistemas GCAM

| Sistema | Temas cubiertos |
|---------|----------------|
| Energía | Recursos fósiles/renovables, electricidad (segmentos de carga, refrigeración), hidrógeno (12 tecnologías), CCS, refinación, integración de intermitentes |
| Tierra | AgLU logit anidado, GLU, preprocesamiento Moirai, contabilidad de carbono, bioenergía, ganadería, gestión forestal |
| Agua | 6 sectores de demanda, 235 cuencas, competencia de tecnologías de refrigeración, aguas subterráneas (Superwell), desalinización |
| Economía | PIB exógeno/endógeno, producción CES KLEM, calibración SAM, retroalimentación del precio del carbono |
| Emisiones | 30+ especies, curvas MAC, Hector v3.2.0 (permafrost), GWP AR4/AR5, mercados de GEI vinculados |
| Políticas | Impuesto/restricción de carbono, RES/CES, target finder (7 tipos de objetivo), protección de tierras, apilamiento de múltiples políticas |
| Comercio | Heckscher-Ohlin, Armington (21 sectores con parámetros logit), comercio fijo, comercio interestatal GCAM-USA |

### APIs de Herramientas

| Herramienta | Cobertura |
|-------------|-----------|
| `gcamreader` (Python) | `Query`, `LocalDBConn`, `RemoteDBConn`, `runQuery`, `parse_batch_query`, modos CLI |
| `gcamextractor` (R) | `readgcam()` 16 parámetros, 83+ valores de `paramsSelect` en 14 grupos, caché `.Proj`, agregación regional |
| `rgcam` (R) | Resumen conceptual; sin código fuente en el proyecto |
| ModelInterface | Generación XML de comandos por lotes en modo headless |

### Soporte de Versiones

22 versiones desde **v3.2** hasta **v8.7**, organizadas por familia de documentación:

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1, v8.2 línea base)
- `delta-only` (v7.2--v7.4, v8.0--v8.1, v8.3--v8.7)

## Validación

El skill incluye 22 validadores automatizados que cubren:

- Cumplimiento de contratos documentales (frases requeridas, detección de versiones)
- Integridad de paquetes de páginas y paridad de contenido
- Higiene del sistema de archivos y portabilidad multiplataforma
- Alineación de divulgación progresiva
- Cobertura de contratos semánticos (cada documento tiene un validador)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## Documentación del Proyecto

La memoria persistente para colaboradores se encuentra en `docs/`:

- `PROJECT.md` -- alcance, decisiones, tareas pendientes
- `DEVELOPMENT.md` -- guía de flujo de trabajo, taxonomía de scripts, puertas de validación
- `CHANGELOG.md` -- registro de hitos
- `KNOWN_ISSUES.md` -- limitaciones conocidas y deuda técnica

## Licencia

[MIT](LICENSE)

## Agradecimientos

Este skill sintetiza contenido del ecosistema GCAM de código abierto:

- [GCAM](https://github.com/JGCRI/gcam-core) -- el Modelo de Análisis del Cambio Global (PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- documentación oficial de GCAM
- [gcamreader](https://github.com/JGCRI/gcamreader) -- interfaz de consulta en Python
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- paquete de extracción en R
