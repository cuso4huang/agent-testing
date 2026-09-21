# 论文仓库整理方案

状态：已执行（结构迁移、入口索引和第一轮去重完成）  
制定日期：2026-09-21

## 1. 整理目标

把当前仓库从“按历次调研任务累积文件”调整为“按研究材料生命周期组织”，使读者能够快速回答四个问题：

1. 从哪里开始了解本研究领域；
2. 某篇论文的原文、元数据、证据等级和阅读笔记在哪里；
3. 某份综述或专题报告基于哪些证据；
4. 哪些文件是正式维护内容，哪些只是检索过程、临时文件或生成物。

本次整理不改变论文结论，不合并未经人工核验的内容，不因文件名相似而删除文件。

## 2. 当前状况

截至 2026-09-21，仓库约 440 MB，共 314 个非 Git 文件：

- Markdown 113 个；
- PDF 107 个；
- PPTX 18 个；
- PNG 33 个；
- CSV/JSON 等结构化数据 15 个；
- 其余为 HTML、DOCX、脚本和过程文件。

主要问题：

- 根目录有多份专题报告、阅读清单、HTML 转换结果和单篇 PDF，入口层职责过多；
- `research/` 同时容纳综述、专题报告、检索日志、检索结果、论文 PDF、笔记和证据表，层次不足；
- `toRead/` 既是精选阅读包，又保存了与 `research/papers/` 或其他目录内容相同的 PDF；
- `自己找的论文/` 表达的是来源而非材料角色，不利于长期维护；
- `output/` 混合最终交付物、演示文稿、图片和参考格式；
- 日期、语言和命名方式不统一，难以根据文件名判断材料类型和状态；
- README 所述核验日期和数量容易与后续增量调研脱节；
- 当前工作区存在未跟踪研究文件，整理时必须保留并单独登记，不能覆盖或误删。

已发现至少 6 组内容完全相同的 PDF 副本，涉及 MemoryAgentBench、AgentDoS、Process Evaluation、ATA、Les Dissonances 和 SIRAJ。它们只是候选去重项，执行前仍需检查链接和阅读包的独立分发需求。

## 3. 统一材料类型

后续目录和索引使用以下术语。它们描述材料在研究流程中的角色，而不是文件格式。

| 规范术语 | 定义 | 不应混入 |
| --- | --- | --- |
| 领域综述 | 对整个智能体测试领域的稳定综合叙述 | 单次增量检索结果、单篇论文笔记 |
| 专题报告 | 围绕一种方法、风险、会议范围或研究问题形成的综合分析 | 仅按日期堆叠的检索日志 |
| 论文笔记 | 一篇论文对应的一份结构化阅读记录 | 多篇论文的横向综合结论 |
| 证据记录 | 支撑纳入、排除、证据等级和核验状态的结构化事实 | 面向读者的叙述性报告 |
| 检索记录 | 可复现搜索所需的查询、时间、数据库和原始结果 | 已筛选、已综合的最终结论 |
| 原始论文 | 依法保存的论文全文或作者稿 | 阅读笔记、翻译或报告 |
| 阅读包 | 为特定学习路径选出的论文集合及导读 | 全量论文库的第二套长期副本 |
| 交付物 | 由源材料生成、面向展示或提交的 PDF、PPTX、DOCX 等 | 唯一可编辑源文件 |
| 临时材料 | 可重新生成、尚未核验或只服务一次处理的中间文件 | 长期引用的研究证据 |

在方案获确认前，这些术语仅为提议，不直接修改现有 `CONTEXT.md`。

## 4. 建议目标结构

```text
.
├── README.md                         # 唯一总入口
├── CONTEXT.md                        # 领域术语表
├── CONTRIBUTING.md                   # 新论文和报告的维护流程
├── docs/
│   ├── repository-organization-plan.md
│   └── portfolio/                    # 工程实践与作品集材料
├── literature/
│   ├── papers/                       # 原始论文的唯一长期存放处
│   ├── notes/                        # 一篇论文一份笔记
│   ├── evidence/                     # 证据表、筛选表、核验例外
│   ├── bibliography/                 # references.bib 与引用规范
│   └── reading-packs/                # 阅读路线和清单，优先链接 papers/
├── reviews/
│   ├── overview/                     # 稳定的领域综述和研究进展入口
│   ├── topics/                       # 方法、风险、轨迹、回归测试等专题
│   └── audits/                       # 顶会复查、代码审计、覆盖度审计
├── searches/
│   ├── logs/                         # 人类可读检索日志
│   └── runs/YYYY-MM-DD-主题/         # CSV、JSON 等原始检索结果
├── assets/
│   └── source/                       # 合法保留的 HTML 等外部源材料
├── outputs/
│   ├── presentations/                # PPTX 及其渲染图
│   ├── reports/                      # 生成的 PDF/DOCX
│   └── examples/                     # 参考格式
├── scripts/                          # 数据整理和一致性检查脚本
└── tmp/                              # 可删除、可再生成；默认不纳入版本控制
```

