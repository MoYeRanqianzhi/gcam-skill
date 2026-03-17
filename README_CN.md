# GCAM Skill (`gacm`)

一个可移植的、自包含的 AI Agent Skill，用于 [全球变化分析模型 (GCAM)](https://github.com/JGCRI/gcam-core)。无需本地安装 GCAM 即可为 AI Agent 提供完整的 GCAM 专业知识。

## 功能概述

本 Skill 为 AI Agent（Claude 等）提供 GCAM 全生态系统的深度知识：

- **模型结构** -- 能源、土地、水资源、经济、排放与气候系统
- **22 个 GCAM 版本**（v3.2 至 v8.7），支持版本感知路由和版本特定文档
- **情景配置** -- XML 编辑、政策设计、target-finder 模式、批处理运行
- **数据提取** -- Python (`gcamreader`) 和 R (`gcamextractor`) API 参考，涵盖 83+ 个提取参数
- **情景分析** -- 多情景对比工作流、可视化模式、常见分析模板
- **构建与安装** -- 发布包下载、源码编译、工作空间管理

## 安装

将以下内容发送给你的 AI Agent（Claude Code、Codex、Cursor 等）即可安装：

```
Read this repository's README and install the GCAM Skill:
https://github.com/MoYeRanqianzhi/gcam-skill
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

## 快速开始

安装完成后，在 Agent 中直接提问 GCAM 相关问题：

```
> 如何在 GCAM v8.2 中设置碳税情景？
> 比较 SSP2 和 SSP5 的能源系统结果
> 使用 gcamreader 提取各技术的发电量
> v5.4 到 v7.1 之间土地系统有什么变化？
```

Skill 会自动识别 GCAM 相关查询并路由到正确的版本文档。

### 开发者使用

```bash
git clone https://github.com/MoYeRanqianzhi/gcam-skill.git
cd gcam-skill
```

验证 Skill 完整性：

```bash
python skills/gacm/scripts/validate_all.py
```

## 架构

```
skills/gacm/
├── SKILL.md                    # SOP -- Agent 工作流、版本路由、渐进式披露
├── scripts/                    # 28 个 Python 脚本（2 运行时、3 生成器、23 验证器）
│   ├── doc_search.py           # 运行时：按版本/模式搜索捆绑参考
│   ├── version_catalog.py      # 运行时：版本注册表和版本族元数据
│   ├── generate_bundled_pages.py
│   └── validate_all.py         # 一键验证套件
└── reference/                  # 33 个主题文档 + 22 个版本捆绑包
    ├── overview.md             # 模型结构和核心概念
    ├── energy_system.md        # 资源、电力、氢能、CCS、需求
    ├── land_system.md          # AgLU、GLU 嵌套、Moirai、碳核算
    ├── water_system.md         # 235 个流域、冷却技术、水-能-食 Nexus
    ├── economy.md              # GDP、KLEM、GCAM-macro、SAM 校准
    ├── emissions_climate.md    # CO2/非CO2、MAC 曲线、Hector、GWP、IAMC
    ├── policies_scenarios.md   # 碳税、RES、target finder、XML 示例
    ├── trade.md                # Armington、Heckscher-Ohlin、商品分配
    ├── scenario_analysis.md    # Python/R 多情景对比工作流
    ├── gcamreader_api.md       # Python Query/Connection API 参考
    ├── gcamextractor_api.md    # R readgcam() 83+ 参数、14 个分组
    ├── ssp.md                  # SSP1-5 叙事、量化假设
    ├── gcam_usa.md             # 51 州子国家级扩展
    ├── versions/               # 22 个版本路由文件（v3.2--v8.7）
    └── version_pages/          # 614 个捆绑版本页面 Markdown 文件
```

### 渐进式披露（Progressive Disclosure）

本 Skill 使用三级加载系统，最小化上下文窗口消耗：

| 层级 | 内容 | 加载时机 | Token 消耗 |
|------|------|----------|-----------|
| **1** | `name` + `description` | 始终加载 | ~130 tokens |
| **2** | SKILL.md 工作流 | Skill 触发时 | ~2,800 tokens |
| **3** | 主题文档、脚本、版本页面 | 按需加载 | 无限制 |

三个显式的**停止加载门控**防止不必要的上下文累积。

## 覆盖范围

### GCAM 系统模块

| 系统 | 覆盖内容 |
|------|----------|
| 能源 | 化石/可再生资源、电力（负荷段、冷却）、氢能（12 种技术）、CCS、炼油、间歇性整合 |
| 土地 | AgLU 嵌套 logit、GLU、Moirai 预处理、碳核算、生物能源、畜牧业、森林管理 |
| 水资源 | 6 大需求部门、235 个流域、冷却技术竞争、地下水（Superwell）、海水淡化 |
| 经济 | 外生/内生 GDP、KLEM CES 生产函数、SAM 校准、碳价反馈 |
| 排放 | 30+ 种排放物、MAC 曲线、Hector v3.2.0（永冻层）、GWP AR4/AR5、链接 GHG 市场 |
| 政策 | 碳税/约束、RES/CES、target finder（7 种目标类型）、土地保护、多政策叠加 |
| 贸易 | Heckscher-Ohlin、Armington（21 个部门含 logit 参数）、固定贸易、GCAM-USA 州际贸易 |

### 配套工具 API

| 工具 | 覆盖范围 |
|------|----------|
| `gcamreader` (Python) | `Query`、`LocalDBConn`、`RemoteDBConn`、`runQuery`、`parse_batch_query`、CLI 模式 |
| `gcamextractor` (R) | `readgcam()` 16 参数、83+ 个 `paramsSelect` 值（14 个分组）、`.Proj` 缓存、区域聚合 |
| `rgcam` (R) | 概念摘要 |
| ModelInterface | 无头批处理命令 XML 生成 |

### 版本支持

支持 22 个版本，从 **v3.2** 到 **v8.7**，按文档族组织：

- `legacy-wiki`（v3.2）
- `compact-modern`（v4.2--v4.4）
- `modern-transitional`（v5.1--v5.3）
- `modern-comprehensive`（v5.4--v7.1、v8.2 基线）
- `delta-only`（v7.2--v7.4、v8.0--v8.1、v8.3--v8.7）

## 验证体系

包含 22 个自动化验证器，覆盖：

- 文档合约合规性（必要短语、版本感知）
- 页面捆绑包完整性和内容一致性
- 文件系统卫生和跨平台可移植性
- 渐进式披露对齐
- 语义合约覆盖（每个文档都有验证器）

```bash
python skills/gacm/scripts/validate_all.py
# All GCAM skill validations passed.
```

## 项目文档

贡献者持久化记忆位于 `docs/`：

- `PROJECT.md` -- 范围、决策、待办事项
- `DEVELOPMENT.md` -- 工作流指南、脚本分类、验证门控
- `CHANGELOG.md` -- 里程碑日志
- `KNOWN_ISSUES.md` -- 已知限制和技术债务

## 许可证

[MIT](LICENSE)

## 致谢

本 Skill 综合了开源 GCAM 生态系统的内容：

- [GCAM](https://github.com/JGCRI/gcam-core) -- 全球变化分析模型（PNNL/JGCRI）
- [gcam-doc](https://github.com/JGCRI/gcam-doc) -- GCAM 官方文档
- [gcamreader](https://github.com/JGCRI/gcamreader) -- Python 查询接口
- [gcamextractor](https://github.com/JGCRI/gcamextractor) -- R 提取包
