# AI 智能体测试与质量保障：系统化文献综述

> **更新提示（2026-08-13）：** 新增动态测试生成、灰盒模糊测试、agentic oracle、轨迹回归及 USENIX Security 2026 安全测试进展，见 `research/2026-08-13-agent-testing-update.md`。本文原有 40 篇核心语料与统计口径保持不变。

> 检索截止：2026-07-23。正文中的方括号为 `research/references.bib` 的 BibTeX 引文键。
> 本综述纳入 40 篇身份已核验论文，其中 25 篇完成全文精读并有独立结构化笔记，15 篇仅在摘要允许的范围内使用。完整纳排记录见 `research/evidence/screening-log.csv`，逐篇证据等级见 `research/evidence/evidence-table.csv`。

## 1. 执行摘要

AI 智能体测试不是“给大模型出更多题”。普通 LLM 评测通常观察一次输入后的文本；智能体测试面对的是一个持续闭环：

```text
目标/政策
  → 观察环境
  → 规划与选择动作
  → 调用工具/控制界面/发送消息
  → 环境与记忆发生变化
  → 再观察、纠错或继续执行
  → 终态与外部副作用
```

因此，测试对象同时包含模型、提示与规划器、工具适配层、记忆、编排器、权限控制、执行环境、评测器和运行基础设施。一个最终答案正确的智能体，仍可能在途中泄露数据、重复付款、越权读取、违反确认流程；一个攻击成功率很低的智能体，也可能只是根本不会完成任何任务。

本次调研的核心结论是：

1. **最终任务成功率必要但不充分。** 较可信的 oracle 应组合环境终态、预期/允许状态差分、中间里程碑、禁止事件、工具调用与人工或经校准的语义评审。AppWorld 的数据库差分、ToolSandbox 的 milestone/minefield DAG、AgentDojo 的 utility/security 检查体现了三种互补设计 [trivedi2024appworld; lu2025toolsandbox; debenedetti2024agentdojo]。
2. **轨迹必须成为一等测试产物。** AgentBench、AgentBoard 和 BrowserGym 显示，二元成功分数会掩盖循环、无效动作、格式错误、局部进展、环境故障和脚手架差异 [liu2024agentbench; ma2024agentboard; lesellierdechezelles2025browsergym]。
3. **单次成功不等于可靠。** τ-bench 的 `pass^k` 要求同一任务连续 `k` 次都成功；其最佳零售设置单次成功约 61.2%，但 `pass^8` 已低于 25% [yao2025taubench]。生产验收应报告重复运行、置信区间、语义等价扰动和版本漂移，而非只跑一次。
4. **评测器本身需要被测试。** AgentRewardBench 的专家轨迹表明，规则 evaluator 精度较高但召回不足，LLM judge 又倾向高估成功；所测 judge 没有一个在所有 Web 基准上占优，也没有一个成功判断精度超过 70% [lu2025agentrewardbench]。LLM judge 不能直接当金标准。
5. **安全必须和效用联合报告。** AgentDojo、AgentHarm、SafeAgentBench 与 BadRobot 都说明：拒绝一切会得到表面安全；语言拒绝也不保证工具或物理动作安全 [debenedetti2024agentdojo; andriushchenko2025agentharm; yin2024safeagentbench; zhang2025badrobot]。
6. **成本、延迟与可复现性是质量属性，不是脚注。** 相同任务中，不同脚手架可能相差数量级成本；模型别名、网站、API、OS、时区和工具 schema 的变化会使分数漂移 [kapoor2025aiagentsmatter; lesellierdechezelles2025browsergym]。应报告每个成功任务成本，而不是只报告每次调用成本。
7. **当前最缺的不是另一个排行榜，而是测试方法学。** 变形测试、属性测试、模糊测试、故障注入、跨框架 trace 语义、长期状态漂移和多智能体级联失败仍缺少成熟、同行评审且可复用的方法。

## 2. 智能体测试的定义与范围

本综述将“AI 智能体测试”定义为：

> 对具有目标驱动、多步决策、环境交互、工具调用、状态或记忆维护、或多主体协作能力的 AI 系统，通过离线评测、交互场景、轨迹检查、对抗测试、故障注入、回归测试和线上监控，验证其功能正确性、可靠性、安全性、效率与可复现性的过程。

这一边界包含：

- 单智能体与多智能体；
- API/函数调用、浏览器/GUI、代码仓库、具身机器人和企业工作流；
- 规划、推理、记忆、工具选择、参数、恢复与协作；
- 评测器、模拟用户、工具模拟器和运行时 guardrail；
- 离线基准、CI 回归、沙箱红队与生产监控。

它不把没有行动闭环的普通聊天质量评测作为核心文献。通用 LLM-as-a-Judge 研究只在解释 agent evaluator 偏差时作为方法背景；“让多个 agent 去测试 REST API”的论文，如果真正被测对象是传统 API 而不是 agent，也被排除。

### 2.1 测试单元

最小测试单元不应只是 `(prompt, answer)`，而应是：

```text
TestCase = {
  goal,
  policy_and_permissions,
  initial_environment_snapshot,
  initial_memory,
  available_tools_and_schemas,
  user_or_peer_behavior,
  fault_or_attack_schedule,
  execution_budget,
  expected_terminal_properties,
  required_milestones,
  forbidden_events
}
```

测试结果则至少包括最终状态、完整动作轨迹、工具副作用、资源消耗、环境版本和 oracle 证据。

