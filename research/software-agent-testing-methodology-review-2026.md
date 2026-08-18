# 软件智能体测试方法学：主流方法、代表工作与研究空白

> 检索截止：2026-08-15。本文的“测试”对象是会规划、调用工具、改变环境或与其他 Agent 协作的软件智能体系统，而不是普通单轮 LLM 问答。详细证据见 [`software-agent-testing-evidence-2026.csv`](./evidence/software-agent-testing-evidence-2026.csv)，检索记录见 [`software-agent-testing-search-log-2026.md`](./software-agent-testing-search-log-2026.md)。

## 1. 一页结论

软件智能体测试的核心不是“给模型更多题”，而是在可控的初始状态下执行多步任务，观察轨迹和外部副作用，并判断结果、过程、安全、稳定性和成本是否同时合格。最小测试对象应是 `初态 + 目标 + 权限/政策 + 工具 + 扰动/故障 + 轨迹 + 终态 + oracle`，而不是 `prompt + answer`。

当前主流方法可按测试生命周期分为八类：

| 方法类别 | 解决的核心问题 | 首选代表 | 当前成熟度 |
|---|---|---|---|
| 场景/用例生成 | 怎样系统产生高价值任务、攻击和 hard negative | ATA、SIRAJ、Erroneous Planning | 中 |
| 可控环境与沙箱 | 如何可重置、可观察地执行并隔离副作用 | AppWorld、ToolSandbox、AgentDojo | 高 |
| 状态/轨迹/复合 oracle | 如何判定结果和过程是否真正正确 | AppWorld、AgentBoard、Process Evaluation | 高 |
| 重复、扰动与回归 | 如何区分偶然成功与可依赖行为 | τ-bench、AI Agents That Matter、ReliabilityBench | 中高 |
| 模糊/对抗/安全红队 | 如何主动发现注入、越权和长轨迹风险 | AgentDojo、SIRAJ、VeriGrey/FLARE | 安全红队高；灰盒早期 |
| 故障注入与混沌测试 | 如何验证故障确实触发、传播并被恢复 | AgentChaos、MAS-FIRE、OrchestraBench | 早中期 |
| 诊断与根因定位 | 哪个 Agent、哪一步、哪类错误导致失败 | REFLECT、StepFinder、VerifyMAS | 中 |
| 可观测性、重放与持续验证 | 如何把生产 trace 变成回归、归因和告警证据 | AgentOps、AgentDebugX、Agentic CLEAR | 早中期 |

最有实践价值的 oracle 不是单一 LLM Judge，而是“可执行终态断言 + 允许/禁止的状态差分 + 里程碑/时序规则 + 经校准的局部语义 Judge + 必要时的重放”。AgentRewardBench 与 AJ-Bench 表明，评测器自身也是需要单独测试的系统组件 [lu2025agentrewardbench; shi2026ajbench]。

## 2. 边界、检索和证据

### 2.1 纳入与排除

纳入 2023–2026 年直接测试工具调用、Web/GUI、代码、企业工作流或相关多智能体系统的论文；早于 2023 年的工作只在它提供必要方法基础时追溯。论文必须贡献可复用的测试生成、执行、oracle、注错、诊断、回归或监控方法。仅给出任务集和能力排行榜的 benchmark 不进入主线；当 WebArena、OSWorld、SWE-bench 等提供独特的环境或 oracle 设计时，才作为支撑证据。

本轮以仓库已有 102 篇证据库（42 篇 core-method）37 篇 supporting-benchmark）23 篇 background）为基础，用六个英文查询族对 Semantic Scholar、OpenAlex、Crossref、arXiv 和 DBLP 做增量检索。详细查询、来源错误和筛选规则保存在检索日志。

### 2.2 证据等级

- **全文已检查**：可支撑方法细节、实验结论和局限。
- **摘要已检查**：只用于概括目的、高层方法和作者报告的结论；不支撑细粒度比较。
- **元数据已检查**：只用于论文身份和发现。
- **已核验**：Crossref 与 OpenAlex 一致，或 DOI/出版方权威记录解决身份；没有 DOI 的预印本只标为部分核验。

代表性依次考虑主题相关性、方法匹配、证据质量、可复用性、时间影响与引用信号，不用引用数单独排名。

