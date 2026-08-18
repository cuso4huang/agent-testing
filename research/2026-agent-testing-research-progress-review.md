# AI Agent 测试研究进展：方法谱系、代表工作与前沿方向

> 面向研究组的精炼调研报告；检索与版本核验截止 2026-08-18。
>
> 本文所称“Agent 测试”，是指被测对象为基于大语言模型的 Agent 或 Agentic System，而不是“使用 Agent 去测试普通软件”。正文中的“正式”表示已核验会议、期刊或出版方记录；“预印本”表示只有 arXiv 等公开版本，不能等同于经过同行评审；“摘要级前沿”只用于说明研究动向，不支撑细粒度方法或实验结论。

## 1. 执行摘要

AI Agent 测试的研究对象，已经从一次性的 `(prompt, answer)` 扩展为一个有状态、会行动、能改变外部世界的执行闭环：

```text
目标与权限
  -> 观察环境
  -> 规划、记忆和选择工具
  -> 执行动作并产生副作用
  -> 接收工具/用户/其他 Agent 的反馈
  -> 重规划、恢复或终止
  -> 环境终态、完整轨迹、成本与风险
```

这使 Agent 测试同时面对传统软件故障、模型概率性、开放语义、动态环境和外部副作用。最终答案正确，并不表示过程合规；一次任务成功，也不表示重复运行可靠；攻击成功率低，也可能只是 Agent 根本不会完成任务；一条自动评分为“成功”的轨迹，还可能是评测器被 Agent 自述误导。

截至 2026 年 8 月，研究大致经历了三个阶段：

1. **2023-2024：环境和 benchmark 奠基。** WebArena、SWE-bench、AppWorld、AgentBoard、AgentDojo 等工作把 Agent 放进可执行 Web、代码、应用和工具环境，开始用环境终态、测试套件、子目标和安全副作用代替纯文本评分（Zhou 等, 2024；Jimenez 等, 2024；Trivedi 等, 2024；Ma 等, 2024；Debenedetti 等, 2024）。
2. **2025：评价方法本身成为研究对象。** τ-bench 用 `pass^k` 强调连续成功，AI Agents That Matter 强调成本、重复、脚手架和统计可比性，AgentRewardBench 则直接测试 evaluator 是否可信（Yao 等, 2025；Kapoor 等, 2025；Lù 等, 2025）。
3. **2026：从“做榜单”走向“做测试方法”。** 自动用例生成、灰盒 fuzzing、故障注入、混沌测试、轨迹归因、反事实重放和线上可观测性形成新的方法簇。与此同时，最新实证研究 Tangent 发现，开源 Agent 项目仍以窄范围单元测试、重 mocking、简单数据和浅层断言为主，研究方法与工程实践之间仍有明显断层（Pan 等, 2026）。

当前较稳固的结论不是“哪一个 benchmark 最好”，而是：**Agent 测试需要把可控环境、复合 Oracle、重复与扰动、主动注错、失败归因和生产 trace 连成闭环。** 最成熟的是可执行环境和状态型 Oracle；增长最快的是安全测试、可靠性、故障注入和轨迹诊断；最薄弱的是 Agent 专属覆盖率、可移植复合 Oracle、长期状态、生产故障校准以及隐私安全的可观测性。

## 2. 调研范围、证据与研究边界

本报告以项目中的宽口径证据库为起点：`research/evidence/evidence-table.csv` 含 111 条记录，其中 58 篇标为已阅读全文；主体方法论以 `software-agent-testing-evidence-2026.csv` 的 25 篇严格核心集为骨架，其中 24 篇全文、1 篇摘要。另以本地综述、结构化笔记和 PDF 复核 Web、代码、工具、记忆与多智能体方向。

检索范围为 2020-2026，重点是 2023 年以后直接测试 Agent、Agent 轨迹、harness 或多智能体编排的论文。只把普通 LLM 评测作为 evaluator 背景；只提供任务和排行榜、没有独特测试环境或方法贡献的工作，不与测试方法论文并列。

为补齐截止日期，本轮还全文核读了两篇新增候选：

- **Tangent**：分析 240 个测试模块中的 2,572 个测试方法，并访谈 10 名产业实践者。论文首页和 ASE 2026 官方日程确认其接收身份，但 DOI 在 Crossref/OpenAlex 尚未入库，因此记为“ASE 2026 接收稿、结构化元数据待入库”（Pan 等, 2026）。
- **Validation Evidence in LLM Repair Agents**：提出 BSG-VA，将代码修复 Agent 的验证命令分别在 buggy、candidate 和 gold-fix 状态重放。其 Crossref 题名查询只返回无关模糊匹配，故仅按 arXiv 预印本引用（Xu 与 Wu, 2026）。

本报告不是严格意义上的穷尽式系统综述。详细结论仅来自已检查全文；摘要级工作只说明目标和高层方法；不同论文的 success rate、ASR、cost 和 judge 分数定义不同，本文不把它们拼成统一排行榜。

## 3. Agent 测试与传统测试、普通 LLM 评测的区别

