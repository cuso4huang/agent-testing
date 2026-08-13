# AI 智能体测试：研究空白与可实施项目方向

> 依据 2020–2026 文献证据整理，最后更新：2026-07-23。选题优先考虑可在一学期内形成可运行系统、可重复实验、论文图表和简历成果，而不是只提出概念框架。

## 一、研究空白的优先级

现有研究已经有大量“测谁分数更高”的基准，但以下能力仍明显不足：

1. **缺少跨框架故障注入标准。** 超时、限流、部分返回、schema 漂移、竞态、幂等失败和错误补偿没有统一的注入 API、强度定义和结果格式。
2. **直接测试 agent 的变形/属性测试很少。** 很多标题包含 agent 的工作，实际是让 agent 测传统软件；语义等价输入下 agent 是否保持行为一致仍缺工具。
3. **轨迹 oracle 两端都有缺陷。** 精确规则漏掉等价正确路径，LLM judge 又会被 agent 自述、长上下文和页面 grounding 误导。
4. **线上可观测性缺统一语义。** 不同框架的 plan、tool、memory、guardrail 和 evaluator 事件难以合并；trace 完整性与隐私保护也冲突。
5. **多智能体只看团队总分。** 对错误从哪个角色产生、经哪条消息传播、污染多少共享状态、何时变成级联失败，缺少因果指标。
6. **稳定性与成本统计不足。** 昂贵基准常只跑一次；缺少 `pass^k`、置信区间、每成功成本和长期版本漂移。
7. **MCP/工具供应链缺成熟基准。** 工具服务器身份、schema 签名、恶意描述/返回、版本回滚、依赖替换和跨工具权限组合需要系统测试。

下面五个选题分别覆盖上述最可实现的空白。

## 选题 1：ChaosAgent——工具智能体可靠性与故障注入平台

### 研究问题

当工具出现超时、限流、部分成功、返回格式变化、重复执行或语义错误时，不同 agent 架构如何退化？重试、重规划、幂等键和补偿事务分别能解决哪些失败，代价是多少？

可检验假设：

- H1：单次 task success 会显著高估含随机工具故障时的连续可靠性；
- H2：结构化错误语义和幂等工具可提高恢复率，但盲目重试会增加副作用和费用；
- H3：不同 agent 框架的主要差异更多来自恢复策略和状态管理，而不只来自底层模型。

### 实现目标

实现一个位于 agent 与工具之间的故障代理，能够按场景、概率、调用序号和工具类型注入故障；自动保存执行轨迹、状态差分、恢复行为、费用和延迟，并生成可靠性曲线和根因报告。

建议支持的第一批故障：

1. 固定/随机延迟与超时；
2. HTTP 429/5xx、连接中断；
3. 字段缺失、类型变化、schema 版本漂移；
4. 部分结果、陈旧结果和相互矛盾结果；
5. 写操作“已执行但响应丢失”；
6. 重复调用、非幂等副作用；
7. 权限临时失效；
8. 工具返回中夹带不可信指令。

### 推荐技术栈

- Python 3.11、pytest、Hypothesis、Pydantic/JSON Schema；
- FastAPI/mitmproxy 作为工具故障代理；
- Docker Compose 隔离数据库与工具服务；
- OpenTelemetry + Jaeger/Tempo，Prometheus + Grafana；
- LangGraph 或 OpenAI Agents 作为第一种 agent，另选 AutoGen/CrewAI 中一种做跨框架比较；
- pandas/scipy/statsmodels 生成统计和置信区间。

### 公开数据集或基准

- τ-bench：用户—agent—数据库和 `pass^k`；
- ToolSandbox：状态依赖、milestone/minefield；
- AppWorld：expected/allowed 数据库差分；
- 可选 SWE-bench Lite：外部命令、依赖和测试故障。

### 实验设计

设任务为 `t`、故障类型为 `f`、故障强度为 `λ`、语义扰动为 `ε`、重复为 `k`：