## 3. 八类主流测试方法

### 3.1 测试场景与用例生成

**方法。** 从需求、角色、工具 schema、政策、攻击面或已有 trace 生成目标、初态、扰动和预期性质。典型反馈是失败是否被触发、场景多样性、覆盖的风险/规则类别和执行成本。

**代表。** Erroneous Planning 用合成用户输入定向触发规划错误 [ji2024erroneousplanning]；ATA 把用例生成、执行和评估组成测试 Agent [komoravolu2026ata]；SIRAJ 用蒸馏的结构化推理生成多样、高效的 Agent 红队测试 [zhou2026siraj]。

**局限。** 生成器和被测 Agent 若来自同类模型，可能共享盲区；语义多样不等于状态、权限或轨迹分支覆盖。成熟方案需要将自动生成与需求/风险 taxonomy、去重、可执行性检查和人工抽样结合。

### 3.2 可控执行环境、模拟器与沙箱

**方法。** 在可重置的网站、OS、数据库或工具世界中执行，保存每步观察、动作、状态差分与成本；也可用 LM 模拟工具将高风险动作留在隔离环境。

**代表。** AppWorld 用可控 App/数据库世界支持可执行状态检查 [trivedi2024appworld]；ToolSandbox 提供有状态工具交互、milestone DAG 和 minefield DAG [lu2025toolsandbox]；AgentDojo 在同一环境中分别验证用户效用与攻击者目标 [debenedetti2024agentdojo]；ToolEmu 用 LM 模拟沙箱识别工具 Agent 风险 [ruan2024toolemu]。WebArena、OSWorld 和 SWE-bench 在本文中是支撑型环境/oracle，不是独立测试方法 [zhou2024webarena; xie2024osworld; jimenez2024swebench]。

**局限。** 高保真环境昂贵且会漂移；模拟环境又可能丢失真实 API 的时序、并发和错误语义。报告必须锁定环境、工具 schema、地区/时区、模型和 harness 版本，并区分 Agent failure 与 infrastructure failure。

### 3.3 状态、轨迹和复合 Oracle

**方法。** 终态 oracle 检查数据库、文件、页面或测试套件；轨迹 oracle 检查里程碑、必要确认、工具参数、动作偏序、循环和禁止事件；语义 Judge 只处理难以编码的局部问题。

**代表。** AppWorld 分开 `expected changes` 与 `allowed changes`，可发现 collateral damage [trivedi2024appworld]；AgentBoard 用人工子目标计算 progress rate [ma2024agentboard]；ToolSandbox 用 DAG 接受多条合法路径并检查禁止状态 [lu2025toolsandbox]；Process Evaluation 用过程问题和 rubric 识别“答案正确但过程有问题” [gritta2026processevaluation]。

AgentRewardBench 用专家轨迹元评测自动 evaluator，发现规则 evaluator 和 LLM Judge 有不同的精度/召回偏差 [lu2025agentrewardbench]；AJ-Bench 进一步测试会主动访问环境的 Agent-as-a-Judge，但工具能力与评估推理仍然耦合 [shi2026ajbench]。

**局限。** 终态相同不代表过程合规；固定参考轨迹会错杀合法多路径；开放 Judge 则会被 Agent 自述、错误证据或同源模型偏差误导。应将 Judge 与人类标注、可执行状态和对抗样例单独校准。

### 3.4 重复、扰动、差分与回归测试

**方法。** 同一任务多 seed/多次执行，对等价输入、页面布局、工具返回、时区、模型或 harness 版本做配对扰动，比较成功分布、轨迹差异、成本和失败簇。

**代表。** τ-bench 的 `pass^k` 测量同一任务连续 k 次成功，而不是“多试几次总有一次成功” [yao2025taubench]；AI Agents That Matter 强调脚手架、成本、重复次数和统计不确定性 [kapoor2025aiagentsmatter]；ReliabilityBench 将 Agent 放入生产式压力与故障中 [gupta2026reliabilitybench]；Beyond pass@1 将长时程 Agent 评估表述为可靠性科学问题 [khanal2026beyondpass1]。

**局限。** `pass@1`、`pass^k` 和 `pass@k` 回答不同问题，不能混用。任务不独立、环境漂移与服务端模型变化会污染回归结果；需保存环境快照、轨迹、版本和失败原因，并报告置信区间而非单点分数。