| 维度 | 传统软件测试 | 普通 LLM 评测 | Agent 测试 |
|---|---|---|---|
| 最小对象 | 函数、组件、系统 | 一次输入输出 | 目标、初态、轨迹、终态和副作用 |
| 执行路径 | 主要由代码控制流决定 | 通常单轮推理 | 模型动态规划、选工具、重试和重规划 |
| Oracle | 精确值、异常、状态断言 | exact match、偏好或 Judge | 状态差分、里程碑、禁区、Judge 和人工复核的组合 |
| 状态 | 进程和数据库状态 | 上下文窗口 | 环境、记忆、工具、共享消息和外部服务共同演化 |
| 不确定性 | 环境和并发为主 | 模型采样 | 模型、harness、用户/工具模拟器、外部环境共同引入 |
| 主要风险 | 错误输出、崩溃、性能和安全漏洞 | 幻觉、偏见、对齐问题 | 越权动作、错误副作用、循环、成本失控和级联失败 |
| 复现条件 | 代码、依赖、数据、环境 | 模型、提示、参数 | 还需工具 schema、权限、初态、trace、评测器和环境快照 |

因此，一个可执行的 Agent 测试用例至少应包含：目标、初始环境与记忆、身份和权限、可用工具及 schema、用户或同伴行为、扰动/攻击/故障计划、预算、必要里程碑、禁止事件、预期变化和允许变化。结果则应保存终态、完整动作轨迹、外部副作用、版本、成本、延迟和 Oracle 证据。

## 4. 八个主要研究方向

### 4.1 测试场景与用例自动生成

**研究问题。** 自然语言目标空间巨大，手写长程场景昂贵；自动生成既要覆盖不同约束、角色、环境和攻击，又要保证任务可执行、Oracle 可判定，不能只生成“看起来困难”的提示。

**方法进展。** PDoctor 从 DSL 合成带顺序和时间约束的用户请求，再用 Z3 检查可满足性，并以 mock tool 的实际调用序列作为确定性 Oracle；它把规划错误测试从自然语言主观判断收缩为约束违反，但只覆盖作者定义的动作语义（Ji 等, 2024）。ATA 进一步用 meta-agent 分析被测 Agent、询问开发者、检索相关风险、生成 persona 和测试，并根据 Judge 反馈提高难度，代表“测试 Agent 生成 Agent 测试”的方向（Komoravolu 与 Mrini, 2026）。SIRAJ 则把结构化风险推理蒸馏进自动红队流程，根据 Agent 定义生成风险种子，并利用前一轮攻击轨迹迭代（Zhou 等, 2026）。

**代表工作。** PDoctor（预印本，全文）、ATA（EACL 2026，全文）、SIRAJ（Findings EACL 2026，全文）。Tangent 不是生成器，但其大规模实证发现 39.9% 的测试仍使用简单示例式数据，说明系统化场景生成尚未进入主流工程实践（Pan 等, 2026）。

**局限。** 生成器、被测 Agent 和 Judge 常使用相近模型，容易产生相关偏差；DSL 和 mock 保证可判定，却会损失真实环境语义；开放式生成又容易产生不可执行任务和错误 Oracle。下一步需要需求/策略驱动的场景生成、独立可执行验证、失败测试最小化，以及从生产 incident 反向生成回归案例。

### 4.2 可控环境、沙箱与系统级执行

**研究问题。** Agent 的正确性依赖真实动作和环境变化，静态问答无法验证“是否真的执行”；真实 Web/API 又会漂移、产生费用或带来不可逆风险，因此需要可重置且足够真实的执行环境。

**方法进展。** WebArena 通过自托管网站和任务特定 evaluator 建立 Web 系统测试；SWE-bench 用仓库和测试套件判断代码补丁；AppWorld 以跨应用数据库状态差分检查 expected changes 和 collateral damage；ToolSandbox 保存逐步世界状态，用 milestone/minefield DAG 表示必要路径和禁区；AgentDojo 则把正常任务、间接提示注入和可执行工具环境组合起来，分别计算任务效用与攻击目标（Zhou 等, 2024；Jimenez 等, 2024；Trivedi 等, 2024；J. Lu 等, 2025；Debenedetti 等, 2024）。

**代表工作。** WebArena（ICLR 2024）、SWE-bench（ICLR 2024 Oral）、AppWorld（ACL 2024）、ToolSandbox（Findings NAACL 2025）、AgentDojo（NeurIPS 2024 Datasets and Benchmarks），均已阅读全文。

**局限。** 自托管环境可复现但真实性有限，真实网站保真却会漂移；模拟器自身会幻觉或违反状态约束；环境初始化、时间、地区、浏览器、API 和身份权限都会改变结果。环境必须像测试夹具一样版本化，并分别报告 agent failure、environment failure 和 evaluator failure。

### 4.3 状态、轨迹与复合 Oracle

**研究问题。** 多条轨迹都可能正确，终态相同也可能在过程中越权；开放任务又难以完全程序化判定。核心问题是怎样组合确定性状态、过程规则、语义 Judge 与人工金标。

**方法进展。** AgentBoard 用子目标 progress rate 解释 Agent 在哪一步停滞；ToolSandbox 的里程碑和雷区 DAG 允许多条合法路径，同时约束关键偏序；Process Evaluation 将“是否遵循必要流程”从答案正确性中分离（Ma 等, 2024；J. Lu 等, 2025；Gritta 等, 2026）。AgentRewardBench 用专家标注轨迹反过来测试 evaluator，发现其所测 LLM Judge 的成功判断 precision 均未超过 70%，而规则 evaluator 精度较高、召回不足，说明 Judge 自身必须有回归集（Lù 等, 2025）。AJ-Bench 再进一步测试能主动访问搜索、数据系统和 GUI 环境的 Agent-as-a-Judge，区分信息获取、状态验证和过程验证（Shi 等, 2026）。Plan-RewardBench 则通过受控 hard negative 测试轨迹级 reward model 是否真正理解规划错误，而不是只识别表面差异（Wang 等, 2026）。

