# 2026 年智能体测试顶会专项复查

检索日期：2026-09-02

## 1. 本轮方法

本轮不再以 Semantic Scholar/OpenAlex 的关键词结果作为主入口，而是逐项扫描各会议官方 accepted-papers、program 或 proceedings，再以论文全文、Crossref/OpenAlex/arXiv 和论文官方仓库核验。

纳入范围分两层：

- **严格相关**：测试/评测/诊断/红队的对象是 LLM、AI agent、agent framework、工具链或轨迹；或者方法本身是执行软件/安全测试的自主、多智能体系统。
- **宽口径相关**：LLM 驱动的测试生成、oracle、验证、failure diagnosis，但未必构成 autonomous agent。

代码状态分为 `verified_code`、`artifact_pending`、`code_not_found`、`unverified_candidate`。没有代码的相关论文仍保留在总表，但不进入“可复现核心集”。

## 2. 会议状态

| 领域 | 会议 | 2026-09-02 状态 |
|---|---|---|
| 软件工程 | ICSE、FSE、ASE、ISSTA、ICST | 官方 program/accepted papers 已公布并逐项扫描 |
| AI | ICLR、AAAI、ACL/EACL、IJCAI-ECAI | 正式 proceedings 或官方 accepted list 已公布 |
| AI | EMNLP | 官方 accepted main list 已公布；正式 Anthology/DOI 尚未发布 |
| AI | NeurIPS | 官方论文通知日期为 2026-09-24；当前不能声称任何主会录用 |
| AI | ICML | 已召开；官方主会 Poster 索引已公布并逐项扫描 |
| 安全 | IEEE S&P、USENIX Security、NDSS | 官方 program/proceedings 已公布并逐项扫描 |
| 安全 | ACM CCS | accepted papers 已公布；会议尚未召开，部分 DOI/PDF/Artifact 尚未齐全 |

## 3. 软件工程顶会：严格相关

### ICSE 2026 Research Track