### 3.5 模糊测试、对抗测试与安全红队

**方法。** 在 prompt、工具输出、网页、记忆、工具池和多轮轨迹中注入恶意或异常内容；用效用成功、攻击目标、越权状态和禁止工具调用做联合 oracle。灰盒方法进一步使用 Agent 状态或轨迹反馈引导输入变异。

**代表。** InjecAgent 和 AgentDojo 是工具 Agent 间接 prompt injection 的主要动态测试载体 [zhan2024injecagent; debenedetti2024agentdojo]；SIRAJ 代表自动化结构红队 [zhou2026siraj]；Les Dissonances 研究工具池中的跨工具收集与污染 [li2026lesdissonances]。VeriGrey 和 FLARE 分别代表灰盒 Agent 验证和 coverage-guided 多 Agent fuzzing，但本综述对其只作摘要级判断 [zhang2026verigrey; hui2026flare]。

**局限。** 攻击成功率必须与正常任务效用联合报告，否则“拒绝一切”会显得完全安全。当前仍没有被广泛接受的 Agent 覆盖语义；代码覆盖无法表示权限边界、轨迹分支、工具参数、状态转移或风险规则覆盖。

### 3.6 故障注入、混沌测试与恢复能力

**方法。** 在 LLM/API 边界注入 crash、omission、延迟或 value fault，或在语义/编排层注入错误委派、消息损坏、角色偏移和依赖故障。测试必须首先证明故障已触发，再测量成功下降、检测、传播半径、恢复率和成本。

**代表。** AgentChaos 在共享 HTTP 边界程序化注入 API 故障，并验证注错是否实际触发 [tan2026agentchaos]；MAS-FIRE 覆盖语义与协调故障，并比较多 Agent 架构的容错 [jia2026masfire]；OrchestraBench 测量编排故障、恢复、级联与任务分解 [chen2026orchestrabench]。

**局限。** 研究者设计的故障分布尚未被生产 incident 频率和严重度校准。API 注错跨框架但看不到内部语义；修改 prompt/消息能表达语义故障，但高度依赖具体 harness。生产方案应同时有 transport/API 和 semantic/orchestration 两层故障模型。

### 3.7 失败诊断、根因定位与多 Agent 归因

**方法。** 将轨迹转换为责任 Agent、错误类型、首个决定性步骤或可修复点；使用多视角 Judge、三值假设验证、时序异常排序或保持前缀的干预重放进行检查。

**代表。** VerifyMAS 先在全轨迹上验证错误假设，再归因责任组件 [qiao2026verifymas]；StepFinder 将定位转为 Agent-aware 的轻量时序异常排序 [zhu2026stepfinder]；REFLECT 通过定向 patch 和前缀重放，用 outcome flip 反馈候选归因 [lin2026reflect]；Seeing the Whole Elephant 说明输入、metadata 和完整 trace 决定归因上限 [chen2026seeingwholeelephant]。

**局限。** source、first decisive step、symptom manifestation 和 recovery opportunity 不是同一标签。Outcome flip 只证明某次干预足以改变结果，不证明它是唯一或最小根因。评测应报告 Agent accuracy、exact/±1 step accuracy、类别 F1、误报、未知错误与重放成本。

### 3.8 线上可观测性、重放与持续验证

**方法。** 用统一事件 schema 记录 prompt、观察、工具调用、状态、成本和版本；把生产失败聚类、脱敏、固化为离线回归案例，必要时在可重置环境中局部重放。

**代表。** AgentOps 提出 Agent 全生命周期可观测基础 [dong2024agentops]；AgentDebugX 将采集、归因、修复和重跑连成闭环 [zhu2026agentdebugx]；Agentic CLEAR 组织 system–trace–node 多层评估和跨轨迹聚合 [yehudai2026agenticclear]。AgentTelemetry、AgentTrace 和 Causal Agent Replay 是值得跟踪的前沿，但本轮只有摘要级证据，不用它们支撑详细结论。

**局限。** 完整 trace 可能包含凭据、PII、文件、屏幕截图和内部推理；删除字段又可能降低可诊断性。应默认最小化采集、字段级脱敏、本地/受控存储、访问审计和重放权限门控。

