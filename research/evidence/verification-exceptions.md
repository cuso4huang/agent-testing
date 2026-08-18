# 核验例外与受限证据清单

> 截止 2026-08-14。本文件是便于人工检查的摘要；逐篇状态以 `evidence-table.csv` 为准。

## 正式元数据仍待核验

- **AgentSpec**：已找到论文/正式身份线索，但精确 DOI 尚未进入或未能从 Crossref 获得；只按摘要级证据使用。
- **AgentCollabBench、STATE-Bench、AgentLAB、Counsel**：项目页、数据页或报告可访问，但正式出版身份和 DOI 未核验；均为 watchlist。
- **AJ-Bench（已解决）**：现已核验 Findings of ACL 2026 正式版本，DOI `10.18653/v1/2026.findings-acl.1269`；Crossref 与 OpenAlex 题名、年份和 DOI 一致，已从 watchlist 升级为全文核心方法证据。
- **Adaptive Adversaries**：数据集及会议声明已检查，最终出版元数据仍待确认；为 watchlist。

以上条目不在 BibTeX 中虚构作者、DOI 或会议字段。只有可核验字段才写入 `references.bib`。

## 仅有摘要或未完成全文核验

证据表中 `evidence_level=仅阅读摘要` 的 44 条记录不用于支撑具体实验数字或细粒度方法结论。其中需要优先补全文的 16 条 watchlist 是：

1. VeriGrey
2. FLARE
3. LogicHunter
4. AgentLens
5. Benchmarking LLM Judges for Mobile Agent Evaluation
6. AgentCollabBench
7. Adaptive Adversaries
8. STATE-Bench
9. AgentLAB
10. Counsel
11. Can LLM Agents Stick to the Script?
12. AgentTelemetry
13. Observability and Fault Injection for LLM-Based Multi-Agent Systems in Software Engineering
14. AgentTrace
15. FALAT
16. Causal Agent Replay

其中 VeriGrey、FLARE、LogicHunter 和 AgentLens 本轮已有方法阅读笔记，但因版本较新、正式出版状态未定，筛选状态仍保守地保留为 watchlist。其余摘要级记录的完整名单可用同一字段从 CSV 直接筛选，避免维护第二份易漂移的逐篇清单。

## 元数据冲突与访问限制

- Crossref/OpenAlex 的批量核验曾遇到 HTTP 429；发生限流时使用 ACL Anthology、arXiv、OpenReview、USENIX 或出版方原始页面复核，并在对应状态列记录来源。
- Crossref 返回题名模糊匹配而非精确匹配时，不采纳候选 DOI。
- 免费 PDF、开放数据和可执行代码分别记录，不把“可下载论文”推断为“开源实现”。
- 预印本和正式论文判为同一工作时合并为一条，以正式版本为首选，并在 `version_status` 中保留关系。