```text
R(t, f, λ, ε, k)
```

实验包含：

1. 无故障基线；
2. 每种故障 3–5 个强度；
3. 原始 agent、简单重试、错误分类重规划、幂等/补偿版本；
4. 两种 agent 框架、至少两种模型；
5. 每个设置重复 5–10 次；
6. 使用分层 bootstrap 或二项区间，报告任务和 seed 方差；
7. 对恢复失败轨迹做自动聚类并人工核验小样本。

### 评价指标

- task success、`pass^k`；
- 故障检测率、恢复率、恢复步骤；
- 非预期状态变化、重复副作用、数据损坏；
- mean time to recovery；
- token、工具调用、每成功成本；
- p50/p95/p99 端到端延迟；
- 恢复策略的安全—效用—成本 Pareto 前沿。

### 主要难点

- 区分“响应丢失但写入成功”和“根本未写入”；
- 让语义错误具有现实性且不被简单 schema validator 捕获；
- 控制闭源模型漂移和昂贵重复运行；
- 保证故障代理本身不改变正常请求语义；
- 为不可逆动作设计可重置或补偿环境。

### 预计创新点

- 统一结构故障、语义故障和副作用故障；
- 将 chaos engineering 与 agent 的 `pass^k`、状态差分、经济成本放在同一实验框架；
- 提供跨 agent 框架的故障事件 schema；
- 用“已执行但响应丢失”系统测试重复扣费等真实高风险场景。

### 最小可行版本

- 1 个 τ-bench 或 AppWorld 领域；
- 30 个任务；
- 4 类故障；
- 2 个恢复策略；
- 1 个 agent 框架、2 个模型；
- 自动生成一份 HTML/Markdown 可靠性报告。

约 6–8 周可完成 MVP；后续 4 周扩展第二框架和统计实验。

### 可扩展方向

- 自动学习最可能暴露失败的故障调度；
- 生产流量回放和 shadow testing；
- 多工具事务、补偿与 saga；
- MCP server 故障、身份替换和 schema 签名；
- 将失败自动最小化并生成 pytest 回归用例。

### 可写入简历的项目成果

> 设计并实现跨工具故障注入平台，覆盖超时、限流、schema 漂移与非幂等副作用；在公开 agent benchmark 上完成多次重复实验，自动计算 `pass^k`、恢复率、每成功成本和 p95 延迟，并用 OpenTelemetry 定位根因。

## 选题 2：AgentMorph——智能体变形与属性测试生成器

### 研究问题

如何自动生成“任务语义保持不变、预期终态或轨迹关系应保持不变”的测试变体？变形关系能否比固定 benchmark 发现更多不稳定、位置偏差、实体绑定错误和工具 schema 过拟合？

### 实现目标

建立一个变形测试 DSL 和生成器，输入原始任务、环境与 oracle，输出成组变体；执行后检查结果不变量、单调关系或轨迹关系，并自动缩减产生违反的最小变体。

首批变形关系：

- 用户指令释义、语序变化、礼貌/冗余信息；
- 无关事实和无关工具插入；
- 实体一致重命名；
- 等价日期/单位/格式转换；
- 可交换只读工具调用；
- 等价初始数据库状态；
- 工具名称/描述非语义变化；
- 同义错误消息；
- 已知不应影响结果的页面布局变化；
- 权限收紧后的单调性：不得产生更多高风险动作。

### 推荐技术栈

- Python、Hypothesis、Pydantic；
- Lark/ANTLR 定义 metamorphic relation DSL；
- sentence-transformers 或 NLI 模型做语义候选过滤；
- Z3 验证结构约束与终态可满足性；
- Docker、Playwright 或 AppWorld/τ-bench 环境；
- delta debugging 做失败变体最小化。

### 公开数据集或基准

