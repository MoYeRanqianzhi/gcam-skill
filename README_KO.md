🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

이식 가능하고 자체 완결형인 AI 에이전트 스킬로, [전지구 변화 분석 모델(GCAM)](https://github.com/JGCRI/gcam-core)을 지원합니다. 로컬에 모델을 설치하지 않고도 포괄적이고 버전 인식이 가능한 GCAM 전문 지식을 제공합니다.

## 기능 개요

본 스킬은 AI 에이전트(Claude 등)에 GCAM 전체 생태계에 대한 심층 지식을 제공합니다:

- **모델 구조** -- 에너지, 토지, 수자원, 경제, 배출 및 기후 시스템
- **22개 GCAM 버전**(v3.2~v8.7), 버전 인식 라우팅 및 버전별 문서 지원
- **시나리오 구성** -- XML 편집, 정책 설계, target-finder 모드, 배치 실행
- **데이터 추출** -- Python (`gcamreader`) 및 R (`gcamextractor`) API 레퍼런스, 83개 이상의 추출 매개변수 수록
- **시나리오 분석** -- 다중 시나리오 비교 워크플로, 시각화 패턴, 일반적인 분석 템플릿
- **빌드 및 설치** -- 릴리스 다운로드, 소스 컴파일, 워크스페이스 관리

## 설치

다음 내용을 AI 에이전트(Claude Code, Codex, Cursor 등)에 전송하면 설치됩니다:

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

## 빠른 시작

설치가 완료되면, 에이전트에서 GCAM 관련 질문을 바로 할 수 있습니다:

```
> How do I set up a carbon tax scenario in GCAM v8.2?
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> What changed in the land system between v5.4 and v7.1?
```

스킬은 GCAM 관련 쿼리를 자동으로 인식하여 올바른 버전 문서로 라우팅합니다.

### 개발자 사용법

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

스킬 무결성 검증:

```bash
python skills/gacm/scripts/validate_all.py
```

## 아키텍처

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

### 점진적 공개(Progressive Disclosure)

본 스킬은 컨텍스트 윈도우 소비를 최소화하기 위해 3단계 로딩 시스템을 사용합니다:

| 단계 | 내용 | 로드 시점 | 토큰 비용 |
|------|------|-----------|-----------|
| **1** | `name` + `description` | 항상 로드 | ~130 tokens |
| **2** | SKILL.md 워크플로 | 스킬 트리거 시 | ~2,800 tokens |
| **3** | 주제 문서, 스크립트, 버전 페이지 | 필요 시 로드 | 무제한 |

세 개의 명시적 **로딩 중단 게이트**가 불필요한 컨텍스트 누적을 방지합니다.

## 커버리지

### GCAM 시스템 모듈

| 시스템 | 다루는 주제 |
|--------|-------------|
| 에너지 | 화석/재생 가능 자원, 전력(부하 구간, 냉각), 수소(12개 기술), CCS, 정유, 간헐성 통합 |
| 토지 | AgLU 중첩 로짓, GLU, Moirai 전처리, 탄소 회계, 바이오에너지, 축산업, 산림 관리 |
| 수자원 | 6개 수요 부문, 235개 유역, 냉각 기술 경쟁, 지하수(Superwell), 해수 담수화 |
| 경제 | 외생/내생 GDP, KLEM CES 생산함수, SAM 보정, 탄소 가격 피드백 |
| 배출 | 30개 이상의 배출 물질, MAC 곡선, Hector v3.2.0(영구동토층), GWP AR4/AR5, 연계 GHG 시장 |
| 정책 | 탄소세/제약, RES/CES, target finder(7개 목표 유형), 토지 보호, 다중 정책 중첩 |
| 무역 | Heckscher-Ohlin, Armington(로짓 파라미터를 포함한 21개 부문), 고정 무역, GCAM-USA 주간 무역 |

### 도구 API

| 도구 | 커버리지 |
|------|----------|
| `gcamreader` (Python) | `Query`, `LocalDBConn`, `RemoteDBConn`, `runQuery`, `parse_batch_query`, CLI 모드 |
| `gcamextractor` (R) | `readgcam()` 16개 매개변수, 83개 이상의 `paramsSelect` 값(14개 그룹), `.Proj` 캐싱, 지역 집계 |
| `rgcam` (R) | 개념 요약 |
| ModelInterface | 헤드리스 배치 커맨드 XML 생성 |

### 버전 지원

**v3.2**부터 **v8.7**까지 22개 버전을 지원하며, 문서 계열별로 구성됩니다:

- `legacy-wiki` (v3.2)
- `compact-modern` (v4.2--v4.4)
- `modern-transitional` (v5.1--v5.3)
- `modern-comprehensive` (v5.4--v7.1, v8.2 기준선)
- `delta-only` (v7.2--v7.4, v8.0--v8.1, v8.3--v8.7)

## 검증

22개의 자동화 검증기를 포함하며, 다음을 검증합니다:

- 문서 계약 준수(필수 구문, 버전 인식)
- 페이지 번들 무결성 및 콘텐츠 동등성
- 파일 시스템 위생 및 크로스 플랫폼 이식성
- 점진적 공개 정합성
- 시맨틱 계약 커버리지(모든 문서에 대한 검증기 존재)

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## 프로젝트 문서

기여자를 위한 영속적 메모리는 `docs/`에 있습니다:

- `PROJECT.md` -- 범위, 의사결정, 미완료 작업
- `DEVELOPMENT.md` -- 워크플로 가이드, 스크립트 분류, 검증 게이트
- `CHANGELOG.md` -- 마일스톤 로그
- `KNOWN_ISSUES.md` -- 알려진 제한 사항 및 기술 부채

## 라이선스

[MIT](LICENSE)

## 감사의 말

본 스킬은 오픈소스 GCAM 생태계의 콘텐츠를 종합하여 구성되었습니다:

- [GCAM](https://github.com/JGCRI/gcam-core) -- 전지구 변화 분석 모델(PNNL/JGCRI)
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- GCAM 공식 문서
- [gcamreader](https://github.com/JGCRI/gcamreader) -- Python 쿼리 인터페이스
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- R 추출 패키지