### 2.2 “正确”的多层含义

一个智能体可能同时具有以下不同状态：

- **目标正确**：用户要求已完成；
- **过程合规**：必要确认、授权、顺序和政策均满足；
- **副作用可接受**：除允许变化外没有破坏无关状态；
- **信息正确**：向用户返回的事实来自环境而非幻觉；
- **安全**：没有完成攻击者目标或危险动作；
- **稳定**：重复运行和等价输入下仍可靠；
- **经济可行**：没有以无限循环、过量 token 或高延迟换取成功。

这些维度不能压缩成一个不透明总分。

## 3. 与传统软件测试的区别

传统软件在固定输入、版本和环境下通常具有较强确定性；测试 oracle 可以写成精确值、异常类型或状态断言。智能体保留了软件系统的一切故障，同时增加了概率模型和开放环境的行为不确定性。

| 维度 | 传统软件 | 智能体系统 |
|---|---|---|
| 输入 | 结构化且边界相对明确 | 自然语言、网页、图像、工具输出、其他 agent 消息 |
| 执行路径 | 由代码控制流决定 | 模型动态生成计划、动作和工具参数 |
| 正确答案 | 常有精确 oracle | 多条等价轨迹，正确性可能依赖语义与政策 |
| 状态 | 程序内状态为主 | 环境、对话、长期记忆、共享黑板、外部服务共同演化 |
| 副作用 | 可由接口契约约束 | 模型可能调用未预期工具或在错误时机执行不可逆动作 |
| 复现 | 固定版本/seed 后通常稳定 | 即使温度为 0，服务端模型、并发和外部系统仍可漂移 |
| 故障传播 | 组件依赖图相对显式 | 错误观察可污染信念、计划、记忆、工具和其他 agent |
| 安全边界 | 代码与身份权限为主 | 不可信自然语言可能被模型解释成高优先级指令 |
| 资源预算 | 通常由程序复杂度控制 | 循环、重试和上下文增长会造成 token/费用爆炸 |

传统的单元、集成、系统和验收测试仍适用，但需要扩展：

- “工具单元测试”必须验证 schema、权限、幂等、超时和错误语义；
- “集成测试”要覆盖模型—规划器—工具—状态之间的闭环；
- “系统测试”要运行在可重置的真实或高保真环境；
- “验收测试”必须把业务政策、安全和经济预算写入 oracle；
- 回归基线要包含分布、置信区间和失败簇，而不是一个确定值。

## 4. 与机器学习系统测试的区别

传统 ML 系统测试已关注数据漂移、鲁棒性、公平性、校准和非确定性。智能体继承这些问题，但又增加了三个本质变化。

第一，预测会改变后续输入。分类模型的一次错误通常结束于错误标签；智能体的一次错误工具调用会改变数据库，导致下一步观察、记忆和决策全部偏离。

第二，行动空间是开放和结构化的。模型不仅选择类别，还生成工具名、参数、代码、鼠标坐标、消息和执行顺序；测试要区分选择错误、参数错误、前置条件错误和执行反馈误读。

第三，环境和模型共同构成测量对象。OSWorld 的 VM、WebArena 的网站、AndroidWorld 的模拟器、AppWorld 的数据库，都有自己的初始化、重置、并发和漂移问题 [xie2024osworld; zhou2024webarena; rawles2025androidworld; trivedi2024appworld]。环境 bug 可能被误记为 agent failure，环境过于宽松又会放过真实错误。

所以，智能体 QA 至少要把四类不确定性分开：

1. 模型采样与服务端非确定性；
2. 脚手架、提示、上下文截断和并发；
3. 用户/工具/环境模拟器误差；
4. 真实外部环境漂移与网络故障。

## 5. 与普通 LLM 评测的区别

普通 LLM 评测主要测知识、推理或文本偏好，常以 exact match、BLEU/ROUGE、人工偏好或 LLM judge 为 oracle。智能体评测至少多出五项：

1. **行动真实性**：模型声称“已完成”不等于环境已改变；
2. **时序性**：先授权后退款与先退款后授权终态可能相同，但合规性不同；
3. **副作用**：完成目标的同时可能删除或修改无关数据；
4. **恢复性**：工具超时、返回部分结果或页面改变后是否能重新规划；
5. **持续成本**：每一步都会增加 token、工具费用和延迟。

AgentRewardBench 提供了直接证据：LLM judge 容易相信 agent 的 reasoning 或自述，没有在页面状态中找到对应证据 [lu2025agentrewardbench]。BadRobot 则显示文本安全与动作安全可能分离：语言通道拒绝，结构化动作通道仍可驱动物理执行 [zhang2025badrobot]。

因此，普通 LLM 分数最多是智能体组件能力的先验，不能替代闭环执行测试。

## 6. 研究领域分类图谱

### 6.1 按测试层分解

