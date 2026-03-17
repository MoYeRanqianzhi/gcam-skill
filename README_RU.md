🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

Портативный, автономный навык (Skill) для AI-агентов, предназначенный для работы с [Global Change Analysis Model (GCAM)](https://github.com/JGCRI/gcam-core). Предоставляет исчерпывающую, версионно-зависимую экспертизу по GCAM без необходимости локальной установки модели.

## Обзор функций

Данный Skill обеспечивает AI-агентов (Claude и др.) глубокими знаниями всей экосистемы GCAM:

- **Структура модели** -- системы энергетики, землепользования, водных ресурсов, экономики, выбросов и климата
- **22 версии GCAM** (от v3.2 до v8.7) с версионно-зависимой маршрутизацией и документацией
- **Конфигурация сценариев** -- редактирование XML, проектирование политик, режим target-finder, пакетные запуски
- **Извлечение данных** -- справочники API для Python (`gcamreader`) и R (`gcamextractor`) с 83+ документированными параметрами извлечения
- **Анализ сценариев** -- рабочие процессы многосценарного сравнения, шаблоны визуализации, типовые аналитические шаблоны
- **Сборка и установка** -- загрузка релизов, компиляция из исходников, управление рабочим пространством

## Установка

Отправьте следующее сообщение вашему AI-агенту (Claude Code, Codex, Cursor и др.) для установки:

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

## Быстрый старт

После установки просто задавайте вопросы, связанные с GCAM, в вашем агенте:

```
> How do I set up a carbon tax scenario in GCAM v8.2?
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> What changed in the land system between v5.4 and v7.1?
```

Skill автоматически активируется при запросах, связанных с GCAM, и направляет к документации нужной версии.

### Для разработчиков

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

Проверка целостности Skill:

```bash
python skills/gacm/scripts/validate_all.py
```

## Архитектура

```
skills/gacm/
├── SKILL.md                    # SOP -- рабочий процесс агента, версионная маршрутизация, прогрессивное раскрытие
├── scripts/                    # 28 Python-скриптов (2 runtime, 3 генератора, 23 валидатора)
│   ├── doc_search.py           # Runtime: поиск по bundled references по версии/паттерну
│   ├── version_catalog.py      # Runtime: реестр версий и метаданные семейств
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # One-shot validation suite
└── reference/                  # 33 тематических документа + 22 версионных пакета
    ├── overview.md             # Структура модели и ключевые концепции
    ├── energy_system.md        # Ресурсы, электроэнергия, водород, CCS, спрос
    ├── land_system.md          # AgLU, GLU nesting, Moirai, углеродный учёт
    ├── water_system.md         # 235 бассейнов, технологии охлаждения, nexus вода-энергия-продовольствие
    ├── economy.md              # GDP, KLEM, GCAM-macro, калибровка SAM
    ├── emissions_climate.md    # CO2/не-CO2, MAC-кривые, Hector, GWP, IAMC
    ├── policies_scenarios.md   # Углеродный налог, RES, target finder, XML-примеры
    ├── trade.md                # Armington, Heckscher-Ohlin, товарные назначения
    ├── scenario_analysis.md    # Python/R рабочие процессы многосценарного сравнения
    ├── gcamreader_api.md       # Python Query/Connection API reference
    ├── gcamextractor_api.md    # R readgcam() с 83+ параметрами, 14 групп
    ├── ssp.md                  # SSP1-5 нарративы, количественные допущения
    ├── gcam_usa.md             # 51-штатное субнациональное расширение
    ├── versions/               # 22 версионных файла маршрутизации (v3.2--v8.7)
    └── version_pages/          # 614 bundled version-page markdown-файлов
```

### Прогрессивное раскрытие (Progressive Disclosure)

Skill использует трёхуровневую систему загрузки для минимизации потребления контекстного окна:

| Уровень | Содержимое | Момент загрузки | Стоимость в токенах |
|---------|-----------|-----------------|---------------------|
| **1** | `name` + `description` | Всегда | ~130 tokens |
| **2** | SKILL.md (рабочий процесс) | При активации Skill | ~2,800 tokens |
| **3** | Тематические документы, скрипты, версионные страницы | По запросу | Без ограничений |

Три явных **шлюза остановки загрузки** предотвращают ненужное накопление контекста.

## Покрытие

### Системы GCAM

| Система | Покрываемые темы |
|---------|-----------------|
| Энергетика | Ископаемые/возобновляемые ресурсы, электроэнергия (сегменты нагрузки, охлаждение), водород (12 технологий), CCS, нефтепереработка, интеграция прерывистой генерации |
| Землепользование | AgLU nested logit, GLU, препроцессинг Moirai, углеродный учёт, биоэнергетика, животноводство, лесоуправление |
| Водные ресурсы | 6 секторов спроса, 235 бассейнов, конкуренция технологий охлаждения, подземные воды (Superwell), опреснение |
| Экономика | Экзогенный/эндогенный GDP, KLEM CES производственная функция, калибровка SAM, обратная связь углеродной цены |
| Выбросы | 30+ видов, MAC-кривые, Hector v3.2.0 (вечная мерзлота), GWP AR4/AR5, связанные рынки GHG |
| Политика | Углеродный налог/ограничение, RES/CES, target finder (7 типов целей), охрана земель, многоуровневое наложение политик |
| Торговля | Heckscher-Ohlin, Armington (21 сектор с logit-параметрами), Fixed Trade, GCAM-USA межштатная торговля |

### API инструментов

| Инструмент | Покрытие |
|------------|----------|
| `gcamreader` (Python) | `Query`, `LocalDBConn`, `RemoteDBConn`, `runQuery`, `parse_batch_query`, CLI modes |
| `gcamextractor` (R) | `readgcam()` 16 параметров, 83+ значений `paramsSelect` по 14 группам, кэширование `.Proj`, региональная агрегация |
| `rgcam` (R) | Концептуальная справка; исходный код в проекте отсутствует |
| ModelInterface | Генерация XML команд headless batch |

### Поддержка версий

22 версии от **v3.2** до **v8.7**, организованные по семействам документации:

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1, v8.2 baseline)
- `delta-only` (v7.2--v7.4, v8.0--v8.1, v8.3--v8.7)

## Валидация

Skill включает 22 автоматизированных валидатора, охватывающих:

- Соответствие контрактам документов (обязательные фразы, версионная осведомлённость)
- Целостность пакетов страниц и согласованность содержимого
- Гигиена файловой системы и кроссплатформенная переносимость
- Согласованность с прогрессивным раскрытием
- Покрытие семантических контрактов (для каждого документа есть валидатор)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## Документация проекта

Персистентная память для участников проекта находится в `docs/`:

- `PROJECT.md` -- область, решения, открытые задачи
- `DEVELOPMENT.md` -- руководство по рабочему процессу, таксономия скриптов, шлюзы валидации
- `CHANGELOG.md` -- журнал вех
- `KNOWN_ISSUES.md` -- известные ограничения и технический долг

## Лицензия

[MIT](LICENSE)

## Благодарности

Данный Skill синтезирует материалы из открытой экосистемы GCAM:

- [GCAM](https://github.com/JGCRI/gcam-core) -- Global Change Analysis Model (PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- официальная документация GCAM
- [gcamreader](https://github.com/JGCRI/gcamreader) -- Python-интерфейс для запросов
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- R-пакет для извлечения данных