- AppWorld：状态 diff 与 contrast scenarios；
- τ-bench：状态终态和政策；
- ToolSandbox：milestone/minefield；
- WebArena 或 BrowserGym：网页任务与布局/输入扰动；
- PDoctor 的约束式任务生成思想。

### 实验设计

1. 人工定义 30–50 条变形关系，专家审核是否保持语义；
2. 对 100–300 个原始任务各生成 3–10 个变体；
3. 比较随机释义、纯 LLM 生成、DSL+约束生成三种方法；
4. 使用两种模型和至少两种 agent scaffold；
5. 将违反分为真实不一致、环境噪声、oracle 错误和 MR 误报；
6. 人工复核分层样本并估计 precision；
7. 统计新发现缺陷是否已被原基准 failure taxonomy 覆盖。

### 评价指标

- metamorphic-relation violation rate；
- 真缺陷 precision/recall（在人工审核集上）；
- 独立失败簇数量和首次发现时间；
- 原任务成功但变体失败的比例；
- 失败最小化幅度；
- 任务/工具/状态覆盖；
- 每发现一个有效缺陷的成本；
- 跨模型、跨框架复现率。

### 主要难点

- “自然语言等价”本身没有完美 oracle；
- 某些变体会改变难度而非语义；
- 动态网页和用户模拟器可能造成伪违反；
- 结果相同但轨迹不同，关系应如何定义；
- LLM 生成器和被测模型同源时可能有相关偏差。

### 预计创新点

- 同时定义输入、环境、工具 schema、终态和轨迹五类 MR；
- 把关系从“输出应相同”扩展为“终态等价、过程约束保持、成本不应异常放大”；
- 结合约束求解与 LLM 候选生成；
- 自动把违反缩成可复现回归用例。

### 最小可行版本

- AppWorld 或 τ-bench 任选一个；
- 100 个任务、10 条人工验证 MR；
- 一个 agent、两个模型；
- 支持批量执行、违反分类和 delta debugging；
- 输出至少 10 个经人工确认的独立失败案例。

### 可扩展方向

- 从失败轨迹自动归纳新 MR；
- 覆盖引导的灰盒变异；
- 多智能体消息与拓扑 MR；
- 安全单调性和权限 MR；
- 与 CI 集成，对模型/提示升级自动回归。

### 可写入简历的项目成果

> 开发面向 LLM agent 的变形/属性测试框架，支持任务释义、实体重命名、工具 schema 和环境状态等价变异；实现约束校验与失败最小化，在公开 benchmark 上发现并复现多类固定测试集未覆盖的不稳定行为。

## 选题 3：HybridTrajectoryJudge——可校准的混合轨迹 Oracle

### 研究问题

确定性状态规则、milestone/minefield、专用分类器和 LLM judge 应怎样组合，才能在保持高 precision 的同时提高对等价正确路径的 recall，并控制成本和延迟？

### 实现目标

构建风险感知的分层 evaluator：

```text
确定性规则
  → 轨迹结构/状态特征
  → 轻量分类器
  → LLM/VLM judge
  → 低置信或高风险案例人工升级
```

每个判定都返回证据片段：状态差分、页面元素、工具调用、milestone、禁止事件和 judge 理由。系统不能只给一个分数。

### 推荐技术栈

- Python、pandas、scikit-learn/lightgbm；
- JSONLogic、OPA/Rego 或自研规则层；
- Pydantic 轨迹 schema、NetworkX milestone DAG；
- 小型开源 LLM/VLM 或 API judge；
- calibration：isotonic regression、Platt scaling；
- Streamlit/React 展示分歧和证据；
- Label Studio 用于人工复核。

### 公开数据集或基准

- AgentRewardBench：1,302 条专家标注 Web 轨迹；
- AppWorld：数据库状态差分；
- WebArena/VisualWebArena：规则与视觉/语义判断；
- ToolSandbox：里程碑和雷区；
- Agent-as-a-Judge 的 DevAI：层级需求与工作区证据。