代码 Agent 的新增证据也很有启发。BSG-VA 对 3,730 个验证事件进行 buggy/candidate/gold-fix 三状态重放，发现 46.0% 的正向可比较事件没有区分原始缺陷，23.8% 的基线 rollout 仅凭这类证据结束。该结果来自单一预印本和有限模型/任务设置，但清楚说明“Agent 跑过一个通过的测试”不等于“该测试验证了目标缺陷”（Xu 与 Wu, 2026）。

**代表工作。** AgentBoard、AgentRewardBench、Process Evaluation、AJ-Bench、Plan-RewardBench，均为正式论文且已全文检查；BSG-VA 为新增全文预印本。

**局限。** 固定参考轨迹会错杀等价方案，开放 Judge 会被自述和同源模型偏差误导，人工金标昂贵且不完全一致。较可靠的优先级是：可执行终态/测试套件 > 权限、时序和禁区断言 > 局部语义 Judge > 人工争议升级；同时对 evaluator 单独报告 precision、recall、稳定性、成本和攻击面。

### 4.4 重复、扰动、差分与回归可靠性

**研究问题。** 概率模型即使温度为零也可能因服务端、并发或环境变化而漂移。单次 `pass@1` 只能说明一次运行结果，不能回答连续多次是否可靠、等价输入是否稳定、升级后是否回归。

**方法进展。** τ-bench 提出 `pass^k`，要求同一任务连续 `k` 次全部成功，与“多试几次至少成功一次”的 `pass@k` 明确不同（Yao 等, 2025）。AI Agents That Matter 把模型、harness、成本、重复次数、holdout 和统计不确定性纳入评价设计，反对只比较裸分（Kapoor 等, 2025）。ReliabilityBench 将重复一致性、语义等价扰动和受控工具/API 故障组织为生产式压力维度；Beyond pass@1 则把长程 Agent 评价表述为可靠性科学问题，主张报告成功分布而不是一个点估计（Gupta, 2026；Khanal 等, 2026）。

**代表工作。** τ-bench（ICLR 2025）、AI Agents That Matter（TMLR 2025）为正式全文；ReliabilityBench、Beyond pass@1 为已阅读全文预印本。

**局限。** 当前没有统一的运行次数、置信区间、配对统计和回归门限；任务之间不独立，网站和闭源模型会在实验期间变化。回归测试应固定环境快照和版本，对同一任务做配对运行，报告置信区间、失败簇、每成功任务成本和延迟分布，并区分 flakiness 与确定性功能回归。

### 4.5 安全红队、对抗测试与灰盒模糊测试

**研究问题。** Agent 会把网页、邮件、工具返回和记忆中的自然语言重新解释为指令，攻击能够跨工具、跨轮次和跨 Agent 传播；安全测试还必须避免“拒绝一切”的伪安全。

**方法进展。** InjecAgent 和 AgentDojo 建立间接提示注入的动态工具测试；后者用环境检查函数分别度量 utility 和 targeted ASR（Zhan 等, 2024；Debenedetti 等, 2024）。Les Dissonances 把威胁扩展到工具池中的跨工具信息收集与污染（Li 等, 2026）。AgentDoS 将静态程序分析、资源生命周期、语义种子和运行时资源反馈组合为定向灰盒 fuzzing，在真实开源 Agent 中寻找内存/磁盘耗尽漏洞（Luo 等, 2026）。

2026 年的灰盒路线开始探索 Agent 专属覆盖反馈：VeriGrey 以调用过的工具序列引导 prompt 变异；FLARE 从多智能体实现中抽取主体内和主体间行为空间，再做 coverage-guided fuzzing（Zhang 等, 2026；Hui 等, 2026）。二者目前均是**摘要级预印本前沿**，只能说明方法目标，不能据此认定其覆盖定义已经成熟。

**代表工作。** InjecAgent（Findings ACL 2024）、AgentDojo（NeurIPS 2024）、AgentDoS（USENIX Security 2026）、Les Dissonances（NDSS 2026）均有全文；VeriGrey/FLARE 为摘要级观察项。

**局限。** ASR 必须与正常效用、误拒、成本和真实副作用联合报告。工具序列新颖性、代码覆盖或模型激活都只是风险覆盖的代理；领域尚无统一的状态、权限、轨迹和多 Agent 行为覆盖标准。自适应攻击还会持续击穿固定模板防御，因此安全回归集必须版本化并允许针对具体防御更新。

### 4.6 故障注入、混沌测试与恢复

**研究问题。** Agent 不只会遭受恶意输入，还会遇到 LLM/API 超时、遗漏、错误值、工具部分成功、消息损坏、错误委派和共享状态故障。测试必须证明故障确实触发，并观察检测、传播、恢复和成本。

**方法进展。** ToolEmu 用 LM 模拟高风险工具环境，代表低成本发现后再抽样做真实验证的两阶段路线（Ruan 等, 2024）。AgentChaos 在共享 HTTP 层拦截和修改 LLM API 响应，覆盖 crash、omission 和 value fault，并只对实际触发的任务计算退化（Tan 等, 2026）。MAS-FIRE 将故障提升到多 Agent 的 planning、memory、reasoning、消息和协调语义；OrchestraBench 则单独测量路由、恢复、cascade radius 和任务分解（Jia 等, 2026；Chen 等, 2026a）。