官方入口：[ICSE 2026 Research Track](https://conf.researchr.org/track/icse-2026/icse-2026-research-track)

| 论文 | 核心内容 | 代码状态 |
|---|---|---|
| Breaking Single-Tester Limits: Multi-Agent LLMs for Multi-User Feature Testing | 多个 tester agents 扮演不同用户，协作测试 multi-user feature | `code_not_found` |
| An LLM Agentic Approach for Legal-Critical Software: A Case Study for Tax Prep Software | 多 agent 开发法律关键软件；metamorphic-testing agent 生成反例 | `code_not_found` |
| [E-Test: E’er-Improving Test Suites](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/84/E-Test-E-er-Improving-Test-Suites) | 识别现有测试未覆盖的自然语言场景并迭代补充测试；arXiv `2510.19860` | `code_not_found` |
| [Testora](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/10/Testora-Using-Natural-Language-Intent-to-Detect-Behavioral-Regressions) | 生成测试、差分执行，用 PR 意图作为 behavioral regression oracle | `code_not_found` |
| [TestWeaver](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/277/TestWeaver-Execution-aware-Feedback-driven-Regression-Testing-Generation-with-Large) | execution-aware、feedback-driven 回归测试生成 | `code_not_found` |
| [SAFE](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/190/SAFE-Harnessing-LLM-for-Scenario-Driven-ADS-Testing-from-Multimodal-Crash-Data) | 从事故材料生成可重放 ADS 测试场景并 self-validate | `code_not_found` |

宽口径相关还包括 RBCTest、Knowledge Matters、Issue2Test、AutoOracle、MioHint、LLM Test Generation via Iterative Hybrid Program Analysis、Delta Debugging for LLM-integrated Systems、Google integration-test failure diagnosis 等。

### FSE 2026 Research Papers

官方入口：[FSE 2026 Research Papers](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers)

| 论文 | 核心内容 | 代码状态 |
|---|---|---|
| [WebTestPilot](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/207/WebTestPilot-Agentic-End-to-End-Web-Testing-against-Natural-Language-Specification-b) | 根据自然语言规格自主执行 Web E2E 测试，并从符号化 GUI 推断 oracle；DOI `10.1145/3797115`，arXiv `2602.11724` | **`verified_code`**：[code-philia/WebTestPilot](https://github.com/code-philia/WebTestPilot) |
| [Failure-Based Testing for Deep Reinforcement Learning Agents](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/152/Failure-Based-Testing-for-Deep-Reinforcement-Learning-Agents) | 用任务诱导的失败信息指导 Prior Random Testing | `code_not_found` |
| [IntentTester](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/163/IntentTester-Intent-Driven-Multi-Agent-Framework-for-Cross-Library-Test-Migration) | 多 agent 完成测试意图提取、跨库迁移、执行和修复 | `code_not_found` |
| Towards Automated Crowdsourced Testing via Personified-LLM | 用人格化 LLM 模拟不同众包测试人员 | `code_not_found` |
| [Agentic Verification of Software Systems](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/110/Agentic-Verification-of-Software-Systems) | LLM proof agent 迭代验证程序 | `code_not_found` |
| [Event-B Agent](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/211/Event-B-Agent-Towards-LLM-Agent-for-Formal-Model-Synthesis-and-Repair) | 用模型检查/证明反馈迭代修复 Event-B 模型 | `code_not_found` |
| Evaluating Privilege Usage of Agents on Real-World Tools | 测量 agents 调用真实工具时的不必要权限 | `code_not_found` |
| [AgentBound](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/14/AgentBound-Securing-Execution-Boundaries-of-AI-Agents) | MCP server 声明式访问控制与执行边界 | `code_not_found` |

`TestAgent` 是 FSE Tool Demonstration；`AstraGame` 是 Industry Paper；`Elevate` 是 Journal First，均不能写成 Research Paper。

### ISSTA 2026 Research Papers

官方入口：[ISSTA 2026 Research Papers](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers)

| 论文 | 核心内容 | 代码状态 |
|---|---|---|
| [AgentInspect](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/83/AgentInspect-Diagnosing-Behavioral-Failures-in-Artificial-Intelligence-Agents) | agent-specific coverage、异常工具模拟、确定性行为失败 oracle | `code_not_found`；同名 TS 项目与论文无关 |
| [Datura](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/10/Datura-Progressive-Red-Teaming-Testing-for-Tool-Invocation-Chain-in-LLM-Agents) | 渐进式红队测试 LLM agent 工具调用链 | **`verified_code`**：[Datura_RedTeaming_Testing](https://github.com/ycshao12/Datura_RedTeaming_Testing) |
| LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle | 规格驱动 fuzzing + 可主动查询文档/源码/状态的 ReAct oracle；arXiv `2607.06195` | `code_not_found` |
| [Test vs Mutant](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/31/Test-vs-Mutant-Adversarial-LLM-Agents-for-Robust-Unit-Test-Generation) | tester 与 mutant agents 对抗演化 | `code_not_found` |
| [MuMuTestUp](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/126/MuMuTestUp-Mutation-based-Multi-Agent-Test-Case-Update) | mutation-guided multi-agent test update | `code_not_found` |
| Learning from the Test: Self-Referential Differential Testing for Deep RL Agents | 利用多次执行间的自参照关系构造 DRL agent differential oracle | `code_not_found` |

宽口径相关还包括 CAST、Testing RAG Systems with Chunk Coverage、LLMutantKiller、PAGENT、Red-Teaming Coding Agents from a Tool-Invocation Perspective、Sifting the Noise 等。

### ASE 2026 Research Papers

官方入口：[ASE 2026 Research Track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track)

强相关论文：

- Understanding Bugs in Modern Agentic Frameworks: A Study of Symptoms, Root Causes, and Triggering Conditions
- Breaking Customized LLMs for Coding: Automated Red Teaming for Instruction Backdoor Attacks
- Breaking the Isolation: Coordinated Multi-agent Fuzzing for Smart Contracts with Multi-dimensional Objective Learning
- Automated Lemma Discovery in Agentic Program Verification
- IntOAgent: Automated Detection and Triggering of Integer Overflow Vulnerabilities
- Piece by Piece: Automating Combination Interaction GUI Testing via Planning and Dual Memory
- When Knowledge Changes: Metamorphic Testing of RAG Systems with Mutations
- When Compression Becomes an Attack Surface: Black-Box Attacks on Prompt-Compressed LLM Agents
- To Think or Not to Think: Evaluating LLM Reasoning and Agents in Vulnerability Detection

这些均已由 ASE 官方列表确认录用，但本轮没有核实到与论文准确对应的公开代码，统一暂标 `code_not_found`，不能据此断言作者最终不会发布 Artifact。

### ICST 2026 Main Track

官方入口：[ICST 2026 Main Track](https://conf.researchr.org/track/icst-2026/icst-2026-papers)

最直接的是 **Metamorphic Testing of Vision-Language Action–Enabled Robots**，测试 VLA robotic agents 并以 metamorphic relations 缓解 oracle 问题。其他宽相关包括 LLM-based flakiness diagnosis、无 ground truth 的 test-generation verification、Android bug reproduction、LLM-generated counterexamples 和 protocol specification synthesis。本轮均未核实代码。

ICST 另有 ASTA workshop，但 workshop 论文与主会严格分开。

## 4. AI/NLP 顶会

### ICLR 2026：正式 Conference Papers

官方 proceedings 已逐项扫描。2026 年已经形成密集的 agent testing/evaluation 集群：

| 类别 | 论文 |
|---|---|
| 故障归因/调试 | [AgenTracer](https://proceedings.iclr.cc/paper_files/paper/2026/hash/134ed7a477770f227f12450ef0cbb8f4-Abstract-Conference.html)、[DoVer](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2f5fdce256ff0d7fb774da76e5e63209-Abstract-Conference.html)、[Aegis](https://proceedings.iclr.cc/paper_files/paper/2026/hash/56e8943ecd44b67bbea2702b9117b858-Abstract-Conference.html)、[Talk, Evaluate, Diagnose](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4cb31c278aae8c8862af1672557d3b11-Abstract-Conference.html) |
| 软件/终端/科研 agents | [DevOps-Gym](https://proceedings.iclr.cc/paper_files/paper/2026/hash/15e35461247bbd05fa890d384060c847-Abstract-Conference.html)、[Terminal-Bench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/444a3737adaee10d86ad2ef5f74468e6-Abstract-Conference.html)、[EXP-Bench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c411f5b2d9c55f1685e72db224ad8b0e-Abstract-Conference.html)、Process-Level Trajectory Evaluation for SE Agents |
| MCP/tool use | [MCPMark](https://proceedings.iclr.cc/paper_files/paper/2026/hash/8138d211ce8790fdfbeeeb9781838a37-Abstract-Conference.html)、[MCP-Bench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/9e4b14eb6f16fe7b5818a8d633a0606a-Abstract-Conference.html)、[MCP-SafetyBench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d46f127a80dc58cbc0732a717285c43a-Abstract-Conference.html) |
| computer-use/web agent 红队 | [VPI-Bench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/28e4c3696637ac727051a2922643ec6a-Abstract-Conference.html)、[RedTeamCUA](https://proceedings.iclr.cc/paper_files/paper/2026/hash/505ca7558b83126389727d08f2366b72-Abstract-Conference.html)、[ST-WebAgentBench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c6c29e590e3c62e37e6b39cdd6baf2e8-Abstract-Conference.html)、[OpenApps](https://proceedings.iclr.cc/paper_files/paper/2026/hash/bffc719468c22f9ba53e73696dd71858-Abstract-Conference.html) |
| 安全与治理 | [OpenAgentSafety](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a0f6c06b8d6114bb37688c2dc19b4d74-Abstract-Conference.html)、[A2ASecBench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c6a4c60e4c12b4157d33f34b29d22067-Abstract-Conference.html)、[RedCodeAgent](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d51ce6040fe3dafd260411593f05a1fa-Abstract-Conference.html)、[Just Do It!?](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ea7623ff02edffe68866f88da2667592-Abstract-Conference.html) |
| 通用能力/长期行为 | [Gaia2](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c26a67e0470774df98c12480ec5d2d7b-Abstract-Conference.html)、[ManagerBench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/b8330f5b70b3c53172417deac6f057b1-Abstract-Conference.html)、[agent memory evaluation](https://proceedings.iclr.cc/paper_files/paper/2026/hash/fd1eff9dd295df50a41f2521942fa31d-Abstract-Conference.html)、Your Agent May Misevolve、GhostEI-Bench、CyberGym |

已核实代码的代表性 ICLR 2026 核心方法：

- [RedTeamCUA](https://github.com/OSU-NLP-Group/RedTeamCUA)（ICLR 2026 Oral）：混合 Web–OS 沙箱、RTC-Bench、自动对抗注入。
- [Terminal-Bench](https://github.com/jvpoulos/terminal-bench)：真实终端环境、程序化测试脚本和 oracle solution。
- [MCPMark](https://github.com/eval-sys/mcpmark)：真实 MCP 工具环境压力测试。
- [MCP-SafetyBench](https://github.com/xjzzzzzzzz/MCPSafety)：MCP agent safety benchmark。

其余 ICLR 项目统一暂标 `code_pending_verification`，不是“无代码”。

### ACL / Findings / EACL 2026

正式 ACL Anthology 强相关论文包括：

- [AgencyBench](https://aclanthology.org/2026.acl-long.337/) — ACL Long
- [SafeAgent](https://aclanthology.org/2026.acl-long.1501/) — ACL Long
- [Plan-RewardBench](https://aclanthology.org/2026.acl-long.1062/) — ACL Long
- [AgenticEval](https://aclanthology.org/2026.findings-acl.727/) — Findings
- [PerMemSafe](https://aclanthology.org/2026.findings-acl.320/) — Findings
- [TraineeBench](https://aclanthology.org/2026.findings-acl.1505/) — Findings
- [SecureWebArena](https://aclanthology.org/2026.findings-acl.582/) — Findings
- [ToolSafe / TS-Bench](https://aclanthology.org/2026.findings-acl.1850/) — Findings
- [ABC-Bench](https://aclanthology.org/2026.findings-acl.1142/) — Findings
- [A Survey on Evaluation of LLM-based Agents](https://aclanthology.org/2026.findings-acl.1330/) — Findings，综述入口而非具体方法终点
- [Agent-Testing Agent](https://aclanthology.org/2026.eacl-long.339/) — EACL Long，自动分析 agent、生成 persona 驱动对抗测试并自适应提高难度

### AAAI / IJCAI-ECAI / EMNLP 2026

- AAAI 正式论文：[MCP-AgentBench](https://ojs.aaai.org/index.php/AAAI/article/view/40347)、[ShoppingBench](https://ojs.aaai.org/index.php/AAAI/article/view/40640)、AMS-IO-Bench/Agent。
- IJCAI-ECAI 官方 accepted list：[ResearchEnvBench](https://2026.ijcai.org/accepted-papers/)、role-playing agent safety、multi-agent RL probabilistic verification、human–agent collaboration testbed。Survey Track 只作追踪入口。
- [EMNLP 2026 accepted main list](https://2026.emnlp.org/program/main_papers/) 包含 Preemptive Detection and Correction of Misaligned Actions、IPIGuard、WebInject、Policy-Adherent Agent Red-Teaming、ToolSafety、Beyond Static Testbeds、Breaking Agents 等；正式卷/DOI 尚未发布，不能把同名 arXiv 自动写成正式版本。
- NeurIPS 2026 尚未通知，当前留空。
### ICML 2026 Main Conference Posters

官方入口：[ICML 2026 Papers](https://icml.cc/virtual/2026/papers.html)。以下均由 `/virtual/2026/poster/` 官方页面确认是主会 Poster，而非 workshop：

| 论文 | 测试/评测重点 | 代码状态 |
|---|---|---|
| [AgentSuite](https://icml.cc/virtual/2026/poster/66603) | component-based pipeline 审计 agent benchmark 的隐藏缺陷 | `code_pending_verification` |
| [Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks](https://icml.cc/virtual/2026/poster/64842) | 跨 session、状态化 agent memory 测试 | `code_pending_verification` |
| [FormulaCode](https://icml.cc/virtual/2026/poster/63544) | 大型代码库上的 agentic optimization evaluation | 项目页已公开，仓库待核 |
| [GameDevBench](https://icml.cc/virtual/2026/poster/64919) | 用游戏开发测试多模态软件开发 agents | **`verified_code`**：[waynchi/gamedevbench](https://github.com/waynchi/gamedevbench) |
| [Implicit Intelligence](https://icml.cc/virtual/2026/poster/64912) | 测试 agent 对用户未明说约束的处理 | `code_pending_verification` |
| [SafeHarbor](https://icml.cc/virtual/2026/poster/64556) | 为 agent safety 构造精确的层级记忆决策边界 | **`verified_code`**：[ljj-cyber/SafeHarbor](https://github.com/ljj-cyber/SafeHarbor) |
| [SafeLab](https://icml.cc/virtual/2026/poster/61584) | 科研机器人 embodied agents 的轨迹级持续安全 | `code_pending_verification` |
| [AgentWebBench](https://icml.cc/virtual/2026/poster/63068) | agentic Web 中的 multi-agent coordination benchmark | 项目页已公开，仓库待核 |

## 5. 安全顶会

### USENIX Security 2026

官方入口：[USENIX Security 2026](https://www.usenix.org/conference/usenixsecurity26/technical-sessions)

| 论文 | 核心内容 | 代码状态 |
|---|---|---|
| [MUZZLE](https://www.usenix.org/conference/usenixsecurity26/presentation/syros) | 基于 agent 轨迹反馈，自适应红队测试 Web agents 的 indirect prompt injection | **`verified_code`**：[gsiros/muzzle](https://github.com/gsiros/muzzle) |
| [AgentDoS](https://www.usenix.org/conference/usenixsecurity26/presentation/luo) | 定向灰盒 fuzzing 发现 agent 资源滥用/DoS 漏洞 | `code_not_found` |
| PANGOLIN | LLM agent 生成跨语言固件输入规格并反馈修正 fuzzing | `code_not_found` |
| Bulbasaur | LLM 在线生成 branch-specific mutator | `code_not_found` |
| Do Not Mention This to the User | 检测和动态验证恶意 agent skills | `artifact_pending` |
| SoK: Attack and Defense Landscape of Agentic AI Systems | 综述/追踪入口，不作方法终点 | 不适用 |

### IEEE S&P 2026

官方入口：[IEEE S&P 2026 Accepted Papers](https://sp2026.ieee-security.org/accepted-papers.html)

已核实代码的强相关方法：

- **Agentic Concolic Execution / ConcoLLMic**：[代码](https://github.com/ConcoLLMic/ConcoLLMic)。Agent 与 concolic execution 结合生成触发路径/漏洞的输入。
- **Cottontail**：DOI `10.1109/SP63933.2026.00110`，arXiv `2504.17542`，[代码](https://github.com/Cottontail-Proj/cottontail)。面向高度结构化输入的 LLM-driven concolic execution。
- **Incalmo**：arXiv `2501.16466`，[代码](https://github.com/bsinger98/incalmo)。自主多主机网络红队测试。

其他强相关包括 PromptLocate、agentic-browser site isolation、AI-agent data permissions、dark patterns 对 Web agents 的影响、LLM-driven web-agent scraping、LLM CLI/GPU-driver fuzzing 等，代码仍待核验。

### NDSS 2026

官方入口：[NDSS 2026 Accepted Papers](https://www.ndss-symposium.org/ndss2026/accepted-papers/)

| 论文 | 核心内容 | 代码状态 |
|---|---|---|
| FirmAgent | fuzzing feedback 辅助 LLM agent 发现 IoT firmware 漏洞/生成 PoC | **`verified_code`**：[vul337/FirmAgent](https://github.com/vul337/FirmAgent) |
| ObliInjection | multi-source data 下的 order-oblivious prompt injection | **`verified_code`**：[ReachalWang/ObliInjection](https://github.com/ReachalWang/ObliInjection) |
| ACE | structured plan 静态验证 + capability/data barriers | `code_pending_verification` |
| SAGA | agent 身份、委托、策略治理 | `code_pending_verification` |
| ToolHijacker | 对 LLM agent tool selection 的 prompt injection | `code_not_found` |
| Chimera | multi-agent insider-threat simulation | `code_not_found` |
| Les Dissonances | cross-tool harvesting/polluting | `code_not_found` |

### ACM CCS 2026

官方入口：[CCS 2026 Accepted Papers](https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html)

| 论文 | 核心内容 | 代码状态 |
|---|---|---|
| CVE-Genie | multi-agent 自动复现 CVE | **`verified_code`**：[BUseclab/cve-genie](https://github.com/BUseclab/cve-genie) |
| PBFuzz | PLAN–IMPLEMENT–EXECUTE–REFLECT 的 agentic directed fuzzing/PoV generation | **`verified_code`**：[sgzeng/pbfuzz](https://github.com/sgzeng/pbfuzz)；artifact DOI `10.5281/zenodo.20769185` |
| MirrorGuard | simulation-to-real reasoning correction，保护 computer-use agents | **`verified_code`**：[WhitzardAgent/MirrorGuard](https://github.com/WhitzardAgent/MirrorGuard) |
| Mind the Gap: Action Rebinding Attacks against Android GUI Agents | 攻击 GUI agents | `code_not_found` |
| BACAgent | agent 自动发现 Web broken-access-control 漏洞 | `code_not_found` |
| LLM-Driven Fuzzing of JavaScript Engines in PDF Readers | 从文档生成输入并 fuzz | `code_not_found` |

## 6. 代码已核实的 2026 核心集

当前严格核实“正式/官方 accepted venue + 具体方法 + 对应公开实现”的高优先级集合：

1. WebTestPilot — FSE 2026
2. Datura — ISSTA 2026
3. RedTeamCUA — ICLR 2026 Oral
4. Terminal-Bench — ICLR 2026
5. MCPMark — ICLR 2026
6. MCP-SafetyBench — ICLR 2026
7. MUZZLE — USENIX Security 2026
8. Agentic Concolic Execution / ConcoLLMic — IEEE S&P 2026
9. Cottontail — IEEE S&P 2026
10. Incalmo — IEEE S&P 2026
11. FirmAgent — NDSS 2026
12. ObliInjection — NDSS 2026
13. CVE-Genie — CCS 2026
14. PBFuzz — CCS 2026
15. MirrorGuard — CCS 2026
16. GameDevBench — ICML 2026
17. SafeHarbor — ICML 2026

## 7. 顺藤摸瓜链

### 测试 agent 本身

AgentBoard/轨迹评测（2024）
→ AgenTracer、Aegis、DoVer（ICLR 2026：故障归因、错误生成、干预式调试）
→ AgentInspect、LogicHunter（ISSTA 2026：coverage、异常工具、agentic oracle）
→ WebTestPilot（FSE 2026：可执行 GUI oracle）。

### 工具链与 prompt injection

早期 prompt-injection benchmark
→ ToolHijacker / ObliInjection（NDSS 2026）
→ ACE / SAGA / MirrorGuard（验证、治理、防御）
→ MUZZLE、Datura、RedTeamCUA（自适应、链式、跨 Web–OS 红队测试）。

### AgentFuzz 后续安全测试

AgentFuzz（USENIX Security 2025）
→ AgentDoS（USENIX 2026：资源滥用漏洞）
→ FirmAgent（NDSS 2026：fuzz feedback + agent）
→ PBFuzz / CVE-Genie / BACAgent（CCS 2026：PoV、CVE 复现、访问控制漏洞）。

## 8. 结论与限制

2026 年不是论文少，而是研究已快速分化为四条主线：

1. agent-specific coverage、轨迹归因和可诊断 oracle；
2. MCP/工具调用链、computer-use agent 和多 agent 安全测试；
3. agentic fuzzing、concolic execution、CVE/PoC 自动复现；
4. 用 tester/mutator/persona agents 执行软件测试。

主要空白仍是：跨模型/版本可重放、非确定性统计、统一的轨迹覆盖、可解释 oracle，以及“发现漏洞后自动生成最小权限策略和长期回归测试”的闭环。

本轮已扫描已公布的主要官方列表。**NeurIPS 2026 尚未通知**，因此报告不能宣称覆盖该会议的最终论文；后续应在 2026-09-24 官方结果发布后增量补查。