## 4. 横向比较：测试可见性与 Oracle

| 视角 | 可见信息 | 优势 | 主要盲区 | 典型用途 |
|---|---|---|---|---|
| 黑盒 | 用户输入、最终输出、外部终态 | 跨框架，接近验收视角 | 难以解释失败和中途违规 | 业务验收、版本对比 |
| 灰盒 | 再加工具调用、状态摘要、轨迹事件或覆盖反馈 | 能引导测试生成并定位错误 | trace schema 不统一，可能泄露敏感信息 | fuzzing、轨迹回归、归因 |
| 白盒 | 再加规划器、记忆、路由、编排和内部状态 | 最强的组件级注错与诊断 | 对实现耦合，跨框架性差 | 单元/集成测试、编排混沌测试 |

| Oracle | 最适合 | 主要问题 |
|---|---|---|
| 精确终态/测试套件 | 数据库、文件、代码和可查询系统 | 可能漏掉中途泄露、时序和副作用 |
| 状态差分 | 需要限定允许变更的工作流 | 声明成本高，初态必须稳定 |
| 里程碑/规则/DAG | 多条合法路径和时序约束 | 规则不完备会形成 oracle gap |
| LLM/Agent Judge | 开放语义、工作区检查和大规模预筛 | 偏差、不稳定、证据 grounding 不足；必须元评测 |
| 人工评审 | 金标抽样、高风险争议案例 | 贵、慢、标注者也会不一致 |
| 重放/干预 | 验证故障触发、修复充分性和候选因果 | 随机性和环境变化会污染反事实 |

## 5. 工程落地：一套最小可用的 Agent QA 栈

1. **先定义事件和状态。** 每个案例固定目标、初态、身份/权限、工具 schema、预算、允许变更、必要里程碑和禁止事件。
2. **分层测试。** 先测工具契约、幂等、超时和错误语义，再测模型–规划器–工具闭环，最后跑可重置的系统/验收场景。
3. **组合 oracle。** 精确终态和状态差分优先，轨迹规则补过程，Judge 只用于剩余语义并持续用人工金标校准。
4. **把可靠性当一等结果。** 对关键任务多次执行，报告成功率、`pass^k`、置信区间、成本/延迟分布和失败簇。
5. **主动注入扰动。** 覆盖工具超时、空/null/malformed 返回、权限拒绝、部分成功、重复执行、状态漂移、间接注入和错误委派。
6. **保存可重放证据。** 对失败保存脱敏 trace、环境快照、模型/harness 版本、seed 和 oracle 证据；自动重放必须受权限、预算和人工门控。
7. **用生产失败更新回归集。** 合并语义重复案例，保留失败簇、频率、严重度和发现版本，避免回归集只由合成测试构成。

## 6. 共识、冲突与研究空白

### 6.1 较稳固的共识

- 最终任务成功率必要但不充分；轨迹、副作用、政策和成本都必须可独立审计。
- 同一任务一次成功不能表示生产可靠；重复、扰动和版本差分应进入 CI/验收。
- 安全与效用必须联合报告；拒绝正常任务不是合格的安全。
- Evaluator/Judge 不是外部金标，而是一个有自己精度、召回、偏差、成本和攻击面的子系统。
- 环境、模型、脚手架和评测器共同决定分数；跨论文横向排名必须先检查这些条件是否可比。

### 6.2 尚未解决的冲突

- **环境真实性 vs. 可复现性：** 真实 Web/API 保真但会漂移；模拟器稳定但可能错过真实故障。
- **开放语义 vs. 确定 oracle：** 规则可审计但不完备；Judge 灵活但不稳定。
- **完整 trace vs. 隐私：** 更多上下文提高归因，但同时提高凭据、PII 和内部数据泄露风险。
- **多路径正确性 vs. 回归可比性：** 固定轨迹易比较却过严；只看终态又会漏过程问题。

### 6.3 最值得继续研究的空白