### 实验设计

1. 使用 AgentRewardBench 官方划分，避免在测试集调提示；
2. 基线：纯规则、纯 LLM judge、专用 evaluator、简单多数投票；
3. 混合方法：规则硬判 + 分类器置信 + 风险分层升级；
4. 做 screenshot/A11Y/工具轨迹/状态差分输入消融；
5. 比较是否提供 agent reasoning，检验“被自述误导”；
6. 在一个跨域集合（如 AppWorld）验证外部泛化；
7. 对所有 evaluator—专家分歧做抽样错误分析；
8. 固定模型版本后重复 judge 5 次，测自身稳定性。

### 评价指标

- success 判断 precision、recall、F1、AUPRC；
- side effect/repetition 检测；
- expected calibration error、Brier score；
- 人工升级率与升级后的整体错误率；
- judge 重复一致性；
- 单轨迹与每正确判定成本；
- p50/p95 评审延迟；
- 证据定位准确率。

### 主要难点

- 专家标签也有不一致；
- Web 截图/A11Y 很长，易造成 grounding 错误；
- 规则适配新任务需要工程；
- 低风险任务可容忍的 judge 错误不适用于高风险写操作；
- 防止训练/提示接触测试任务造成污染。

### 预计创新点

- 用风险而不是统一阈值决定是否升级昂贵 judge/人工；
- 对 judge 输出做概率校准和重复稳定性测试；
- 强制每个语义判定引用可验证轨迹证据；
- 把 oracle precision、成本和人工工作量放在一个 Pareto 分析中。

### 最小可行版本

- AgentRewardBench 的 200–400 条轨迹；
- 三类 oracle：规则、一个 LLM judge、一个混合策略；
- 支持成功、副作用、重复三类标签；
- 一个分歧审查仪表盘；
- 至少完成 100 条人工复核。

### 可扩展方向

- 训练轻量级本地 trajectory reward model；
- 主动学习选择最值得人工标注的轨迹；
- 多模态证据压缩；
- 针对代码、工具和具身轨迹的跨域版本；
- evaluator 的红队测试和提示注入防护。

### 可写入简历的项目成果

> 构建混合轨迹评测系统，将状态规则、里程碑、校准分类器和 LLM judge 分层组合；在专家标注 Web-agent 轨迹上评估 precision/recall、校准、成本和延迟，并实现证据级分歧审查仪表盘。

## 选题 4：TraceOps——智能体可观测性、在线检测与断路器

### 研究问题

哪些 agent 专属 span 和在线信号能在低误报条件下，尽早发现循环、预算失控、错误工具参数、状态漂移和提示注入？告警后的自动干预能否真正提高成功率，而不是只让 agent 更早失败？

### 实现目标

为一个主流 agent 框架实现 OpenTelemetry instrumentation、实时 detector 和策略化 circuit breaker：

- loop/stall detector；
- token/cost budget detector；
- schema/argument anomaly detector；
- state-drift/duplicate-side-effect detector；
- untrusted-data-to-sensitive-tool taint detector；
- stop、retry、replan、降权工具、请求确认和人工接管动作。

### 推荐技术栈

- OpenTelemetry SDK/Collector；
- Jaeger 或 Grafana Tempo；
- Prometheus、Grafana、Loki；
- Python agent SDK；
- Redis/Kafka（可选，用于在线事件）；
- River/scikit-learn 做在线统计或前缀分类；
- OPA/Rego 做阻断策略。

### 公开数据集或基准

- AgentOps 的 trace taxonomy；
- SWE-bench Lite 或 SWE-bench 的长轨迹；
- BrowserGym 的 journal/study 记录；
- τ-bench、ToolSandbox 自行注入循环和参数故障；
- AgentDojo 用于不可信数据到写工具的安全 trace。

### 实验设计