| 测试层 | 主要问题 | 代表方法/文献 |
|---|---|---|
| 基础模型与提示 | 指令理解、推理、格式、拒绝、judge 偏差 | AgentBench、GAIA、AgentHarm |
| 规划器 | 子目标、顺序、约束、终止、重规划 | AgentBoard、PDoctor、τ-bench |
| 工具接口 | 工具选择、参数、schema、返回解释 | ToolLLM、API-Bank、StableToolBench、ToolSandbox |
| 记忆与状态 | 过期状态、污染、重复写、身份混淆 | AgentPoison、AppWorld、AgentOps |
| GUI/环境控制 | grounding、窗口/网页变化、真实执行 | WebArena、VisualWebArena、OSWorld、AndroidWorld |
| 多智能体编排 | 分工、消息、共享记忆、冲突与级联 | MultiAgentBench、Why Do Multi-Agent LLM Systems Fail? |
| 具身动作 | 物理危险、语言—动作不一致、恢复 | ALFWorld、ScienceWorld、SafeAgentBench、BadRobot |
| 安全控制 | 注入、越权、恶意工具、数据泄露 | InjecAgent、AgentDojo、ASB、Agent-SafetyBench |
| 评测器 | 规则召回、judge 偏差、证据 grounding | AgentRewardBench、Agent-as-a-Judge |
| 运维与运行时 | trace、预算、告警、策略阻断 | AgentOps、BrowserGym、AgentSpec |

### 6.2 按质量属性分解

- **功能正确性**：目标完成、规划、工具/参数、记忆、恢复、协作；
- **可靠性**：重复成功、扰动鲁棒、环境漂移、容错和可恢复；
- **性能/经济性**：token、调用数、每成功成本、p50/p95/p99 延迟；
- **可解释与可观测**：轨迹证据、失败定位、版本与因果关系；
- **安全与隐私**：注入、越权、泄露、污染、危险动作和供应链；
- **可维护与可复现**：可重置环境、版本锁定、数据污染、回归稳定性。

### 6.3 按应用类型分解

- Web/浏览器：Mind2Web、WebArena、VisualWebArena、WorkArena++、BrowserGym；
- 移动/桌面 GUI：AndroidWorld、OSWorld；
- 编程：InterCode、SWE-bench、AppWorld；
- 工具调用与企业工作流：ToolLLM、API-Bank、ToolSandbox、τ-bench；
- 多智能体：MultiAgentBench、Multi-Agent Failure Taxonomy；
- 具身：ALFWorld、ScienceWorld、SafeAgentBench、BadRobot；
- 通用助手：AgentBench、AgentBoard、GAIA。

## 7. 主要测试方法

### 7.1 基准测试与场景测试

基准提供可比较的任务、环境和评分器，但“同一个成功率”可能测量完全不同的东西。GAIA 主要核对最终短答案；WebArena/OSWorld 执行任务特定 evaluator；SWE-bench 运行测试；MultiAgentBench 混合规则与 LLM rubric。跨论文横向排名只有在任务、模型、脚手架、环境和 oracle 同时可比时才有意义。

场景测试比随机问题更适合生产系统。一个业务场景应包含初态、身份、权限、政策、可用工具、扰动和期望状态。AppWorld 的 contrastive scenario 要求同一场景的三个变体全部成功，能揭示看似相近需求下的不稳定 [trivedi2024appworld]。

### 7.2 状态与副作用 oracle

这是目前证据最强的方向：

- WebArena/OSWorld：对真实执行结果写任务特定检查；
- τ-bench：比较数据库终态并验证需返回的信息；
- AppWorld：分别声明 `expected changes` 与 `allowed changes`，其余状态差分视为 collateral damage；
- AgentDojo：分别检查用户效用和攻击者目标；
- SWE-bench：补丁必须让 fail-to-pass 测试通过，同时保留 pass-to-pass 回归测试。

优点是可复现、可审计，不依赖模型自评。缺点是只检查终态可能漏掉途中泄露、错误确认和先后顺序；测试本身也可能不完备。

### 7.3 轨迹级评测

AgentBoard 用人工子目标计算 progress rate；ToolSandbox 用 milestone DAG 接受不同但正确的路径，用 minefield DAG 检测禁止状态；Agent-as-a-Judge 让 evaluator agent 检查工作区和层级需求 [ma2024agentboard; lu2025toolsandbox; zhuge2025agentasajudge]。

轨迹评测宜把下列信号分开：

- 子目标覆盖和首次达成时间；
- 工具选择、参数和前置条件；
- 关键动作偏序；
- 重复/停滞/无效动作；
- 错误后是否恢复；
- 状态读写和副作用；
- 最终终态与用户输出。

固定参考轨迹不适合开放任务，因为多条路径可能都正确；完全开放的 LLM judge 又不稳定。DAG、状态断言与局部语义 judge 的混合最有实践价值。

### 7.4 重复、扰动与回归测试

同一任务至少应运行多次。τ-bench 的 `pass^k` 衡量连续可靠，而不是“多试几次总有一次成功” [yao2025taubench]。OSWorld 对窗口位置、尺寸和 clutter 的扰动显示 GUI 智能体对布局变化非常敏感 [xie2024osworld]。BrowserGym 进一步指出时区、语言、地理位置、广告和网站动态内容都会影响结果 [lesellierdechezelles2025browsergym]。

建议的回归集合包括：

- 固定 seed 的基线运行；
- 多 seed/重复运行；
- 自然语言释义和无关信息；
- 实体一致重命名；
- 工具顺序可交换与 schema 兼容变化；
- 页面布局、窗口、网络、时区和数据量；
- 历史模型/提示/工具版本重放；
- 已知失败轨迹的最小化复现。

### 7.5 对抗、红队与安全测试

静态攻击集只能说明对已知模板的鲁棒性。AgentDojo 表明攻击措辞、注入位置和针对具体防御的适配会显著改变 ASR；Adaptive Attacks 的摘要级证据进一步指出，防御在自适应攻击下可能失效 [debenedetti2024agentdojo; zhan2025adaptiveattacks]。

