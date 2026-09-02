# 智能体测试：无预设分类增量检索

检索日期：2026-08-19

## 目的

对现有“八类方法”进行反证。查询避免直接使用 fuzzing、metamorphic testing、fault injection、trajectory oracle、chaos testing 等既有分类词，转而从 validation、assurance、dependability、production failure 和 persistent state 进入。

## 数据源与查询

检索脚本合并 Semantic Scholar、OpenAlex、Crossref、arXiv 和 DBLP，并用 Unpaywall 查找开放版本。时间范围为 2023–2026，每组最多保留 80 条合并结果，不限定会议。

| 编号 | 精确查询 | 合并结果 | 来源异常 |
|---|---|---:|---|
| Q1 | `LLM agent validation assurance system behavior` | 80 | arXiv HTTP 429；其他来源成功 |
| Q2 | `agentic systems dependability verification specification` | 80 | 无 |
| Q3 | `LLM autonomous agent production failures empirical study` | 80 | 无 |
| Q4 | `LLM agent long term state memory isolation quality` | 80 | 无 |

原始请求 URL、时间戳、状态和合并记录保存在 `tmp/literature-search-20260819/`。结果中包含大量普通 agent-based modeling、非被测 Agent 应用和“用 Agent 测其他系统”的噪声，80 条不是纳入数量。

## 相对现有证据库的新候选

### A. Agent 框架与 harness 自身缺陷

1. **A Characterization Study of Bugs in LLM Agent Workflow Orchestration Frameworks**，ASE 2025，DOI `10.1109/ASE63991.2025.00278`。Crossref 与 OpenAlex 对 DOI、题名和年份一致；作者名存在一处结构化来源拼写差异，引用时应以 IEEE 正式记录为准。该工作可能补足“被测对象不仅是 Agent 行为，也包括编排框架”的盲区。
2. **Bugs in Modern LLM Agent Frameworks: An Empirical Study**，FSE 2026，DOI `10.1145/3803437.3805536`。Crossref 与 OpenAlex 对身份和核心元数据一致。摘要报告分析 CrewAI 等框架 issue；详细缺陷分类须阅读全文后使用。
3. **Understanding Agent-Reactive Bugs at the Model-Harness Boundary**，arXiv `2607.15684`。预印本候选，关注模型响应与 harness 代码共同触发的边界缺陷；只能作为前沿线索。

### B. 长期记忆不是“多做几次问答”，而是状态审计

1. **MEMPROBE: Probing Long-Term Agent Memory via Hidden User-State Recovery**，arXiv `2606.24595`。开放 PDF 候选；把 Agent 留下的记忆当作可审计产物，而不是仅从最终回答间接评价。
2. **A-TMA: Decoupling State-Aware Memory Failures in Long-Term Agent Memory**，arXiv `2607.01935`。开放 PDF 候选；提出旧事实、当前事实和状态转换事实混存的 `ghost memory` 问题。
3. **MEMTRACK: Evaluating Long-Term Memory and State Tracking in Multi-Platform Dynamic Agent Environments**，arXiv `2510.01353`。当前检索仅摘要；关注异步、多平台环境中的长期状态跟踪。
4. **Evaluating Very Long-Term Conversational Memory of LLM Agents**，ACL 2024 / arXiv `2402.17753`。已有正式身份线索，需判断其是否属于普通记忆能力评测，还是能支持测试方法主线。

### C. 从真实制品和差分执行研究失败

1. **Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents**，arXiv `2608.11888`。开放 PDF 候选；通过有技能/无技能或语义匹配技能的配对运行归因功能失败与成本回归。
2. **When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime**，arXiv `2606.14589`。单系统纵向生产案例，可能补充外部效度，但不能据单一系统概括全领域。

### D. 从业务要求与事务语义验证运行状态

1. **SagaLLM: Context Management, Validation, and Transaction Guarantees for Multi-Agent LLM Planning**，PVLDB 2025，DOI `10.14778/3750601.3750611`。Crossref 与 OpenAlex 完全核验。它主要是系统设计而非测试论文，但 rollback、事务保证和验证机制可能补足当前 Agent QA 图谱中的系统语义。
2. **Formal Verification of Agentic Systems over Operational Data**，arXiv `2608.03609`。开放 PDF 候选；从业务需求和持久化数据演化验证系统级行为，属于前沿形式化路线。
3. **CAVA: Canonical Action Verification and Attestation for Runtime Governance of Agentic AI Systems**，arXiv `2607.13716`。开放 PDF候选；关注跨 runtime 的动作身份、审批绑定和可复核凭证。

### E. 宽泛 QA 方法候选

**Methodology for Quality Assurance Testing of LLM-based Multi-Agent Systems**，AI-ML Systems 2024，DOI `10.1145/3703412.3703439`。Crossref 与 OpenAlex 完全核验。该论文题名直接相关，但 venue、引用信号和摘要贡献不足以自动成为锚点；应阅读全文判断是否只是指标框架或确有可复用测试方法。

## 对领域地图的影响

本轮结果没有推翻“测试活动/生命周期”主轴，反而暴露了旧八分类的三个缺口：

1. **测试对象缺口**：Agent harness、编排框架和模型—harness 边界应被显式纳入，而不是只测任务行为。
2. **状态语义缺口**：长期记忆需要测试写入、更新、过期、来源、隔离和跨会话传播，不能只看 recall 分数。
3. **测试定义缺口**：事务、权限、业务要求和动作身份需要在测试前形成可检查契约；这支持把“定义测试”放在生命周期首位。

## 使用限制

- 当前只完成发现、初筛和四篇正式论文的元数据核验。
- 除仓库既有全文外，本轮候选尚未完成全文阅读，不能据摘要写入详细方法、实验数字或作者局限。
- 2026 年预印本只用于检验领域边界和展示前沿，不能替代正式论文支撑成熟路线。
- Q1 的 arXiv 请求被限流，不能将该组的 arXiv 缺失解释为零结果。

## 下一步全文优先级

优先级 1：ASE 2025 编排框架缺陷、MEMPROBE、Agent Skills Can Be Harmful。

优先级 2：FSE 2026 Agent 框架缺陷、A-TMA、Formal Verification over Operational Data。

优先级 3：SagaLLM、CAVA、生产 silent failures、宽泛 MAS QA 方法。
