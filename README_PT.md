🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

Uma skill de agente de IA portátil e autocontida para o [Global Change Analysis Model (GCAM)](https://github.com/JGCRI/gcam-core). Fornece conhecimento abrangente e sensível a versões sobre o GCAM sem necessidade de instalações locais do modelo.

## Funcionalidades

Esta skill equipa agentes de IA (Claude, etc.) com conhecimento profundo de todo o ecossistema GCAM:

- **Estrutura do modelo** -- sistemas de energia, terra, água, economia, emissões e clima
- **22 versões do GCAM** (v3.2 a v8.7) com roteamento sensível a versões e documentação específica por versão
- **Configuração de cenários** -- edição de XML, design de políticas, modo target-finder, execuções em lote
- **Extração de dados** -- referências de API para Python (`gcamreader`) e R (`gcamextractor`) com 83+ parâmetros de extração documentados
- **Análise de cenários** -- fluxos de trabalho de comparação multi-cenário, padrões de visualização, modelos de análise comuns
- **Compilação e instalação** -- download de releases, compilação a partir do código-fonte, gerenciamento de workspace

## Instalação

Envie o seguinte para o seu agente de IA (Claude Code, Codex, Cursor, etc.) para instalar:

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

## Início Rápido

Após a instalação, basta fazer perguntas relacionadas ao GCAM no seu agente:

```
> How do I set up a carbon tax scenario in GCAM v8.2?
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> What changed in the land system between v5.4 and v7.1?
```

A skill é ativada automaticamente em consultas relacionadas ao GCAM e direciona para a documentação da versão correta.

### Para Desenvolvedores

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

Validar a integridade da skill:

```bash
python skills/gacm/scripts/validate_all.py
```

## Arquitetura

```
skills/gacm/
├── SKILL.md                    # SOP -- fluxo de trabalho do agente, roteamento de versões, divulgação progressiva
├── scripts/                    # 28 scripts Python (2 runtime, 3 geradores, 23 validadores)
│   ├── doc_search.py           # Runtime: busca referências empacotadas por versão/padrão
│   ├── version_catalog.py      # Runtime: registro de versões e metadados de famílias
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # Suíte de validação completa
└── reference/                  # 33 documentos temáticos + 22 pacotes de versões
    ├── overview.md             # Estrutura do modelo e conceitos centrais
    ├── energy_system.md        # Recursos, eletricidade, hidrogênio, CCS, demanda
    ├── land_system.md          # AgLU, aninhamento GLU, Moirai, contabilidade de carbono
    ├── water_system.md         # 235 bacias, tecnologias de resfriamento, nexo água-energia-alimentos
    ├── economy.md              # GDP, KLEM, GCAM-macro, calibração SAM
    ├── emissions_climate.md    # CO2/não-CO2, curvas MAC, Hector, GWP, IAMC
    ├── policies_scenarios.md   # Imposto de carbono, RES, target finder, exemplos XML
    ├── trade.md                # Armington, Heckscher-Ohlin, atribuições de commodities
    ├── scenario_analysis.md    # Fluxos de trabalho de comparação multi-cenário Python/R
    ├── gcamreader_api.md       # Referência de API Python Query/Connection
    ├── gcamextractor_api.md    # R readgcam() com 83+ parâmetros, 14 grupos
    ├── ssp.md                  # Narrativas SSP1-5, premissas quantitativas
    ├── gcam_usa.md             # Extensão subnacional de 51 estados
    ├── versions/               # 22 arquivos de roteamento por versão (v3.2--v8.7)
    └── version_pages/          # 614 arquivos Markdown de páginas empacotadas por versão
```

### Divulgação Progressiva

A skill utiliza um sistema de carregamento em três níveis para minimizar o consumo da janela de contexto:

| Nível | Conteúdo | Quando Carregado | Custo em Tokens |
|-------|----------|------------------|-----------------|
| **1** | `name` + `description` | Sempre | ~130 tokens |
| **2** | Fluxo de trabalho SKILL.md | Ao acionar a skill | ~2.800 tokens |
| **3** | Documentos temáticos, scripts, páginas de versão | Sob demanda | Ilimitado |

Três **portões de parada de carregamento** explícitos previnem acúmulo desnecessário de contexto.

## Cobertura

### Sistemas GCAM

| Sistema | Tópicos Cobertos |
|---------|-----------------|
| Energia | Recursos fósseis/renováveis, eletricidade (segmentos de carga, resfriamento), hidrogênio (12 tecnologias), CCS, refino, integração de intermitentes |
| Terra | AgLU nested logit, GLUs, pré-processamento Moirai, contabilidade de carbono, bioenergia, pecuária, manejo florestal |
| Água | 6 setores de demanda, 235 bacias, competição de tecnologias de resfriamento, água subterrânea (Superwell), dessalinização |
| Economia | GDP exógeno/endógeno, produção KLEM CES, calibração SAM, feedback de preço de carbono |
| Emissões | 30+ espécies, curvas MAC, Hector v3.2.0 (permafrost), GWP AR4/AR5, mercados de GHG vinculados |
| Políticas | Imposto/restrição de carbono, RES/CES, target finder (7 tipos de meta), proteção de terras, empilhamento de múltiplas políticas |
| Comércio | Heckscher-Ohlin, Armington (21 setores com parâmetros logit), Fixed Trade, GCAM-USA interestadual |

### APIs de Ferramentas

| Ferramenta | Cobertura |
|------------|-----------|
| `gcamreader` (Python) | `Query`, `LocalDBConn`, `RemoteDBConn`, `runQuery`, `parse_batch_query`, modos CLI |
| `gcamextractor` (R) | `readgcam()` 16 parâmetros, 83+ valores `paramsSelect` em 14 grupos, cache `.Proj`, agregação regional |
| `rgcam` (R) | Resumo conceitual; sem código-fonte no projeto |
| ModelInterface | Geração de XML por comandos em lote headless |

### Suporte de Versões

22 versões de **v3.2** a **v8.7**, organizadas por família de documentação:

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1, v8.2 baseline)
- `delta-only` (v7.2--v7.4, v8.0--v8.1, v8.3--v8.7)

## Validação

A skill inclui 22 validadores automatizados que cobrem:

- Conformidade de contratos de documentos (frases obrigatórias, consciência de versão)
- Integridade de pacotes de páginas e paridade de conteúdo
- Higiene do sistema de arquivos e portabilidade multiplataforma
- Alinhamento de divulgação progressiva
- Cobertura de contratos semânticos (cada documento possui um validador)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## Documentação do Projeto

A memória persistente para contribuidores está em `docs/`:

- `PROJECT.md` -- escopo, decisões, tarefas pendentes
- `DEVELOPMENT.md` -- guia de fluxo de trabalho, taxonomia de scripts, portões de validação
- `CHANGELOG.md` -- registro de marcos
- `KNOWN_ISSUES.md` -- limitações e dívida técnica

## Licença

[MIT](LICENSE)

## Agradecimentos

Esta skill sintetiza conteúdo do ecossistema GCAM de código aberto:

- [GCAM](https://github.com/JGCRI/gcam-core) -- o Global Change Analysis Model (PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- documentação oficial do GCAM
- [gcamreader](https://github.com/JGCRI/gcamreader) -- interface de consulta Python
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- pacote de extração R