1. **Agent 专属覆盖标准。** 需要能统一状态、轨迹分支、工具/参数、权限边界、政策和故障触发的覆盖概念。
2. **可移植复合 oracle。** 当前状态断言、DAG 和 Judge 多与单一 benchmark 绑定，缺少跨 Web、代码和企业工作流的通用表达。
3. **故障模型的生产校准。** 需要从真实 incident/telemetry 推导故障频率、相关性、严重度和级联结构。
4. **多根因与反事实真值。** 现有数据常假设单个责任 Agent/步骤，无法表达协同失效、错误恢复点和多个充分原因。
5. **Flakiness 预算与统计协议。** 领域尚无统一的重复次数、置信区间、配对比较、任务层级模型和回归门限。
6. **跨框架 trace 语义。** 没有稳定的观察、动作、工具、记忆、委派、错误和副作用 schema，诊断器难以迁移。
7. **隐私–可诊断性曲线。** 需要量化删除/脱敏哪些字段会造成多大诊断损失，而不是默认保存全量 trace。
8. **安全的自动重放与修复。** 回放可能重复付款、删除或发送消息；需要幂等契约、权限、预算、沙箱和人工审批协议。

## 7. 25 篇分层阅读路线

### A. 先建立测试心智模型（7 篇）

1. **AppWorld**：状态差分和 collateral damage oracle [trivedi2024appworld]。
2. **ToolSandbox**：milestone/minefield DAG 与有状态工具交互 [lu2025toolsandbox]。
3. **AgentDojo**：效用–安全联合评估 [debenedetti2024agentdojo]。
4. **AgentBoard**：轨迹子目标和 progress rate [ma2024agentboard]。
5. **τ-bench**：重复可靠性与 `pass^k` [yao2025taubench]。
6. **AI Agents That Matter**：成本、统计与 harness 影响 [kapoor2025aiagentsmatter]。
7. **AgentRewardBench**：先学会怀疑 evaluator [lu2025agentrewardbench]。

### B. 再掌握自动生成与安全测试（6 篇）

8. **Testing and Understanding Erroneous Planning** [ji2024erroneousplanning]。
9. **Agent-Testing Agent (ATA)** [komoravolu2026ata]。
10. **SIRAJ** [zhou2026siraj]。
11. **InjecAgent** [zhan2024injecagent]。
12. **Les Dissonances** [li2026lesdissonances]。
13. **VeriGrey**（摘要级前沿）[zhang2026verigrey]。

### C. 学习故障注入和恢复（3 篇）

14. **AgentChaos** [tan2026agentchaos]。
15. **MAS-FIRE** [jia2026masfire]。
16. **OrchestraBench** [chen2026orchestrabench]。

### D. 深入轨迹判定和失败归因（6 篇）

17. **Process Evaluation for Agentic Systems** [gritta2026processevaluation]。
18. **AJ-Bench** [shi2026ajbench]。
19. **VerifyMAS** [qiao2026verifymas]。
20. **StepFinder** [zhu2026stepfinder]。
21. **REFLECT** [lin2026reflect]。
22. **Seeing the Whole Elephant** [chen2026seeingwholeelephant]。

### E. 最后连到工程闭环（3 篇）

23. **ReliabilityBench** [gupta2026reliabilitybench]。
24. **AgentDebugX** [zhu2026agentdebugx]。
25. **Agentic CLEAR** [yehudai2026agenticclear]。

## 8. 核验冲突和证据限制

- 25 篇阅读路线中，VeriGrey 只作摘要级前沿；其余详细结论来自本地全文笔记。
- AgentChaos 的 DOI 由论文与 OpenAlex 支持，早期 Crossref 曾尚未解析；证据表保留该来源差异。
- AgentSpec、AgentTelemetry、AgentTrace、FALAT 和 Causal Agent Replay 等有主题价值，但本轮全文/正式身份不足，没有用于细粒度结论。
- 2026 预印本密集且数据库收录滞后；本文将“方法值得跟踪”与“方法已被独立验证”严格分开。
- 目前公开论文的生产 trace 证据很少，多数故障、攻击和诊断结论来自合成或 benchmark 环境；外部效度仍是最大限制。

## 9. 引用与可追溯性

本文使用仓库 [`references.bib`](./references.bib) 中的 BibTeX 引文键。证据表保存每篇论文的 DOI/arXiv ID、来源覆盖、版本关系、证据等级、主要限制和核验状态。无 DOI 预印本不会因 Crossref 没有记录而被写成“无效”；它们会被标为 arXiv 身份已核对、正式版本未核验。