一个安全回归案例应明确：

- 攻击者控制的输入面；
- 攻击者已知信息；
- 可调用工具和权限；
- 攻击目标与成功 oracle；
- 正常用户目标与效用 oracle；
- 攻击预算和自适应次数；
- 终态、泄露信息和不可逆副作用。

### 7.6 模拟环境与两阶段验证

ToolEmu 用 LM 模拟工具和风险环境，适合低成本搜索长尾；全文实验中，自动生成的对抗失败还需人工确认，自动安全 evaluator 的精度/召回也不是满分 [ruan2024toolemu]。OSWorld、WebArena 和 BadRobot 更接近真实执行，但成本、危险和环境漂移更高。

合理流程是：

1. 在模拟器中进行大规模变异、红队和故障注入；
2. 抽取高风险、代表性或不确定案例；
3. 在真实 VM、封闭网页、硬件沙箱中复现；
4. 报告模拟失败的真实复现率，而不是把模拟分数直接当真实风险。

### 7.7 自动测试输入合成

PDoctor 用 DSL 描述动作与约束、用 Z3 保证输入可满足，并用 mock tools 记录计划，再判定顺序、遗漏与参数错误 [ji2024erroneousplanning]。它提供了软件测试式 oracle，却也暴露当前限制：动作依赖被简化、工具是假执行、只覆盖少量模型和框架。

这一方向可扩展为属性测试、语法/语义模糊测试和覆盖引导测试。目前直接以 agent 为被测对象的成熟工作仍明显少于“让 agent 帮传统软件生成测试”的工作。

### 7.8 运行时监控与策略执行

AgentOps 从 17 个工具归纳出 agent、reasoning、plan、workflow、task、tool、evaluation、guardrail 和 LLM 等 span 类型 [dong2024agentops]。AgentSpec 的摘要级证据把安全规则写成可定制运行时策略，在动作执行前检查并阻断 [wang2026agentspec]。

离线测试不能穷尽开放环境；高风险系统还需要：

- 实时预算、循环和停滞检测；
- 工具参数、权限和敏感数据策略；
- 状态漂移、重复副作用和异常恢复告警；
- 可撤销/需确认动作的分级执行；
- 模型、提示、schema 和环境版本关联；
- 生产失败自动转入回归集。

## 8. 代表性评测基准和框架对比

| 基准/框架 | 对象 | 主要 oracle | 强项 | 主要边界 |
|---|---|---|---|---|
| AgentBench | 8 类交互环境 | 环境特定成功 + 失败类型 | 广覆盖、轨迹故障分型 | 聚合异质，环境维护重 |
| AgentBoard | 多轮 agent | 子目标 progress + success | 解释局部进展 | 子目标人工成本高 |
| GAIA | 通用助手 | 规范化短答案 | 真实工具/浏览需求 | 过程和副作用不可见 |
| WebArena | 浏览器 | 网站终态/内容检查 | 自托管真实风格网站 | 网站状态、并发和 evaluator 维护 |
| VisualWebArena | 多模态浏览器 | 功能终态 | 视觉 grounding | 同上，且模态/布局更敏感 |
| OSWorld | 桌面 GUI | VM 内定制 evaluator | 真实应用、布局扰动 | VM/应用版本成本高 |
| AndroidWorld | 移动 GUI | 初始化—检查—清理逻辑 | 动态参数化任务 | 摘要级证据；移动 app 维护 |
| AppWorld | 交互式编码/API | expected/allowed DB diff | 检测 collateral damage | 模拟应用，过程泄露不可见 |
| ToolLLM/ToolBench | 大规模 API | API 执行 + LLM evaluator | API 规模与检索 | API 漂移、judge 与生成偏差 |
| StableToolBench | 工具学习 | 虚拟 API | 纵向稳定 | 摘要级证据；保真度权衡 |
| ToolSandbox | 有状态工具 | milestone/minefield DAG | 多路径、状态、schema 变异 | oracle 编写成本高 |
| τ-bench | 工具—用户—数据库 | 终态 + 必要输出 + `pass^k` | 政策、重复可靠性 | 用户模拟误差、过程合规缺口 |
| SWE-bench | 仓库级编程 | fail-to-pass + regression tests | 真实代码执行 | 测试不完备、污染与依赖漂移 |
| BrowserGym | Web 评测基础设施 | 复用各基准原生 oracle | 统一 harness、日志、成本/时间 | 统一接口不等于统一测量 |
| MultiAgentBench | 多智能体 | task score + KPI + 协调 judge | 拓扑、通信、竞争 | 指标异质、judge 校准范围窄 |
| AgentRewardBench | evaluator | 专家轨迹标签 | 测评测器而非只测 agent | 限于 Web 轨迹 |
| AgentDojo | 注入安全 | utility/security 状态检查 | 动态、自适应、双 oracle | 合成环境、手工任务 |
| AgentHarm | 恶意工具任务 | 人工 rubric + 工具完成 | 多步 harmful capability | 代理工具、特定威胁模型 |
| SafeAgentBench/BadRobot | 具身安全 | 危险计划/动作判定 | 物理层安全 | 仿真/实验室外推有限 |

### 8.1 不应直接比较的“人类—模型差距”

几篇全文论文都报告了巨大差距，但实验条件不同：