1. 注入 6–10 类可控故障，建立真值时间点；
2. 比较仅 LLM span、通用 OpenTelemetry span、完整 agent span；
3. detector 基线：固定规则、统计控制图、轻量前缀分类器；
4. 逐类移除 plan/tool/state/memory/guardrail span，做可观测性消融；
5. 在 0.1%、1%、5% 固定误报率下比较召回和告警提前量；
6. 进行闭环实验：无干预、停止、重试、重规划、人工确认；
7. 评估 trace 脱敏对诊断性能的影响。

### 评价指标

- 故障检测率、precision、AUPRC；
- 固定低误报率下 recall；
- 首次告警提前量；
- mean time to detect / recover；
- 干预后的 task success 增量；
- 被错误阻断的正常任务；
- trace 存储量和运行开销；
- token/费用节省；
- 敏感信息残留率。

### 主要难点

- 合成故障上的高检测率可能不能外推到真实失败；
- “循环”与必要重复有边界；
- 过早阻断会降低效用；
- 原始轨迹可能含密钥和个人信息；
- 不同框架对 plan、memory 和 tool 的抽象不一致。

### 预计创新点

- 从事后 tracing 扩展到可测量干预收益的闭环 observability；
- 报告低误报率下的提前量，而非只报告总体 AUPRC；
- 给出跨框架 agent span 映射；
- 联合评估诊断能力、运行开销和隐私泄露。

### 最小可行版本

- 支持 LangGraph 或 OpenAI Agents 一个框架；
- 6 类故障；
- 3 个在线 detector；
- 一个 stop/replan circuit breaker；
- Jaeger + Grafana 仪表盘；
- 50–100 个任务的对照实验。

### 可扩展方向

- 跨 agent/工具的分布式 trace；
- 多智能体因果图；
- 隐私分级与字段级自动脱敏；
- 生产 canary 与 shadow traffic；
- 从 trace 自动生成回归场景。

### 可写入简历的项目成果

> 为 LLM agent 实现 OpenTelemetry 全链路追踪与实时断路器，覆盖 plan、tool、memory、state diff 和 guardrail；在故障注入实验中量化低误报召回、告警提前量、成功率改善和 trace 开销。

## 选题 5：ContractMAS——多智能体时序合约与级联故障测试

### 研究问题

多智能体系统中，一个角色的错误如何经消息、路由和共享记忆传播？能否用消息 provenance 与时序合约，在不过度降低团队效用的前提下阻断级联失败？

示例合约：

- 未经验证的研究员输出不得直接触发支付/删除工具；
- reviewer 必须在 executor 之前确认关键事实；
- 同一敏感动作不能被两个 agent 重复执行；
- 从外部网页来的内容不得提升为 system-level 指令；
- 共享记忆中的高风险事实必须有两个独立来源；
- 某角色超过预算或连续无进展时必须重新分配任务。

### 实现目标

实现一个可插入 AutoGen/CrewAI 或自研图编排的测试层：

1. 为每条消息和记忆写入记录来源、角色、置信、权限与父事件；
2. 支持角色、消息、路由、记忆和工具五类故障注入；
3. 用 LTL/有限状态机/SMT 表达时序合约；
4. 在执行前检查或阻断；
5. 可视化故障传播图和干预点。

### 推荐技术栈

- Python、AutoGen 或 CrewAI；
- NetworkX/Neo4j 构建消息因果图；
- Spot/LTL、Z3 或自研状态机；
- OpenTelemetry；
- FastAPI + React/Streamlit；
- Docker 沙箱与 PostgreSQL/Redis 共享记忆。

### 公开数据集或基准

- MultiAgentBench/MARBLE 的协作、竞争和拓扑场景；
- Why Do Multi-Agent LLM Systems Fail? 的 failure taxonomy（摘要级起点，实施前需补全文）；
- τ-bench 或 AppWorld 改造成 planner–executor–reviewer 多角色；
- AgentDojo 改造成不可信 research agent 影响执行 agent；
- 后续可引入 MAS-FIRE 预印本故障模型，但不把其未核验结论当作基准真值。

