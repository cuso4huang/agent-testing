# 2026 软件工程顶会中的“直接测试智能体”论文：严格检索与证据复核

> 检索日期：2026-09-19（Asia/Shanghai）  
> 研究问题：在最新软件工程顶会中，哪些论文把 **AI agent / agentic system / multi-agent system / agent framework 本身作为被测对象（SUT）**？  
> 结论边界：本文严格排除“用智能体测试普通软件”（agent-as-tester）。详细技术结论只基于会议官方摘要或 arXiv 摘要，未声称完成全文精读。

## 1. 结论先行

截至 2026-09-19，直接测试智能体已经在软件工程顶会形成清晰集群：

1. **端到端、真实环境测试**：ICSE 2026 的 **SpecOps** 是最直接的代表，自动生成、部署、执行并验证 GUI agent 测试，在 5 个真实 agent 上报告发现 164 个真实缺陷。
2. **行为覆盖、轨迹诊断与故障归因**：ISSTA 2026 的 **AgentInspect**、FSE 2026 的 **FAMAS**、ASE 2026 的 **AgentChaos** 分别对应 agent-specific coverage、multi-agent failure attribution、LLM API fault injection。
3. **工具调用链安全测试/红队**：ISSTA 2026 出现密集专题，核心包括 **AgentBreaker、Datura、Red-Teaming Coding Agents**；ASE 2026 的 **COMA** 把 prompt compression 识别为新的 agent 攻击面。
4. **框架与测试 oracle**：ISSTA 2026 的 **LogicHunter** 直接测试 LangChain、LlamaIndex、CrewAI 等 agent framework，并用可检索文档/源码/运行状态的 agentic oracle 处理静默语义失败。
5. **测试实践与现实故障证据**：ASE 2026 的 **Tangent** 研究开源 agent 应用如何写测试；**What Breaks When LLMs Code?** 从真实事故构建 coding-agent operational-safety failure taxonomy。
6. **可观测性与受控故障**：ICST 2026 Tool Showcase 的 **llmmas-otel** 把 OpenTelemetry 级的跨 agent trace 与可定位 fault injection 结合，是搭建实验基础设施最实用的一项。

严格意义上，当前最值得优先阅读/复现的是：**SpecOps、AgentInspect、Datura、LogicHunter、AgentChaos、llmmas-otel**。它们覆盖了 test generation、coverage、oracle、fault injection、trace observability 和真实环境执行的主要技术缺口。

## 2. 范围、纳入标准与检索策略

### 2.1 会议范围

- 主线顶会/旗舰会议：ICSE 2026、FSE 2026、ASE 2026、ISSTA 2026。
- 测试专业旗舰会议补充：ICST 2026。
- 只把 Research Track/Research Papers 当作“正式主线论文”；Ideas, Visions and Reflections（IVR）、Tool/Testing Tools and Data Showcase 单列，不与主会 Research Paper 混排。

时间状态必须注意：

- ICSE 2026（4 月）、ICST 2026（5 月）、FSE 2026（7 月）已举行。
- ISSTA 2026（10 月 4–9 日）和 ASE 2026（10 月 12–16 日）在检索日尚未举行；本文所称“录用”来自官方 accepted/program 页面。ISSTA 页面明确标注 program tentative，因此其会议信息应在会后再复核。

### 2.2 严格纳入标准

论文至少满足以下一项，且被测对象必须是 agent：

- 生成并执行针对 agent 的测试输入、场景或攻击；
- 对 agent 运行时注入故障或环境异常；
- 构造 agent-specific coverage、oracle、failure detection/attribution；
- 对 agent 的轨迹、协作、工具调用、安全性或真实故障进行系统评估；
- 构建明确以 agent 为被测对象的 benchmark。

排除：agent 只负责生成普通程序测试、GUI 测试、API 测试、fuzzing、修复或验证，而 agent 自身并非 SUT。

### 2.3 数据源与精确检索式

优先级：会议官方 Researchr 页面（venue/track/作者/摘要） > ACM/IEEE DOI/Crossref/OpenAlex（正式元数据） > arXiv（开放全文与版本关系） > Semantic Scholar（引用数快照）。

执行的查询族：

```text
(agent OR agentic OR "multi-agent" OR "LLM agent")
AND (test OR testing OR evaluation OR benchmark OR failure
     OR "fault injection" OR "red team" OR robustness OR safety)
AND venue:{ICSE,FSE,ASE,ISSTA,ICST}
AND year:2026
```

并对每个会议 accepted/program 页面进行标题扫描，关键词包括：

```text
agent, agentic, multi-agent, tool invocation, prompt injection,
fault, failure, chaos, runtime verification, benchmark,
trajectory, testing practice, operational safety
```