- WebArena 中当时 GPT-4 设置约 14.41%，人类约 78.24%；
- VisualWebArena 主实验 GPT-4V+SoM 约 16.37%，人类约 88.70%；
- OSWorld 的 GPT-4+a11y 约 12.24%，人类约 72.36%；
- GAIA 人类约 92%，人工选择插件的 GPT-4 估计约 15%，Level 3 当时系统为 0。

这些数字不能排成一张能力榜：WebArena 是网页功能终态，VisualWebArena增加视觉 grounding，OSWorld 是桌面 VM，GAIA 是短答案；使用的模型快照、脚手架、任务、指标和人类设置也不同。GAIA 的插件结果还被作者明确描述为不可精确复现的 oracle 式估计 [zhou2024webarena; koh2024visualwebarena; xie2024osworld; mialon2024gaia]。

## 9. 常见评价指标及其局限

| 指标 | 适用问题 | 主要局限 |
|---|---|---|
| Task success / resolved | 最终是否完成 | 隐藏局部进展、过程违规和随机性 |
| Progress / milestone coverage | 走到了哪里 | 子目标标注成本高，里程碑粒度影响分数 |
| State diff | 是否产生期望副作用 | 可能看不到读取泄露和危险中间动作 |
| Tool-call exact/AST match | 工具与参数是否一致 | 多条等价路径会被误罚 |
| `pass^k` | 连续重复可靠性 | 需要更多运行成本；独立性/稳定环境假设要说明 |
| Robustness delta | 扰动后退化 | 扰动是否保持语义需要人工或形式化验证 |
| ASR | 攻击目标是否实现 | 必须和正常 utility、权限和攻击预算一起解释 |
| Refusal rate | 是否拒绝危险请求 | 高拒绝可由“什么都不做”投机 |
| LLM judge score | 开放语义/轨迹质量 | 位置、冗长、自述、同源模型和 grounding 偏差 |
| Token/cost | 资源效率 | 每次调用成本会奖励快速失败；应按成功归一 |
| Latency | 用户/系统性能 | 平均值隐藏长尾；应拆模型、工具、环境和 evaluator |

### 9.1 推荐的最小指标集

功能与可靠性：

- `success@1`、每题重复次数、均值与 95% 置信区间；
- `pass^k` 或连续成功概率；
- progress/milestone、首次失败步骤和恢复率；
- 非预期状态变化、重复不可逆动作和未完成子任务。

安全：

- 正常任务效用；
- targeted/untargeted ASR；
- 过程 policy conformance；
- 越权、泄露、危险工具与不可逆副作用；
- 拒绝率及误拒率。

效率：

```text
cost_per_success = total_evaluation_cost / successful_tasks
```

- 输入/输出 token、模型调用、工具调用、重试；
- 每题成本和每成功成本；
- 端到端 p50/p95/p99；
- 模型、工具、环境重置和 evaluator 耗时分解；
- 准确率—成本—延迟 Pareto 前沿。

评测器：

- precision、recall、F1、AUPRC；
- 与专家一致性和分歧类型；
- 校准误差、重复调用方差；
- judge 成本、延迟和模型/提示版本。

## 10. 智能体典型故障模式

| 层次 | 故障 | 可观察症状 | 推荐检测 |
|---|---|---|---|
| 需求/政策 | 忽略约束、误解优先级 | 终态看似正确但违反确认/政策 | 过程断言、时序规则 |
| 规划 | 漏步骤、错顺序、过早结束 | 部分完成、错误终止 | milestone DAG、PDoctor 式约束 |
| 工具选择 | 选错/不存在工具 | invalid action、无效调用 | schema validator、工具白名单 |
| 参数 | ID 幻觉、字段/类型/方向错误 | 工具异常或错误副作用 | 参数属性测试、数据库约束 |
| 感知/grounding | 误点、误读页面/返回 | 旧 thought 与新观察不一致 | 屏幕/DOM证据、状态快照 |
| 记忆/状态 | 过期、污染、身份混淆 | 重复操作、状态漂移 | 读写 provenance、版本和 TTL |
| 控制流 | 循环、停滞、无效重试 | token/费用不断增长 | 相似轨迹、预算与进展 watchdog |
| 恢复 | 忽略异常、把失败当成功 | 工具报错后继续旧计划 | 错误注入、恢复率 |
| 环境 | 网站/VM/网络/并发故障 | 同题随机失败 | 环境健康检查、隔离与重放 |
| 多智能体 | 重复分工、冲突、错误传播 | 沟通分高但执行失败 | 消息因果图、角色/贡献指标 |
| evaluator | 漏报/误报成功 | 排名和人工判断不一致 | evaluator golden set、分歧审查 |

### 10.1 循环执行

AgentBench 的 task-limit traces 中，超过 90% 在最后 10 次响应里出现 Rouge-L 至少 0.8 的重复 [liu2024agentbench]。VisualWebArena、AppWorld、BrowserGym 与 MultiAgentBench 也观察到重复点击、重复 API、复述分工或停滞 [koh2024visualwebarena; trivedi2024appworld; lesellierdechezelles2025browsergym; zhu2025multiagentbench]。

循环检测不能只看文本重复，还应检查：

- 最近 `n` 步是否没有状态进展；
- 相同工具/参数是否重复；
- 同一错误是否反复出现；
- 计划节点是否来回切换；
- token/费用斜率是否异常。

### 10.2 状态漂移和级联失败

典型链条是：