### 结构原则

- 根目录只保留项目入口、规范和少数项目级配置；
- 一篇论文只保留一个规范 PDF，阅读包通过相对链接引用；
- Markdown 源文件与 PDF/PPTX/DOCX 交付物分离；
- 按“内容角色”分类，不按“谁找到的”“某次任务”分类；
- 日期只表达版本或检索批次，不替代内容类型；
- 所有综合报告都能回溯到证据表、论文笔记或检索记录。

## 5. 现有内容迁移映射

| 当前内容 | 建议位置 | 处理方式 |
| --- | --- | --- |
| `research/papers/*.pdf` | `literature/papers/` | 作为规范论文库基线 |
| `research/notes/*.md` | `literature/notes/` | 保持现有规范命名 |
| `research/evidence/*` | `literature/evidence/` | 保留 CSV 字段和历史 |
| `research/references.bib` | `literature/bibliography/references.bib` | 更新所有引用路径 |
| `toRead/` | `literature/reading-packs/core-agent-testing/` | README 和笔记保留；重复 PDF 改为链接 |
| `自己找的论文/` | `literature/papers/` 或 `tmp/inbox/` | 已核验者规范化入库，未核验者进入收件箱 |
| `research/search-*`、`research/live-*` | `searches/runs/` | 以日期和主题分批保存 |
| `research/search-log.md` 等 | `searches/logs/` | 合并索引，不强行合并原始记录 |
| `research/*review*.md` | `reviews/overview/` 或 `reviews/topics/` | 依据覆盖范围分类 |
| 顶会复查、代码审计、覆盖审计 | `reviews/audits/` | 统一标注审计日期和范围 |
| 轨迹、回归测试、Fuzzing 等报告 | `reviews/topics/<topic>/` | 每个专题设 README 索引 |
| 根目录 MinerU HTML | `assets/source/` | 标明来源、生成方式和语言版本 |
| `output/` | `outputs/` | 按演示文稿、报告、示例重新分层 |
| `tmp/` | `tmp/` | 检查引用后加入忽略规则或清空；不立即删除 |

## 6. 命名规范

### 论文与论文笔记

```text
YYYY-FirstAuthor-ShortTitle.pdf
YYYY-FirstAuthor-ShortTitle.md
```

- 年份采用所保存版本对应的发表年；预印本与正式版本冲突时在元数据中说明；
- `ShortTitle` 使用稳定英文短名，避免会议下载编号；
- PDF 与笔记使用同一 stem，便于自动检查一一对应关系；
- 同名不同版本追加 `-arxiv`、`-conference` 或版本日期，不能静默覆盖。

### 报告、审计和检索批次

```text
YYYY-MM-DD-topic-purpose.md
YYYY-MM-DD-topic-search/
```

- `topic` 表达研究主题；`purpose` 使用 `review`、`reading-guide`、`audit`、`deep-dive` 等受控词；
- 稳定维护的领域总览可不带日期，但正文必须记录“证据核验截至日期”；
- 中文标题放在文档一级标题中，文件名采用可预测的英文 slug，减少跨平台路径问题。

## 7. 索引与元数据设计

建议建立三个入口：

1. 根 `README.md`：面向新读者，提供三条阅读路线——快速入门、研究选题、证据核查；
2. `literature/README.md`：面向资料维护者，说明论文、笔记、证据和 BibTeX 的关系；
3. `reviews/README.md`：列出领域综述、专题报告、审计及其状态。

每份综合报告的文首统一加入轻量元数据：

```yaml
---
title: 中文标题
type: overview | topic-review | audit | reading-guide | deep-dive
status: draft | active | superseded | archived
evidence_checked_through: YYYY-MM-DD
supersedes: []
related_evidence: []
---
```

论文级事实继续以证据表和 BibTeX 为权威来源，不在多个 Markdown 索引中复制维护。

## 8. 分阶段执行计划

### 阶段 0：冻结与清单

- 保存当前 Git 状态，登记所有未跟踪文件；
- 导出全量文件清单、大小、SHA-256 和被 Markdown 引用关系；
- 标记相同内容副本、孤立文件和断链，但不做删除；
- 确定哪些大文件由 Git、Git LFS 或仓库外存储管理。

产物：`inventory.csv`、重复文件候选表、断链报告。

### 阶段 1：术语和权威来源