**代表工作。** ToolEmu（ICLR 2024，全文）、AgentChaos（ASE 2026 接收稿，全文）、MAS-FIRE 和 OrchestraBench（全文预印本）。

**局限。** API 层注错跨框架但看不到内部语义，prompt/消息层注错更真实却高度依赖 harness。人工设计的故障分布尚未由生产 incident 的频率、相关性和严重度校准。完整方案应同时覆盖 transport/API、tool/environment 和 semantic/orchestration 三层，并记录 fault-trigger coverage、传播半径、检测时间、恢复率和恢复后的副作用。

### 4.7 失败诊断、根因定位与多 Agent 归因

**研究问题。** 团队失败后，需要区分责任 Agent、错误类型、首次决定性步骤、症状出现步骤和可修复点；这些标签并不等价。只让 LLM 阅读轨迹并解释，很容易产生流畅但不可验证的故事。

**方法进展。** VerifyMAS 先在完整轨迹上验证错误假设，再定位责任 Agent，减少 agent-first 方法对局部显眼错误的偏好（Qiao 等, 2026）。StepFinder 将定位转为 agent-aware 的时序异常排序，降低生成式逐步检查的 token 和延迟（T. Zhu 等, 2026b）。REFLECT 保留原始前缀，在候选步骤注入定向修复并重放，用 outcome flip 检查归因假设（Lin 等, 2026）。Seeing the Whole Elephant 比较 output-only、完整输入/metadata 和可重放环境，证明 trace 可见度本身会显著改变归因上限（Chen 等, 2026b）。AgentDiagnose 则提供多维轨迹 evaluator 和可视化，但其人工验证规模较小，更适合定位为诊断工具而非通用金标准（Ou 等, 2025）。

**代表工作。** StepFinder（KDD 2026）、Seeing the Whole Elephant（ACL 2026）、AgentDiagnose（EMNLP 2025 Demo）为正式全文；VerifyMAS 为全文预印本；REFLECT 为 ICML 2026 workshop 接收稿。

**局限。** 现有数据多假设单一责任 Agent 或单一步骤，难以表达协同失效、多个充分原因和错误恢复机会。一次干预使结果翻转，只能说明该修复在该次运行中足以改变结果，不证明它是唯一或最小根因。评测应分别报告 Agent、错误类别、exact/±1 step、未知错误、证据不足时弃权和重放成本。

### 4.8 可观测性、重放与持续验证

**研究问题。** 离线 benchmark 无法覆盖生产分布；没有统一 trace，又无法复现循环、工具错误、权限变化和跨 Agent 传播。目标是把线上失败转成可脱敏、可聚类、可重放的回归资产。

**方法进展。** AgentOps 从工具盘点中提出 goal、reasoning、planning、workflow、task、tool、evaluation、guardrail 和 LLM 等 span taxonomy，但尚未通过真实故障检测实验验证（Dong 等, 2024）。AgentDebugX 把统一 trace、异常检测、归因、修复建议、人工批准重跑和失败记忆连成工程闭环（K. Zhu 等, 2026c）。Agentic CLEAR 位于观测层之上，组织 node、trace、system 多层诊断与跨轨迹聚合（Yehudai 等, 2026b）。

AgentTelemetry 直接面向 telemetry 的故障检测 benchmark，但本轮只有正式元数据和摘要；Causal Agent Replay 试图用反事实重放做归因，但只有 arXiv 摘要。二者均记为**摘要级前沿**，不用于支撑详细方法结论（Balusu, 2026；Shah, 2026）。

**代表工作。** AgentOps（全文预印本）、AgentDebugX（全文预印本/软件）、Agentic CLEAR（ACL 2026 Demo，全文）；AgentTelemetry 和 Causal Agent Replay 为摘要级观察项。

**局限。** “记录了 trace”不等于“具备 Oracle”。完整 trace 可能包含凭据、PII、文件、截图、客户数据和内部推理；过度脱敏又会损失诊断证据。生产系统需要字段级最小采集、访问审计、防篡改、保留期和重放权限控制，并以故障注入测试 trace 的完整性和检测能力。

## 5. 八个方向的横向比较

| 方向 | 主要测试输入 | 主要 Oracle | 代表指标 | 成熟度判断 | 典型对象 |
|---|---|---|---|---|---|
| 用例生成 | DSL、persona、风险种子、生产失败 | 约束满足、可执行状态、Judge | 有效用例率、错误发现率、多样性 | 新兴；生成质量受 Oracle 限制 | 对话、规划、工具 Agent |
| 可控执行 | 任务、初态、权限、工具/网站 | 测试套件、状态差分、任务 evaluator | success、collateral damage | 较成熟；是系统测试基础 | Web、代码、工具 Agent |
| 复合 Oracle | 完整轨迹、状态快照、rubric | 里程碑、禁区、Judge、人工 | progress、precision/recall、F1 | 核心但未统一 | 所有 Agent |
| 可靠性回归 | 重复 seed、释义、环境/版本扰动 | 配对结果与分布比较 | `pass^k`、置信区间、成本/延迟 | 正在形成规范 | 所有概率 Agent |
| 安全/fuzzing | 注入、恶意工具输出、语义变异 | 攻击目标、禁止动作、资源预算 | utility、ASR、覆盖、漏洞数 | 红队较成熟；覆盖定义前沿 | 工具、Web、MCP、多 Agent |
| 故障/混沌 | API、工具、消息和编排故障 | 触发确认、终态、恢复检查 | trigger coverage、恢复率、传播半径 | 2026 快速增长 | 长程与多 Agent 系统 |
| 诊断归因 | 失败轨迹、错误假设、干预 patch | 人工标签、异常排序、outcome flip | Agent/step accuracy、F1、成本 | 新兴；因果真值不足 | 多 Agent、代码 Agent |
| 可观测/持续验证 | 生产 spans、版本、事件和状态 | 异常规则、离线重放、人工升级 | 检测率、定位时间、回归命中 | 工程需求强，标准化早期 | 生产 Agent 平台 |