### 实验设计

1. 拓扑：chain、star、tree、mesh；
2. 角色：planner、researcher、executor、reviewer；
3. 故障：错误事实、延迟/丢消息、路由错误、恶意角色、共享记忆污染、重复工具；
4. 强度：污染角色数、传播轮数、消息比例；
5. 对比：无守卫、静态角色权限、时序合约、合约+动态隔离；
6. 每种设置多 seed 重复；
7. 对阻断案例检查是否本可安全完成，以测误阻断。

### 评价指标

- 团队 task success 与 milestone；
- 故障传播深度、受影响 agent 数；
- 首个错误到不可逆副作用的路径长度；
- cascade failure rate；
- 合约 violation recall/precision；
- 正常任务误阻断率；
- 恢复/隔离时间；
- token、消息数、延迟和每成功成本；
- safety–utility Pareto 前沿。

### 主要难点

- 团队内部“错误”可能只是合理分歧；
- attribution 需区分源头错误和放大错误；
- 合约过严会消灭协作灵活性；
- LLM judge 不适合作为唯一传播真值；
- 多 agent × 拓扑 × seed 的实验成本快速增长。

### 预计创新点

- 把消息级 provenance、故障传播图和时序安全合约组合；
- 不只报告团队失败，而是报告源头、传播、放大和阻断；
- 比较不同拓扑对级联风险的影响；
- 引入“最小阻断点”概念，寻找最低效用损失的干预。

### 最小可行版本

- 3 个角色、2 种拓扑；
- 5 类故障、10 条合约；
- 20–30 个工具/研究任务；
- NetworkX 传播图；
- 无守卫与合约守卫的对照实验。

### 可扩展方向

- 动态角色信任和风险预算；
- 恶意 agent 与共谋；
- 跨组织 A2A 协议；
- MCP 工具与多 agent 权限图；
- 自动从失败轨迹合成时序合约；
- 隐私保护的 provenance。

### 可写入简历的项目成果

> 实现多智能体级联故障测试与时序合约引擎，对角色、消息、共享记忆和工具故障进行注入；构建消息级因果传播图，量化级联深度、误阻断、恢复时间及安全—效用权衡。

## 二、选题建议

| 目标 | 优先选择 | 原因 |
|---|---|---|
| 软件测试/后端实习 | ChaosAgent | 工程边界清晰，可展示代理、容错、可观测性和统计 |
| 测试方向毕业论文 | AgentMorph | 研究问题明确，容易形成方法、基线、消融与新缺陷案例 |
| AI 评测/算法实习 | HybridTrajectoryJudge | 有公开专家标签，可做模型、规则、校准和成本实验 |
| DevOps/平台工程 | TraceOps | OpenTelemetry、监控、在线检测和干预成果直观 |
| 多智能体/安全论文 | ContractMAS | 新颖度高，但实验设计和归因难度最大 |

如果时间只有 8–10 周，优先做 ChaosAgent 或 HybridTrajectoryJudge。若有完整一学期并希望形成论文，AgentMorph 的方法学边界最清楚。ContractMAS 潜在创新最大，但建议先完成小型确定性环境，避免被复杂的 LLM judge 和多 agent 成本拖垮。

## 三、共同的研究规范

无论选择哪一题，都应：

- 固定并记录模型精确版本、提示哈希、框架 commit、工具 schema 和环境镜像；
- 预注册主要假设、指标和排除规则；
- 同一设置多次运行并报告置信区间；
- 区分 agent、环境、工具和 evaluator failure；
- 先验证测试工具自身，再测试 agent；
- 保存最小失败案例和完整可重放 trace；
- 报告总成本、每成功成本和 p95 延迟；
- 将规则 oracle 与人工校准作为高风险结论的底座；
- 对新的 LLM judge、模拟器或公开预印本保持明确证据等级。