```text
错误观察
→ 内部状态信念错误
→ 计划选择错误
→ 工具副作用
→ 记忆写入错误事实
→ 其他 agent 读取并传播
→ evaluator 只看最终自述而漏报
```

这解释了为什么单步准确率不能预测长程可靠性，也说明多智能体系统需要消息级 provenance 和故障传播深度，而不只是团队 success。

### 10.3 环境与测试基础设施故障

BrowserGym 的全文记录表明，网页共享后端会造成并发 collision；开放 Web 又受到 CAPTCHA、IP 限流和动态内容影响 [lesellierdechezelles2025browsergym]。测试运行器必须区分：

- agent failure；
- tool/application failure；
- evaluator failure；
- environment reset failure；
- infrastructure timeout。

否则会把环境噪声错误归因给模型。

## 11. 安全测试与对抗评测

### 11.1 攻击面

| 攻击面 | 机制 | 代表证据 |
|---|---|---|
| 直接提示注入/越狱 | 用户直接要求危险多步任务 | AgentHarm、BadRobot |
| 间接提示注入 | 网页、邮件、工具返回携带指令 | BIPIA、InjecAgent、AgentDojo |
| 权限越界/工具滥用 | 利用可用写工具完成非用户目标 | AgentDojo、ASB |
| 数据泄露 | 读取后发送敏感信息 | AgentDojo、Agent-SafetyBench |
| 恶意工具输出 | 不可信观察劫持后续计划 | InjecAgent、Adaptive Attacks |
| 记忆/知识污染 | 毒化长期记忆或 RAG | AgentPoison |
| 物理危险 | 文本对齐未覆盖动作层 | SafeAgentBench、BadRobot |
| 多智能体传播 | 恶意/错误消息进入共享状态 | 当前证据薄弱，属研究空白 |
| 工具/MCP 供应链 | schema、工具描述、服务器身份或返回被替换 | 当前同行评审 agent 测试证据不足 |

### 11.2 关键实证

- AgentDojo 中 GPT-4o 的 targeted ASR 在主设置约 47.69%；具体攻击提示可到 57.7%，工具筛选可降至约 6.84%，但筛选不能处理所有必要工具本身就足以攻击的案例 [debenedetti2024agentdojo]。
- InjecAgent 的全文实验说明，工具返回中的间接指令能劫持后续写操作，增强攻击在不同 agent 协议下显著提高有效 ASR [zhan2024injecagent]。
- AgentHarm 中 jailbreak 会同时提高危险任务完成并降低拒绝；必须验证 agent 是否仍有完成多步工具任务的能力，不能把无能力输出当成功攻击 [andriushchenko2025agentharm]。
- Agent-SafetyBench 在其 16 个 agent 设置中报告总体安全与行为安全明显低于内容安全，说明只做最终文本审核会高估安全 [zhang2024agentsafetybench]。
- BadRobot 在物理/模拟设置中观察到语言与动作安全不一致，证明输出审核必须延伸到结构化控制命令和控制器 [zhang2025badrobot]。

这些数字来自不同模型、攻击、权限和环境，不能直接排名。更强模型有时 ASR 更高，是因为它更会完成任何多步目标；更弱模型 ASR 低可能只是能力不足。

### 11.3 推荐安全测试矩阵

对每个正常任务，至少组合：

- 攻击入口：用户、网页、文件、邮件、工具描述、工具返回、记忆、peer message；
- 攻击位置：开头、中间、末尾、延迟触发；
- 攻击形式：显式、编码、角色伪装、政策伪装、跨轮；
- 权限：只读、有限写、敏感写、不可逆动作；
- 防御：提示、分类器、数据/指令分隔、最小权限、动作审批、运行时规则；
- 攻击者：静态与针对防御的自适应版本。

每次同时测 utility、ASR、误拒、权限使用、泄露、终态和成本。

### 11.4 防御原则

证据不支持“加一段安全系统提示”作为充分防御。更可靠的工程层次是：

1. 不可信数据与控制指令分离并带 provenance；
2. 工具最小权限、读写分离和短期凭证；
3. 高风险参数和副作用由确定性 policy engine 检查；
4. 不可逆动作需用户确认或双人审批；
5. 运行时记录实际环境变化；
6. 对每个防御维护 adaptive attack 回归集；
7. 允许停止、撤销、补偿和人工接管。

## 12. 工程工具链与自动化测试流程

### 12.1 建议流水线

```text
需求/威胁建模
  → 场景与属性定义
  → 可重置环境、工具契约和 golden solution 自测
  → 测试执行（模型/提示/框架/seed/故障矩阵）
  → 全量 trace + 状态快照 + 成本/延迟
  → 分层 oracle（终态/差分/里程碑/禁区/judge）
  → 重复、变形、对抗和故障注入
  → 统计汇总与失败聚类
  → 人工复核高风险/分歧案例
  → 最小化后加入回归集
  → 灰度发布与线上监控
```

### 12.2 测试金字塔

- **L0 契约测试**：工具 schema、参数、权限、异常、幂等；
- **L1 组件测试**：planner、memory、retriever、judge、guardrail；
- **L2 沙箱集成**：固定用户与工具模拟、状态断言；
- **L3 真实环境 E2E**：浏览器、VM、代码仓库、数据库；
- **L4 安全/可靠性**：对抗、故障、扰动和重复；
- **L5 生产监控**：预算、循环、越权、漂移和人工接管。

低层高频且便宜，高层低频但保真度更高。