成熟度不能理解为论文数量排序。可控环境与状态 Oracle 的概念最稳定，但维护成本高；安全 benchmark 较多，却仍受攻击适应性和效用权衡影响；诊断与可观测性论文增长很快，但生产公开 trace、因果真值和隐私协议仍稀缺。

## 6. 不同 Agent 类型如何映射到方法谱系

| Agent 类型 | 最关键的测试组合 | 代表论文 | 特有难点 |
|---|---|---|---|
| Web/浏览器 | 自托管环境 + 页面/后台状态 + 轨迹 Judge 元测试 + 版本回归 | WebArena、BrowserGym、AgentRewardBench | 网站漂移、视觉/A11Y 不一致、登录与地区状态 |
| 代码/修复 | 仓库沙箱 + fail-to-pass/pass-to-pass + 中途验证证据重放 | SWE-bench、BSG-VA | 测试是否真正覆盖缺陷、环境构建、补丁过拟合 |
| 工具调用 | 有状态工具 + 权限/副作用 + milestone/minefield + 故障注入 | ToolSandbox、τ-bench、AgentDojo、ToolEmu | schema 漂移、部分成功、重复写、模拟用户误差 |
| 记忆/长时程 | 写入-更新-检索-使用分阶段测试 + 跨会话状态与遗忘 | LongMemEval、MemoryAgentBench、Mem2ActBench | 过期信息、身份混淆、污染累积、从记忆到动作的落差 |
| 多智能体 | 消息/角色 provenance + 语义注错 + 传播/恢复 + Agent/step 归因 | MultiAgentBench、MAS-FIRE、OrchestraBench、VerifyMAS | 共享状态、错误委派、协同根因和级联传播 |

Web、代码和工具 Agent 已有较强的可执行 Oracle；长期记忆和多智能体评价正在从“最终答对多少”转向分阶段状态和传播分析。具身 Agent 还需要在上述框架上增加物理安全、动作可逆性和 sim-to-real 复现，本文不另建一套重复分类。

## 7. 从单项方法到完整 Agent QA 生命周期

八个方向并不是互相替代的 benchmark 菜单，而是同一质量保障生命周期上的不同环节。把它们组合起来，可以得到一条更接近软件工程测试、同时适应 Agent 概率性和开放环境的流水线：

```text
需求/策略/权限
  -> 组件契约与确定性单元测试
  -> 场景、扰动和攻击生成
  -> 可重置环境中的闭环执行
  -> 重复、故障注入和安全红队
  -> 终态 + 轨迹 + Judge 的复合判定
  -> 失败聚类、归因和干预重放
  -> 线上监控 -> 脱敏事故回流为回归测试
```

### 7.1 测试设计：先定义可判定的目标，而不是先选模型

一个场景在执行前就应固定目标、身份、权限、初态、工具 schema、预算、必要里程碑、禁止事件、预期变化和允许变化。PDoctor 说明约束可以从生成测试的同一结构导出；AppWorld、ToolSandbox 和 AgentDojo 则说明状态、里程碑和攻击目标必须在环境侧可检查（Ji 等, 2024；Trivedi 等, 2024；J. Lu 等, 2025；Debenedetti 等, 2024）。如果这些条件没有预先定义，运行结束后再让 Judge 阅读轨迹，往往只是把模糊需求转移给另一个模型。

Tangent 对工程实践的观察也表明，传统 mock 和单元断言仍然有价值，问题在于它们主要覆盖确定性边界，较少进入多步交互、外部状态和非功能需求（Pan 等, 2026）。因此合理的测试金字塔不是放弃单元测试，而是在工具契约、幂等、超时和错误语义之上，逐层增加模型-工具闭环、可重置系统场景和受控生产式压力。

### 7.2 执行与判定：把环境、Agent 和评测器分开记账

一次运行至少要区分三类结果：被测 Agent 是否完成任务，测试环境/模拟器是否按规格运行，评测器是否有足够证据作出判断。环境初始化失败不能记为 Agent 失败，Judge 无法看到关键状态也不能强制给出成功/失败。AgentRewardBench 和 Seeing the Whole Elephant 分别说明 evaluator 误差与 trace 可见度会系统性改变测量结果（Lù 等, 2025；Chen 等, 2026b）。

建议将一次运行保存为最小的版本化记录：

```text
RunRecord = {
  testcase_version, agent_harness_model_version, evaluator_version,
  initial_state_hash, final_state_diff,
  observation_action_tool_events, memory_and_handoff_events,
  injected_faults_and_trigger_evidence,
  oracle_evidence, success_and_violation_labels,
  tokens_cost_latency, seed, termination_reason
}
```