- 用户确认第 3 节的材料类型；
- 将确认后的术语写入 `CONTEXT.md`；
- 明确各类数据的唯一权威来源：论文事实为证据表，引用为 BibTeX，领域叙述为主综述；
- 为职责重叠的报告标注 `active`、`superseded` 或 `archived`。

产物：更新后的术语表、报告状态表。

### 阶段 2：先建索引，不移动内容

- 创建 `literature/README.md` 与 `reviews/README.md`；
- 给现有报告补充类型、状态和核验日期；
- 在根 README 中提供清晰阅读路线；
- 通过索引暴露重叠和缺失，再确认迁移映射。

产物：可用的新导航系统，旧路径仍完全有效。

### 阶段 3：机械迁移

- 使用 `git mv` 分小批迁移，每批只处理一种材料；
- 每批迁移后更新 Markdown 链接并运行断链检查；
- 优先迁移低风险内容：检索运行、输出、HTML；
- 然后迁移报告和论文资料；
- 暂不处理重复 PDF 的删除。

建议提交顺序：目录骨架 → 检索记录 → 输出物 → 报告 → 论文与笔记 → 链接修复。

### 阶段 4：去重与归档

- 对 SHA-256 相同的 PDF，选定 `literature/papers/` 为规范副本；
- 阅读包改用相对链接，或在确需独立分发时保留副本并记录原因；
- 将被新版取代但仍有历史价值的报告标为归档，不立即删除；
- 对未核验论文先放入 `tmp/inbox/`，完成元数据与全文核验后再入库。

产物：去重记录、归档索引、体积变化报告。

### 阶段 5：自动化维护

- 添加链接检查；
- 检查 PDF 与论文笔记的命名对应；
- 检查 BibTeX key、DOI/arXiv ID 和证据表唯一性；
- 检查报告元数据字段和日期；
- 在 CONTRIBUTING 中记录新增论文的标准流程。

产物：可重复运行的仓库健康检查和维护说明。

## 9. 安全规则

- 不覆盖用户当前未跟踪文件；
- 不凭标题相似判断重复，只用哈希确认文件相同，再人工判断语义版本；
- 不删除带批注、翻译或不同分页的 PDF；
- 不在同一个提交中同时移动文件和大幅改写内容；
- 每批迁移后检查 Git diff、内部链接和关键入口；
- 对外部版权材料保持现有使用边界，不把去重理解为重新分发；
- 所有归档和删除动作必须有可恢复的 Git 历史或明确备份。

## 10. 验收标准

整理完成后应满足：

- 根目录除入口和项目级规范外不再散落研究材料；
- 新读者从 README 最多两次点击可到达主综述、阅读包、研究方向和证据表；
- 任意已纳入论文能够关联到 PDF、BibTeX、证据记录及已有笔记；
- 每份综合报告都标明类型、状态、证据核验日期和相关证据；
- 仓库内 Markdown 相对链接无断链；
- 完全相同的论文 PDF 原则上只有一个规范副本；
- `tmp/` 中没有被正式报告依赖的唯一材料；
- 新论文从“待核验”到“已纳入”的维护流程有文档可循；
- README 中的数量由脚本生成或能通过单一命令复核。

## 11. 建议决策

执行前需要确认三项偏好：

1. 目录名是否统一使用英文，以获得更稳定的脚本和跨平台路径；
2. 论文 PDF 是否继续纳入 Git，还是迁移到 Git LFS/外部文献管理器；
3. 阅读包是否需要作为可独立复制的离线包；如果需要，其重复 PDF 应作为有意副本保留。

默认建议：目录名使用英文；本轮不改变 PDF 的存储方式；阅读包保留导读与笔记，但论文正文链接到唯一论文库。

## 12. 执行记录（2026-09-21）

- 已建立 `literature/`、`reviews/`、`searches/`、`outputs/`、`assets/` 和 `scripts/` 目录；
- 已将原 `research/` 的笔记、证据、引用、报告和检索结果按材料角色迁移；
- 已将精选阅读包迁移到 `literature/reading-packs/core-agent-testing/`，PDF 链接统一指向规范论文库；
- 已移除 4 份经 SHA-256 确认的“自己找的论文”重复副本，并记录在 [`reorganization-dedup.md`](reorganization-dedup.md)；
- 已更新 README、调研规范、脚本路径和跨文档引用；
- 已生成按区域统计的 [`reorganization-inventory.csv`](reorganization-inventory.csv)；
- 已通过本地 Markdown 链接检查（`MISSING=0`）和精选阅读包 SHA-256 校验；
- 尚未做报告级 YAML 元数据补齐、PDF 外部存储迁移和自动化健康检查脚本，这些属于后续维护批次。