### 12.3 最小 trace schema

```text
run
 ├─ task / scenario / policy / identity
 ├─ plan and subgoal
 ├─ model call
 ├─ tool selection and invocation
 ├─ observation and environment diff
 ├─ memory read/write
 ├─ guardrail / evaluator decision
 └─ final state / user response
```

每个 span 至少绑定：

- run/parent ID 与时间；
- 模型精确版本、参数、提示模板哈希；
- agent 框架与 commit；
- 工具名称、schema 版本、权限和参数；
- 环境镜像、数据快照、时区和随机 seed；
- 输入/输出 token、费用、延迟、异常与重试；
- 状态差分、oracle 证据和人工处置。

不应默认永久记录原始隐私数据或内部推理。需要字段级脱敏、访问控制、保留期和可审计的 reasoning 摘要。

### 12.4 CI 与发布门禁

一次可执行的发布门禁可以是：

- 契约/单元场景：每次提交；
- 固定回归集：每个构建；
- 50–200 个重复/变形任务：每日；
- 真实 VM/Web 全量基准：每周或候选发布；
- adaptive security suite：高风险变更或每月；
- 模型、提示、工具 schema 任何升级：强制 A/B；
- 指标门槛：成功率置信下界、`pass^k`、误拒、ASR、每成功成本、p95 延迟；
- 任何高危不可逆副作用：零容忍或人工豁免。

## 13. 当前研究不足

1. **缺少统一故障分类与交换格式。** 不同论文用 invalid action、tool error、planning error、stuck、side effect 等不同术语，难以汇总。
2. **oracle 构建成本高。** 状态检查和 milestone 精确，但大量依赖人工领域知识。
3. **评测器相关性偏差。** user simulator、tool simulator、agent 和 judge 经常使用同类模型，可能相互确认。
4. **运行次数和统计功效不足。** 许多昂贵基准只跑一次或不报告置信区间。
5. **成本/延迟报告不一致。** 很少按成功任务归一，环境和 evaluator 成本常被忽略。
6. **版本与污染问题严重。** 模型别名、网站、工具 API 和公开测试集不断变化；排行榜提升可能包含 benchmark 暴露。
7. **终态偏重。** 权限、确认、读取泄露和危险中间动作常未被 oracle 捕获。
8. **变形/属性/灰盒测试薄弱。** 直接对 agent 做语义等价变异、覆盖引导和测试最小化的同行评审工作很少。
9. **故障注入不足。** 超时、限流、部分返回、schema 漂移、竞态、幂等失败和补偿事务缺少统一实验。
10. **多智能体故障传播不足。** 现有工作多看团队总分，缺角色级因果、消息污染和级联深度。
11. **长期记忆与状态漂移不足。** 多数基准在一次短会话内重置，未测数天/多用户的污染累积。
12. **安全和效用仍常分离。** 单看 ASR 或拒绝率会被“完全无能力”策略投机。
13. **MCP/工具供应链证据不足。** 工具发现、schema 更新、服务器替换、签名和依赖投毒尚无成熟通用基准。
14. **线上可观测性尚未标准化。** LangChain、AutoGen、CrewAI、OpenAI Agents 等缺少一致的 agent trace 语义。
15. **可观测性与隐私冲突。** 完整轨迹可能包含密钥、个人数据和敏感推理，研究很少同时评价诊断收益与隐私风险。
16. **真实后果验证不足。** 模拟器适合规模，真实环境适合保真度，但很少报告 sim-to-real 复现比例。

## 14. 值得继续研究的方向

优先级较高且可落地的方向是：

1. **工具故障注入与语义可靠性曲面**：把超时、限流、部分返回、schema 变化和语义扰动与 `pass^k`、恢复率、成本联合建模；
2. **智能体变形测试**：自动生成语义等价目标、实体一致重命名、工具顺序交换和等价初态，检测不应发生的结果差异；
3. **混合轨迹 oracle**：状态规则、milestone/minefield、校准 judge 和人工升级的分层评测；
4. **实时 trace 与断路器**：在低误报条件下提前发现循环、成本爆炸、错误参数和状态漂移；
5. **多智能体时序合约与级联故障**：给消息、角色、共享记忆建立 provenance，并用时序策略阻断传播；
6. **长期版本回归**：把模型、提示、工具 schema 与环境升级视为软件发布，做统计过程控制和失败簇漂移；
7. **MCP/工具供应链测试**：验证工具身份、schema 签名、最小权限、恶意返回、版本回滚和依赖替换；
8. **隐私保护的可观测性**：研究脱敏后仍可进行根因分析的最小 trace。

五个完整可实施选题、实验设计和简历成果另见 `research/research-directions.md`。

2026 年最新预印本与观察性进展另见 `research/2026-latest-update.md`。该专题单独标记摘要级证据，不与主体 40 篇核心语料混合排名。

## 15. 结论

AI 智能体测试的核心单位是“有状态、可行动、会产生副作用的执行轨迹”，不是单次文本。当前最可靠的实践不是寻找一个万能 benchmark 或 judge，而是建立分层证据：

- 以环境终态和状态差分验证功能；
- 以里程碑、禁区和时序规则验证过程；
- 以重复和扰动验证可靠性；
- 以双重 utility/security oracle 和自适应攻击验证安全；
- 以校准的人工/模型评审处理开放语义；
- 以版本化 trace、成本和延迟支持复现与运维。