其中 `trigger_evidence` 很关键：AgentChaos 表明，只有确认故障实际到达目标调用，故障运行才有资格进入鲁棒性统计（Tan 等, 2026）。同样，安全测试要确认攻击目标或禁止副作用是否真实发生，不能只根据 Agent 输出的文字语气判定。

### 7.3 回归与发布：从单点分数转向统计门禁

对每次 prompt、模型、planner、memory、工具 schema 或权限策略升级，应在同一环境快照上做配对 A/B。每次提交运行确定性契约测试；每个构建运行固定系统回归集；每日或每周对高价值任务做重复、释义和工具故障测试；候选发布再运行高成本 Web/VM、安全与混沌套件。门禁不应只使用平均成功率，而应同时包含成功率置信下界、`pass^k`、高危副作用、误拒、攻击成功、每成功任务成本和尾延迟（Yao 等, 2025；Kapoor 等, 2025）。

生产阶段则需要把失败 trace 在脱敏、权限和预算控制下聚类，人工确认后固化为可重放案例。重放涉及付款、发信、删除或外部写入时，必须使用沙箱、幂等键、补偿动作或人工批准；自动重跑本身也是一个可能制造副作用的 Agent 行为。

### 7.4 当前成熟度判断

- **已形成基础设施范式：** 可控环境、状态差分、执行测试和任务特定 evaluator，已经能支撑 Web、代码和工具 Agent 的系统验收。
- **正在形成评价规范：** 轨迹 Oracle、Judge 元评测、重复可靠性、成本与统计报告已出现明确共识，但尚缺跨 benchmark 统一协议。
- **处于方法创新期：** 自动用例生成、灰盒覆盖、语义故障注入、多 Agent 归因和反事实重放在 2026 年集中出现，证据多来自少量系统或预印本。
- **尚未形成生产科学：** 公开 incident、真实故障分布、跨组织 trace schema、长期漂移和隐私-可诊断性实验仍很少，这是学术方法走向部署保障的主要断点。

## 8. 研究共识、主要争议与优先空白

### 8.1 已形成的共识

1. **最终任务成功率必要但不充分。** 状态、副作用、轨迹、权限、成本和安全需要独立检查。
2. **一次成功不能代表生产可靠。** 关键任务应重复运行并做语义等价、工具 schema、环境和版本扰动。
3. **Evaluator 也是被测系统。** 规则、Judge、模拟用户和模拟工具都有自己的精度、召回、漂移和攻击面。
4. **安全与效用必须联合报告。** 完全拒绝或完全不会使用工具，不是可部署的安全方案。
5. **分数属于完整系统配置。** 模型、prompt、planner、memory、harness、工具、环境和 evaluator 共同决定结果。

### 8.2 尚未解决的争议

- **真实性与可复现性：** 真实 Web/API 有外部效度却持续漂移，模拟器稳定却可能漏掉关键故障。
- **确定规则与开放语义：** 状态断言可审计但覆盖不全，Judge 灵活但不稳定且可能相信自述。
- **多路径正确性与回归可比性：** 固定轨迹过严，只看终态又会漏掉过程违规。
- **完整 trace 与隐私：** 更多上下文提高归因上限，同时增加泄密、合规和存储风险。
- **诊断相关性与因果性：** 轨迹解释和 outcome flip 提供证据，但仍不足以证明唯一根因。

### 8.3 优先研究空白

1. **Agent 专属覆盖标准。** 需要联合表示工具/参数、状态转移、轨迹分支、权限边界、风险规则、记忆生命周期和多 Agent 消息，而不是照搬代码覆盖。
2. **可移植复合 Oracle。** 状态差分、DAG、过程规则和 Judge 多与单一 benchmark 绑定，缺少跨 Web、代码和企业工作流的统一表达与不确定性传播机制。
3. **统计可靠性协议。** 领域尚无统一的重复次数、置信区间、配对检验、flakiness 预算和版本发布门限。
4. **生产校准的故障模型。** 现有故障多由研究者人工设计，需要从真实 incident/telemetry 学习频率、相关性、严重度和级联结构。
5. **多根因与反事实真值。** 数据集应表达错误源、首次决定性步骤、症状、恢复点、多个充分原因及证据不足，而不是只给一个责任标签。
6. **长期状态与记忆演化测试。** 跨 session、跨用户的更新、遗忘、权限变化、污染累积和延迟触发仍远少于短会话 benchmark。
7. **跨框架 trace 语义。** 需要稳定的 observation、action、tool、memory、handoff、evaluation、guardrail 和 side-effect schema，并测试埋点丢失、乱序和篡改。
8. **隐私-可诊断性曲线。** 应量化删除、摘要或脱敏哪些字段会造成多大检测和归因损失，而不是默认保存全部推理与数据。

Tangent 提供了一个重要现实校验：其开源样本中 61.8% 的测试集中于单个 Agent 或工具，只有 7.5% 涉及非功能需求，推理相关断言仅占 8.7%；产业访谈则更重视安全、性能、可靠性、韧性和持续评价（Pan 等, 2026）。这意味着近期最有价值的研究，不只是再造一个榜单，而是把上述方法变成开发者能在 CI、预发布和生产事故处理中真正使用的测试基础设施。

## 9. 建议的分层阅读路线