结构化核验：

- 用 `literature-research/scripts/verify_metadata.py` 对标题执行 Crossref + OpenAlex 核验；
- 对已知 arXiv ID 使用 Semantic Scholar batch API 获取 venue/DOI/citationCount；
- 去重顺序：DOI → arXiv ID → 规范化标题+年份+作者；保留 preprint/正式版本关系。

## 3. 严格核心集：被测对象就是 agent

证据等级：

- **A1**：会议官方页面 + OA preprint/正式 DOI；摘要已检查；元数据可交叉核实。
- **A2**：会议官方页面确认 Research Track/Research Papers，摘要已检查，但正式 DOI/OA preprint 未可靠解析。
- **B**：官方 Tool/IVR/非主 Research Track；方法相关但不可与 Research Paper 等量齐观。

引用数为 Semantic Scholar 在 2026-09-19 的快照；新论文低引用或 0 引用不代表质量低。`—` 表示 exact paper record 未稳定解析，而不是 0。

| 优先级 | 论文 | Venue / 轨道与状态 | 直接测试什么、怎么测（摘要证据） | DOI / OA | S2 引用 | 证据 |
|---|---|---|---|---|---:|---|
| ★ | **SpecOps: A Fully Automated AI Agent Testing Framework in Real-World GUI Environments** — Ahmed et al. | ICSE 2026 Research Track，已举行 | 在真实 GUI/CLI/web/extension 环境中自动完成 test generation、environment setup、execution、validation；被测对象是 5 个真实 agent | [DOI 10.1145/3744916.3787778](https://doi.org/10.1145/3744916.3787778)；[arXiv:2603.10268](https://arxiv.org/abs/2603.10268)；[官方页](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/250/SpecOps-A-Fully-Automated-AI-Agent-Testing-Framework-in-Real-World-GUI-Environments) | 4 | A1 |
|  | **Failure-Based Testing for Deep Reinforcement Learning Agents** — Lin, Meng, Zheng | FSE 2026 Research Papers，已举行 | Prior Random Testing 用 task-induced failure insight 优先测试 DRL agent 的高失败风险区域 | [DOI 10.1145/3808185](https://doi.org/10.1145/3808185)；[arXiv:2606.31372](https://arxiv.org/abs/2606.31372)；[官方页](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/152/Failure-Based-Testing-for-Deep-Reinforcement-Learning-Agents) | 0 | A1 |
| ★ | **Spectrum-based Failure Attribution for Multi-Agent Systems**（preprint 题名 *Who is Introducing the Failure?*）— Ge et al. | FSE 2026 Research Papers，已举行 | FAMAS 重放并抽象 MAS 轨迹，以 spectrum analysis 定位导致失败的 agent action | [arXiv:2509.13782](https://arxiv.org/abs/2509.13782)；[官方页](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/205/Spectrum-based-Failure-Attribution-for-Multi-Agent-Systems) | 34 | A1；正式题名/预印本题名有版本差异 |
| ★ | **AgentBreaker: Evaluating Context-Aware Indirect Prompt Injection Risks in Modern Web Agents** — Son et al. | ISSTA 2026 Research Papers，未来会议；program tentative | 为页面上下文生成 DOM 内间接提示注入，测试 5 个 web agents 的攻击易感性，并评估防御 | [官方页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/74/AgentBreaker-Evaluating-Context-Aware-Indirect-Prompt-Injection-Risks-in-Modern-Web-) | — | A2 |
| ★ | **AgentInspect: Diagnosing Behavioral Failures in Artificial Intelligence Agents** — Manke et al. | ISSTA 2026 Research Papers，未来会议；program tentative | agent-specific coverage 引导输入生成；捕获/模拟异常工具行为；用确定性规则检测 6 类行为故障 | [官方页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/83/AgentInspect-Diagnosing-Behavioral-Failures-in-Artificial-Intelligence-Agents) | — | A2 |
| ★ | **Datura: Progressive Red Teaming Testing for Tool Invocation Chain in LLM Agents** — Shao et al. | ISSTA 2026 Research Papers，未来会议；program tentative | 生成“单步看似合法、组合后有害”的 chained tool manipulation 测试，面向工具链的 progressive red teaming | [官方页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/10/Datura-Progressive-Red-Teaming-Testing-for-Tool-Invocation-Chain-in-LLM-Agents)；[代码](https://github.com/ycshao12/Datura_RedTeaming_Testing) | — | A2 |
| ★ | **Red-Teaming Coding Agents from a Tool-Invocation Perspective: An Empirical Security Assessment** — Xie et al. | ISSTA 2026 Research Papers，未来会议；program tentative | 测试 Cursor、Claude Code、Copilot、Windsurf、Cline、Trae 的 tool invocation；包括 prompt leakage 与 tool-description/tool-return 双通道劫持 | [arXiv:2509.05755](https://arxiv.org/abs/2509.05755)；[官方页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/176/Red-Teaming-Coding-Agents-from-a-Tool-Invocation-Perspective-An-Empirical-Security-A) | 6 | A1 |
| ★ | **LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle** — Long, Zhao, Wang | ISSTA 2026 Research Papers，未来会议；program tentative | specification-aware fuzzing 测试 LangChain/LlamaIndex/CrewAI；oracle 主动查文档、源码和运行状态以识别异常与静默语义错误 | [arXiv:2607.06195](https://arxiv.org/abs/2607.06195)；[官方 track](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | 1 | A1 |
|  | **Environmental Injection Attacks against GUI Agents in Realistic Dynamic Environments** — Zhang et al. | ISSTA 2026 Research Papers，未来会议；program tentative | Chameleon 在动态 web 环境中生成环境注入触发器，测试 4 个 LVLM GUI agents 的劫持风险 | [官方页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/57/Environmental-Injection-Attacks-against-GUI-Agents-in-Realistic-Dynamic-Environments) | — | A2 |
|  | **Learning from the Test: Self-Referential Differential Testing for Deep RL Agents** — He et al. | ISSTA 2026 Research Papers，未来会议；program tentative | Delta 先做 safety testing，再用测试数据训练 challenger agent，与 AUT 差分比较以发现 optimality bugs | [arXiv:2608.22284](https://arxiv.org/abs/2608.22284)；[官方 track](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | 0 | A1 |
| ★ | **AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection** — Tan et al. | ASE 2026 Research Papers，已录用、会议未举行 | 在统一 LLM HTTP API 层注入 crash/omission/value faults，不改 agent 源码，比较系统和架构在 65 种 fault configuration 下的退化 | [DOI 10.1145/3832783.3837437](https://doi.org/10.1145/3832783.3837437)；[arXiv:2608.06790](https://arxiv.org/abs/2608.06790)；[官方页](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/141/AgentChaos-Chaos-Engineering-for-Agent-Systems-via-Programmatic-Fault-Injection) | 0 | A1 |
| ★ | **Tangent: An Empirical Study of Testing Practices for LLM-Based Agent Applications** — Pan et al. | ASE 2026 Research Papers，已录用、会议未举行 | 挖掘 240 个模块、人工标注 2,572 个测试方法，并访谈 10 位资深从业者，形成 23 种 agent 测试模式 taxonomy；这是“测试实践研究”，不是新测试器 | [DOI 10.1145/3832783.3837414](https://doi.org/10.1145/3832783.3837414)；[arXiv:2608.08413](https://arxiv.org/abs/2608.08413)；[官方 track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | 1 | A1 |
| ★ | **What Breaks When LLMs Code? Characterizing Operational Safety Failures of Agentic Code Assistants** — Hasan, Biswas | ASE 2026 Research Papers，已录用、会议未举行 | 从 16,586 个 GitHub issues 中确认 547 个真实 agent safety failures，构建 33 类 operational risk taxonomy；属于事故驱动的测试需求/故障模型证据 | [DOI 10.1145/3832783.3834393](https://doi.org/10.1145/3832783.3834393)；[arXiv:2605.30777](https://arxiv.org/abs/2605.30777)；[官方 track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | 2 | A1 |
| ★ | **When Compression Becomes an Attack Surface: Black-Box Attacks on Prompt-Compressed LLM Agents** — Liu et al. | ASE 2026 Research Papers，已录用、会议未举行 | COMA 用 surrogate compressor/LLM 搜索 pre-compression perturbation，测试压缩导致的 adversarial information loss；直接作用于 agent pipeline | [官方页](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/64/When-Compression-Becomes-an-Attack-Surface-Black-Box-Attacks-on-Prompt-Compressed-LL) | — | A2 |
| ★ | **Observability and Fault Injection for LLM-Based Multi-Agent Systems in Software Engineering** — Seyedghorban et al. | ICST 2026 Testing Tools and Data Showcase，已举行；**非 Research Paper** | llmmas-otel 记录 workflow/agent/message/tool/LLM 调用级对齐 trace，并在指定交互点注入 fault，比较 baseline 与 faulty run | [DOI 10.1109/ICST69053.2026.00037](https://doi.org/10.1109/ICST69053.2026.00037)；[arXiv:2608.24271](https://arxiv.org/abs/2608.24271)；[官方页](https://conf.researchr.org/details/icst-2026/icst-2026-testing-tools-and-data-showcase/5/Observability-and-Fault-Injection-for-LLM-Based-Multi-Agent-Systems-in-Software-Engin) | 0 | B |
|  | **Metamorphic Testing of Vision-Language Action–Enabled Robots** — Valle et al. | ICST 2026 Research Papers，已举行 | 用 2 类 pattern、5 个 metamorphic relations 缓解 VLA robot agent 的 test-oracle problem；覆盖 5 个 VLA models、2 个机器人、4 个任务 | [DOI 10.1109/ICST69053.2026.00020](https://doi.org/10.1109/ICST69053.2026.00020)；[arXiv:2602.22579](https://arxiv.org/abs/2602.22579)；[官方页](https://conf.researchr.org/details/icst-2026/icst-2026-research/33/Metamorphic-Testing-of-Vision-Language-Action-Enabled-Robots) | 5 | A1 |

## 4. 相关但不作为“核心测试方法”混排的论文

这些论文仍是“直接评估/保障 agent”，但更接近 benchmark、runtime assurance 或经验分析：

| 论文 | Venue | 为什么只列为相邻证据 |
|---|---|---|
| [FreshBrew: A Benchmark for Evaluating AI Agents on Java Code Migration](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/172/FreshBrew-A-Benchmark-for-Evaluating-AI-Agents-on-Java-Code-Migration) | ICSE 2026 Research | 是直接 agent benchmark，但任务域单一，重点是 Java migration 能力与 reward hacking，不是通用测试技术 |
| [Beyond Final Code: A Process-Oriented Error Analysis of Software Development Agents](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/98/Beyond-Final-Code-A-Process-Oriented-Error-Analysis-of-Software-Development-Agents-i) | ICSE 2026 Research | 轨迹/测试日志的实证诊断；[arXiv:2503.12374](https://arxiv.org/abs/2503.12374)，DOI `10.1145/3744916.3773140`，S2 引用 13 |
| [CAM: A Causality-based Analysis Framework for Multi-Agent Code Generation Systems](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/147/CAM-A-Causality-based-Analysis-Framework-for-Multi-Agent-Code-Generation-Systems) | ISSTA 2026 Research | 通过中间特征故障模拟分析 MACGS，但主目标是因果重要性/优化，而非一般测试框架 |
| [ProbGuard: Proactive Runtime Monitoring for LLM Agent Safety](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/117/ProbGuard-Proactive-Runtime-Monitoring-for-LLM-Agent-Safety-via-Probabilistic-Predic) | ASE 2026 Research | runtime monitoring / intervention，属于运行时保障；[arXiv:2508.00500](https://arxiv.org/abs/2508.00500)，S2 引用 23 |
| [RefineAct: Automatic Runtime Verification of LLM Agent Actions](https://conf.researchr.org/track/ase-2026/ase-2026-not-in-person-presentations) | ASE 2026 Research | 从自然语言任务生成 Prolog 规格并在线拦截 action，是 verification/enforcement 而非离线 testing；DOI `10.1145/3832783.3834409` |
| [From Plan to Action: How Well Do Agents Follow the Plan?](https://arxiv.org/abs/2604.12147) | ASE 2026 Research | 16,991 条 SWE-agent trajectory 的 plan-compliance 评估；更像过程评测/行为研究 |
| [RACE-Bench: A Reasoning-Augmented Benchmark for Repository-Level Code Agents on Feature Addition](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/130/RACE-Bench-A-Reasoning-Augmented-Benchmark-for-Repository-Level-Code-Agents-on-Featu) | ASE 2026 Research | 明确直接评估 coding agent，但属于任务 benchmark，不是测试方法 |
| [Evaluating Privilege Usage of Agents on Real-World Tools / GrantBox](https://conf.researchr.org/details/fse-2026/fse-2026-ideas-visions-and-reflections/3/Evaluating-Privilege-Usage-of-Agents-on-Real-World-Tools) | FSE 2026 IVR | 方向很相关，但轨道是 Ideas, Visions and Reflections，不应误写成 FSE Research Paper |

## 5. 明确排除：它们是“用 agent 做测试”，不是“测试 agent”

以下题名容易误收，但其 SUT 是普通软件、GUI、API、合约、程序或测试套件：

| 排除论文/系统 | Venue | 排除理由 |
|---|---|---|
| Breaking Single-Tester Limits / MAdroid | ICSE 2026 | 多 agent 扮演 tester 测多用户 app 功能；agent 是测试工具 |
| WebTestPilot | FSE 2026 | agent 自主执行 Web E2E 测试；SUT 是 Web 应用 |
| IntentTester | FSE 2026 | multi-agent 做跨库 test migration；SUT 是软件库 |
| PersonaTester | FSE 2026 | agent 模拟众包测试人员；SUT 是被测 app |
| MuMuTestUp | ISSTA 2026 | 多 agent 更新普通单元测试；SUT 不是 agent |
| Test vs Mutant / AdverTest | ISSTA 2026 | tester/mutant agents 协同生成普通程序单元测试；被评估目标主要是 test suite |
| PAGENT | ISSTA 2026 | agent 生成 PoC；目标是漏洞/程序，不是 agent 自身 |
| WebCQ | ASE 2026 | multi-agent RL 用于 Web GUI testing；SUT 是网页应用 |
| Fuzz4DB、SynerFuzz、PoCo、IntOAgent | ASE 2026 | agent 驱动数据库/合约/程序漏洞发现或 fuzzing；agent 是测试执行者 |
| ICST 2026 ASTA workshop 大多数论文 | ICST workshop | workshop 明确聚焦 agent-as-tester；不能当作“直接测试 agent”的主证据 |

## 6. 主题综合与研究空白

### 6.1 共同趋势

- **从 final answer 转向 process/trajectory**：AgentInspect、FAMAS、Tangent、Beyond Final Code 都说明仅看最终成功率不足，必须记录 action、tool call、agent-to-agent message 与中间状态。
- **从自然输入转向受控扰动**：Datura/AgentBreaker/COMA 注入安全扰动，AgentChaos/llmmas-otel 注入运行时故障，形成“攻击输入 + 系统故障”双轴测试空间。
- **oracle 正在成为核心瓶颈**：LogicHunter 显式解决 agent framework 的静默失败；SpecOps 用环境和执行结果做自动 validation；Delta 用 challenger agent 构造相对 oracle。
- **testability 仍弱**：Tangent 报告的现实测试以窄范围 unit test、重 mocking、浅 assertion 为主，跨 agent 协作、长期状态和非功能属性覆盖不足。

### 6.2 尚未解决的问题

1. **统一覆盖标准缺失**：AgentInspect 有 agent-specific coverage，但还没有跨 framework、跨工具协议可比的 coverage model。
2. **长时序状态测试不足**：当前多数实验仍以单任务/有限轨迹为单位，长期 memory、跨 session、权限积累和环境漂移缺乏系统化 SE 测试。
3. **oracle 的独立性风险**：用 agent/LLM 做 oracle 时，可能与 AUT 共享模型偏差；需要 executable state、formal predicate、human audit 的多重证据。
4. **fault model 尚未统一**：AgentChaos 聚焦 LLM API response faults，llmmas-otel 聚焦交互点 fault injection，安全论文聚焦恶意 tool/context；缺少统一 taxonomy 与组合故障协议。
5. **benchmark-to-production gap**：SpecOps 和 What Breaks 更接近真实部署，但大多数论文仍需在真实权限、长期运行、版本漂移与异构工具环境中复验。
6. **可复现性状态不一**：ISSTA/ASE 未来会议中部分论文尚无稳定 DOI/OA 链接；应在会后用 ACM DL、Crossref、OpenAlex 再核验一次。

## 7. 推荐阅读与复现顺序

若目标是做“智能体测试方法”研究：

1. **Tangent**：先建立现实测试实践与缺口地图。
2. **AgentInspect**：学习 agent-specific coverage、工具异常模拟、deterministic failure detection。
3. **AgentChaos + llmmas-otel**：搭建可观测、可重放、可故障注入的实验底座。
4. **LogicHunter**：研究 specification-aware generation 与 agentic oracle。
5. **Datura / AgentBreaker / COMA**：扩展到 tool chain、web context、prompt compression 的安全测试。
6. **SpecOps**：最后落到真实环境端到端自动化与 bug confirmation。

## 8. 限制与后续复核点

- 本轮以官方摘要、正式元数据和 arXiv 摘要为主，**没有把摘要数字扩展解释成全文结论**。
- Citation count 是动态值，来源为 Semantic Scholar，抓取日期为 2026-09-19。
- Crossref/OpenAlex 对尚未举行的会议存在收录延迟；未解析到 DOI 的论文标为“未可靠解析”，不能推断为“没有 DOI”。
- ISSTA 2026 官方页面写明 program tentative；ASE 2026 也尚未举行。建议在 2026-10-17 之后复核最终 proceedings、DOI、artifact badges 和作者列表。
- 未使用 Google Scholar：当前环境未连接 Chrome remote debugging；引用数使用 Semantic Scholar 快照即可满足新论文的轻量比较。

