🌐 [English](README.md) | [中文](README_CN.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md) | [Deutsch](README_DE.md) | [Português](README_PT.md) | [Русский](README_RU.md) | [العربية](README_AR.md)

# GCAM Skill (`gacm`)

ポータブルかつ自己完結型の AI エージェントスキルで、[Global Change Analysis Model (GCAM)](https://github.com/JGCRI/gcam-core) に対応しています。ローカルにモデルをインストールすることなく、バージョンを意識した包括的な GCAM の専門知識を提供します。

## 機能概要

本スキルは AI エージェント（Claude 等）に GCAM エコシステム全体の深い知識を提供します：

- **モデル構造** -- エネルギー、土地、水資源、経済、排出、気候システム
- **22 の GCAM バージョン**（v3.2 から v8.7）に対応し、バージョン固有のルーティングとドキュメントを提供
- **シナリオ設定** -- XML 編集、政策設計、target-finder モード、バッチ実行
- **データ抽出** -- Python (`gcamreader`) および R (`gcamextractor`) の API リファレンス、83 以上の抽出パラメータを文書化
- **シナリオ分析** -- マルチシナリオ比較ワークフロー、可視化パターン、一般的な分析テンプレート
- **ビルドとインストール** -- リリースのダウンロード、ソースコンパイル、ワークスペース管理

## インストール

以下の内容を AI エージェント（Claude Code、Codex、Cursor 等）に送信してください：

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

## クイックスタート

インストール完了後、エージェントに GCAM 関連の質問をするだけで利用できます：

```
> Set up a carbon tax scenario in GCAM v8.2
> Compare SSP2 and SSP5 energy system outcomes
> Extract electricity generation by technology using gcamreader
> Analyze land system changes between v5.4 and v7.1
```

スキルは GCAM 関連のクエリを自動的に検出し、適切なバージョンのドキュメントにルーティングします。

### 開発者向け

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

スキルの整合性を検証：

```bash
python skills/gacm/scripts/validate_all.py
```

## アーキテクチャ

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

### プログレッシブ・ディスクロージャ（段階的開示）

本スキルは 3 段階のローディングシステムを使用し、コンテキストウィンドウの消費を最小限に抑えます：

| レベル | 内容 | ロードタイミング | トークンコスト |
|--------|------|------------------|----------------|
| **1** | `name` + `description` | 常時 | 約 130 トークン |
| **2** | SKILL.md ワークフロー | スキル起動時 | 約 2,800 トークン |
| **3** | トピックドキュメント、スクリプト、バージョンページ | オンデマンド | 無制限 |

3 つの明示的な**ローディング停止ゲート**により、不要なコンテキストの蓄積を防止します。

## カバレッジ

### GCAM システムモジュール

| システム | カバー範囲 |
|----------|-----------|
| エネルギー | 化石・再生可能エネルギー資源、電力（負荷セグメント、冷却）、水素（12 技術）、CCS、精製、間欠性統合 |
| 土地 | AgLU ネステッドロジット、GLU、Moirai 前処理、炭素会計、バイオエネルギー、畜産、森林管理 |
| 水資源 | 6 需要セクター、235 流域、冷却技術競合、地下水（Superwell）、淡水化 |
| 経済 | 外生・内生 GDP、KLEM CES 生産関数、SAM キャリブレーション、炭素価格フィードバック |
| 排出 | 30 種以上、MAC 曲線、Hector v3.2.0（永久凍土）、GWP AR4/AR5、連結 GHG 市場 |
| 政策 | 炭素税・制約、RES/CES、target finder（7 種の目標タイプ）、土地保護、マルチポリシー重畳 |
| 貿易 | Heckscher-Ohlin、Armington（21 セクター、logit パラメータ付き）、固定貿易、GCAM-USA 州間 |

### コンパニオンツール API

| ツール | カバレッジ |
|--------|-----------|
| `gcamreader` (Python) | `Query`、`LocalDBConn`、`RemoteDBConn`、`runQuery`、`parse_batch_query`、CLI モード |
| `gcamextractor` (R) | `readgcam()` 16 パラメータ、83 以上の `paramsSelect` 値（14 グループ）、`.Proj` キャッシュ、地域集約 |
| `rgcam` (R) | 概念的サマリー（プロジェクト内にソースなし） |
| ModelInterface | ヘッドレスバッチコマンド XML 生成 |

### バージョンサポート

**v3.2** から **v8.7** まで 22 バージョンをサポート。ドキュメントファミリーごとに整理：

- `legacy-wiki`（v3.2）
- `compact-modern`（v4.2--v4.4）
- `modern-transitional`（v5.1--v5.3）
- `modern-comprehensive`（v5.4--v7.1、v8.2 ベースライン）
- `delta-only`（v7.2--v7.4、v8.0--v8.1、v8.3--v8.7）

## バリデーション

22 の自動バリデータを備え、以下をカバーします：

- ドキュメント契約準拠（必須フレーズ、バージョン認識）
- ページバンドルの整合性とコンテンツの一貫性
- ファイルシステムの衛生管理とクロスプラットフォーム移植性
- プログレッシブ・ディスクロージャの整合性
- セマンティック契約カバレッジ（各ドキュメントにバリデータあり）

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## プロジェクトドキュメント

コントリビューター向けの永続化メモリは `docs/` に格納されています：

- `PROJECT.md` -- スコープ、意思決定、未完了タスク
- `DEVELOPMENT.md` -- ワークフローガイド、スクリプト分類、バリデーションゲート
- `CHANGELOG.md` -- マイルストーンログ
- `KNOWN_ISSUES.md` -- 既知の制限事項と技術的負債

## ライセンス

[MIT](LICENSE)

## 謝辞

本スキルはオープンソースの GCAM エコシステムのコンテンツを統合したものです：

- [GCAM](https://github.com/JGCRI/gcam-core) -- Global Change Analysis Model（PNNL/JGCRI）
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- GCAM 公式ドキュメント
- [gcamreader](https://github.com/JGCRI/gcamreader) -- Python クエリインターフェース
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- R 抽出パッケージ