**第一层：建立测试心智模型。** 先读 AppWorld、ToolSandbox、AgentDojo、AgentBoard、τ-bench和 AI Agents That Matter，理解状态差分、轨迹 DAG、安全-效用联合指标、局部进度与重复可靠性。

**第二层：理解 Oracle 和自动生成。** 再读 AgentRewardBench、Process Evaluation、AJ-Bench、PDoctor、ATA 和 SIRAJ，重点观察 evaluator 为什么会错、如何把约束或环境证据变成可执行判定。

**第三层：进入可靠性和安全测试。** 阅读 ToolEmu、InjecAgent、AgentDoS、AgentChaos、MAS-FIRE 和 OrchestraBench，比较模拟、红队、灰盒反馈、API 注错和语义注错的差异。

**第四层：连接诊断与生产闭环。** 阅读 VerifyMAS、StepFinder、REFLECT、Seeing the Whole Elephant、AgentDebugX 和 Agentic CLEAR，关注 trace 可见度、归因标签、重放证据和恢复门控。

研究组若要选择后续课题，优先建议三条主线：可移植复合 Oracle、生产故障校准的可靠性/混沌测试、隐私保护且可重放的跨框架 trace。灰盒覆盖和多根因归因创新空间较大，但 ground truth 和实验基础设施成本也最高。

总体来看，Agent 测试正在从“用一个 benchmark 给模型打分”转向“对一个概率化软件系统建立可审计证据”。研究重心也相应从任务数量和平均成功率，迁移到测试是否覆盖关键行为、Oracle 是否可信、故障是否真实触发、失败能否被复现和定位，以及修复后是否在效用、安全、成本和延迟上同时改善。短期内不会出现一个适用于所有 Agent 的万能指标；更现实的方向是建立可组合协议：确定性状态检查负责能程序化判断的事实，轨迹规则负责过程与权限，经过校准的 Judge 处理剩余开放语义，重复和注错提供可靠性证据，生产 telemetry 则把未知失败带回回归集。谁能把这些证据跨框架、低成本且隐私安全地连接起来，谁就更接近下一阶段真正可部署的 Agent assurance。

换言之，下一阶段的核心竞争不只是提高 Agent 的任务能力，而是建立一条能持续发现未知失败、保留判定依据、控制重放风险，并在系统升级后重新证明质量没有退化的证据链。

## 10. 代表文献与核验状态

下列条目覆盖正文实际引用的主要工作；完整作者、纳排原因和证据字段见项目证据表。

### 10.1 综述、实证与基础环境

- Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024 Oral. arXiv:2310.06770。正式版本；全文。
- Mohammadi, M., et al. (2025). *Evaluation and Benchmarking of LLM Agents: A Survey.* KDD 2025. DOI: `10.1145/3711896.3736570`。正式版本；全文。
- Pan, R., et al. (2026). *Tangent: An Empirical Study of Testing Practices for LLM-Based Agent Applications.* ASE 2026 接收稿. arXiv:2608.08413；论文印载 DOI `10.1145/3832783.3837414`，Crossref/OpenAlex 待入库。全文。
- Yehudai, A., et al. (2026a). *A Survey on Evaluation of LLM-based Agents.* Findings of ACL 2026. DOI: `10.18653/v1/2026.findings-acl.1330`。正式版本；全文。
- Zhou, S., et al. (2024). *WebArena: A Realistic Web Environment for Building Autonomous Agents.* ICLR 2024. arXiv:2307.13854。正式版本；全文。
- Zhu, J., et al. (2026a). *Evolutionary Perspectives on the Evaluation of LLM-Based AI Agents: A Comprehensive Survey.* Frontiers of Computer Science. DOI: `10.1007/s11704-026-51590-2`。正式版本；全文。

### 10.2 用例、环境与 Oracle

- Debenedetti, E., et al. (2024). *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* NeurIPS 2024 Datasets and Benchmarks. DOI: `10.52202/079017-2636`。正式版本；全文。
- Gritta, M., et al. (2026). *Process Evaluation for Agentic Systems.* Findings of EACL 2026. DOI: `10.18653/v1/2026.findings-eacl.140`。正式版本；全文。
- Ji, Z., et al. (2024). *Testing and Understanding Erroneous Planning in LLM Agents through Synthesized User Inputs.* arXiv:2404.17833。预印本；全文。
- Komoravolu, S., & Mrini, K. (2026). *Agent-Testing Agent.* EACL 2026. DOI: `10.18653/v1/2026.eacl-long.339`。正式版本；全文。
- Lu, J., et al. (2025). *ToolSandbox.* Findings of NAACL 2025. DOI: `10.18653/v1/2025.findings-naacl.65`。正式版本；全文。
- Lù, X. H., et al. (2025). *AgentRewardBench.* COLM 2025. arXiv:2504.08942。正式版本；全文。
- Ma, C., et al. (2024). *AgentBoard.* NeurIPS 2024 Datasets and Benchmarks. arXiv:2401.13178。正式版本；全文。
- Shi, W., et al. (2026). *AJ-Bench.* Findings of ACL 2026. DOI: `10.18653/v1/2026.findings-acl.1269`。正式版本；全文。
- Trivedi, H., et al. (2024). *AppWorld.* ACL 2024. DOI: `10.18653/v1/2024.acl-long.850`。正式版本；全文。
- Wang, J., et al. (2026). *Aligning Agents via Planning: A Benchmark for Trajectory-Level Reward Modeling.* ACL 2026. DOI: `10.18653/v1/2026.acl-long.1062`。正式版本；全文。
- Xu, X., & Wu, W. (2026). *Validation Evidence in LLM Repair Agents.* arXiv:2607.28871。预印本；全文。
- Zhou, K., et al. (2026). *SIRAJ.* Findings of EACL 2026. DOI: `10.18653/v1/2026.findings-eacl.171`。正式版本；全文。