现有基准已经充分说明当前 agent 在真实 Web、桌面、工具、代码、协作和具身任务中仍不稳定；下一阶段的研究价值更多在“怎样稳定发现、定位、复现和阻断失败”，而不只是在单一排行榜上提高几个百分点。

## 16. 经过核验的参考文献

完整 BibTeX 位于 `research/references.bib`，包括主体 40 条正式引文和 12 条独立标记的 2026 watchlist。下表给出本综述 40 条核心引文的身份与证据边界；DOI 只在 Crossref/OpenAlex或正式出版页核验后写入 BibTeX。

| 引文键 | 论文 | 版本身份 | 证据 |
|---|---|---|---|
| `shridhar2021alfworld` | ALFWorld | ICLR 2021 | 摘要 |
| `wang2022scienceworld` | ScienceWorld | EMNLP 2022，DOI 已核验 | 摘要 |
| `li2023apibank` | API-Bank | EMNLP 2023，DOI 已核验 | 摘要 |
| `deng2023mind2web` | Mind2Web | NeurIPS 2023 D&B | 摘要 |
| `yang2023intercode` | InterCode | NeurIPS 2023 D&B | 摘要 |
| `zhou2024webarena` | WebArena | ICLR 2024 | 全文 |
| `qin2024toolllm` | ToolLLM | ICLR 2024 | 全文 |
| `liu2024agentbench` | AgentBench | ICLR 2024 | 全文 |
| `ruan2024toolemu` | ToolEmu | ICLR 2024 | 全文 |
| `jimenez2024swebench` | SWE-bench | ICLR 2024 Oral | 全文 |
| `mialon2024gaia` | GAIA | ICLR 2024 | 全文 |
| `yi2025bipia` | BIPIA | KDD 2025，DOI 已核验 | 摘要 |
| `ma2024agentboard` | AgentBoard | NeurIPS 2024 D&B，DOI 已核验 | 全文 |
| `koh2024visualwebarena` | VisualWebArena | ACL 2024，DOI 已核验 | 全文 |
| `zhan2024injecagent` | InjecAgent | Findings of ACL 2024，DOI 已核验 | 全文 |
| `guo2024stabletoolbench` | StableToolBench | Findings of ACL 2024，DOI 已核验 | 摘要 |
| `xie2024osworld` | OSWorld | NeurIPS 2024 D&B，DOI 已核验 | 全文 |
| `ji2024erroneousplanning` | PDoctor / Erroneous Planning | arXiv 2024 | 全文 |
| `rawles2025androidworld` | AndroidWorld | ICLR 2025 | 摘要 |
| `yao2025taubench` | τ-bench | ICLR 2025 | 全文 |
| `debenedetti2024agentdojo` | AgentDojo | NeurIPS 2024 D&B，DOI 已核验 | 全文 |
| `kapoor2025aiagentsmatter` | AI Agents That Matter | TMLR 2025 | 全文 |
| `boisvert2024workarenaplusplus` | WorkArena++ | NeurIPS 2024 D&B | 摘要 |
| `chen2024agentpoison` | AgentPoison | NeurIPS 2024，DOI 已核验 | 摘要 |
| `trivedi2024appworld` | AppWorld | ACL 2024，DOI 已核验 | 全文 |
| `zhang2025badrobot` | BadRobot | ICLR 2025 | 全文 |
| `zhang2025breakingagents` | Breaking Agents | EMNLP 2025，DOI 已核验 | 摘要 |
| `lu2025toolsandbox` | ToolSandbox | Findings of NAACL 2025，DOI 已核验 | 全文 |
| `zhang2025asb` | Agent Security Bench | ICLR 2025 | 摘要 |
| `andriushchenko2025agentharm` | AgentHarm | ICLR 2025 | 全文 |
| `zhuge2025agentasajudge` | Agent-as-a-Judge | ICML 2025 / PMLR 267 | 全文 |
| `dong2024agentops` | AgentOps | arXiv 2024 | 全文 |
| `lesellierdechezelles2025browsergym` | BrowserGym Ecosystem | TMLR 2025 | 全文 |
| `yin2024safeagentbench` | SafeAgentBench | arXiv 2024 | 全文 |
| `zhang2024agentsafetybench` | Agent-SafetyBench | arXiv 2024 | 全文 |
| `zhan2025adaptiveattacks` | Adaptive Attacks | Findings of NAACL 2025，DOI 已核验 | 摘要 |
| `zhu2025multiagentbench` | MultiAgentBench | ACL 2025，DOI 已核验 | 全文 |
| `cemri2025multiagentfailures` | Why Do Multi-Agent LLM Systems Fail? | NeurIPS 2025 D&B | 摘要 |
| `wang2026agentspec` | AgentSpec | ICSE 2026 accepted；DOI 待核验 | 摘要 |
| `lu2025agentrewardbench` | AgentRewardBench | COLM 2025 | 全文 |

### 证据限制

- “已阅读全文”支持方法、实验设置、数值、复现信息和作者局限性分析；
- “仅阅读摘要”只支持目标、总体方法和摘要明确结论；
- 本综述未使用未核验的引用次数；
- AgentSpec 的正式接收身份已核验，但 DOI 尚未核验，因此 BibTeX 不含 DOI；
- SafeAgentBench 与 Agent-SafetyBench 按当前可核验的 arXiv 身份引用；
- 模型/API/网站会变化，所有性能数字均是论文特定时间、模型与脚手架的快照。