### 10.3 可靠性、安全与故障注入

- Gupta, A. (2026). *ReliabilityBench.* arXiv:2601.06112。预印本；全文。
- Hui, M., et al. (2026). *FLARE.* arXiv:2604.05289。预印本；仅摘要。
- Jia, J., et al. (2026). *MAS-FIRE.* arXiv:2602.19843。预印本；全文。
- Kapoor, S., et al. (2025). *AI Agents That Matter.* TMLR 2025. arXiv:2407.01502。正式版本；全文。
- Khanal, A., et al. (2026). *Beyond pass@1.* arXiv:2603.29231。预印本；全文。
- Li, Z., et al. (2026). *Les Dissonances.* NDSS 2026. DOI: `10.14722/ndss.2026.240577`。正式版本；全文。
- Luo, J., et al. (2026). *Autonomy Comes with Costs: Detecting Denial-of-Service Vulnerabilities Caused by Resource Abusing in LLM-based Agents.* USENIX Security 2026。正式会议页面：<https://www.usenix.org/conference/usenixsecurity26/presentation/luo>；全文。
- Ruan, Y., et al. (2024). *Identifying the Risks of LM Agents with an LM-Emulated Sandbox*（ToolEmu）. ICLR 2024. arXiv:2309.15817。正式版本；全文。
- Tan, G., et al. (2026). *AgentChaos.* ASE 2026 接收稿. DOI: `10.1145/3832783.3837437`; arXiv:2608.06790。论文/OpenAlex 已核验，Crossref 待入库；全文。
- Yao, S., et al. (2025). *τ-bench.* ICLR 2025. arXiv:2406.12045。正式版本；全文。
- Zhan, Q., et al. (2024). *InjecAgent.* Findings of ACL 2024. DOI: `10.18653/v1/2024.findings-acl.624`。正式版本；全文。
- Zhang, Y., et al. (2026). *VeriGrey.* arXiv:2603.17639。预印本；仅摘要。
- Chen, Y., et al. (2026a). *OrchestraBench.* arXiv:2608.05263。预印本；全文。

### 10.4 诊断、可观测与应用补充

- Balusu, K. C. (2026). *AgentTelemetry.* AIware 2026. DOI: `10.1145/3805760.3814931`。正式元数据；仅摘要。
- Chen, M., et al. (2026b). *Seeing the Whole Elephant.* ACL 2026. DOI: `10.18653/v1/2026.acl-long.912`。正式版本；全文。
- Dong, L., et al. (2024). *AgentOps: Enabling Observability of LLM Agents.* arXiv:2411.05285。预印本；全文。
- Hu, Y., et al. (2026). *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions.* ICLR 2026. arXiv:2507.05257。正式版本；全文。
- Le Sellier de Chezelles, T., et al. (2025). *The BrowserGym Ecosystem for Web Agent Research.* TMLR 2025. arXiv:2412.05467。正式版本；全文。
- Lin, X., et al. (2026). *REFLECT.* ICML 2026 FAGEN Workshop；arXiv:2606.09071。Workshop 接收稿；全文。
- Ou, T., et al. (2025). *AgentDiagnose.* EMNLP 2025 System Demonstrations. DOI: `10.18653/v1/2025.emnlp-demos.15`。正式版本；全文。
- Qiao, H., et al. (2026). *VerifyMAS.* arXiv:2605.17467。预印本；全文。
- Shah, J. (2026). *Causal Agent Replay.* arXiv:2606.08275。预印本；仅摘要。
- Shen, Y., et al. (2026). *Mem2ActBench.* ACL 2026. DOI: `10.18653/v1/2026.acl-long.370`。正式版本；全文。
- Wu, D., et al. (2025). *LongMemEval.* ICLR 2025. arXiv:2410.10813。正式版本；全文。
- Yehudai, A., et al. (2026b). *Agentic CLEAR.* ACL 2026 System Demonstrations. DOI: `10.18653/v1/2026.acl-demo.74`。正式版本；全文。
- Zhu, K., et al. (2025). *MultiAgentBench.* ACL 2025. DOI: `10.18653/v1/2025.acl-long.421`。正式版本；全文。
- Zhu, T., et al. (2026b). *StepFinder.* KDD 2026. DOI: `10.1145/3770855.3817991`。正式版本；全文。
- Zhu, K., et al. (2026c). *AgentDebugX.* arXiv:2607.18754。预印本/开源工具；全文。

## 11. 证据限制

- 2026 年预印本密集，学术数据库和 DOI 注册存在滞后；“方法值得跟踪”不等于“已被独立复现”。
- 许多实验依赖闭源模型、网站、API 和当时的 Agent harness，论文数值是特定版本快照。
- 完整全文并不自动意味着强证据；小样本、合成环境、单一模型家族和作者设计故障仍限制外部效度。
- 本地证据库的全文标记表示已经阅读论文方法与实验，不表示已复现实验代码。
- 本文优先总结共同方法和边界，避免把不同任务、环境、Oracle 和成本条件下的分数做不成立的横向排名。
