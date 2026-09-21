# AgentDoS 相关工作与后续研究方向评估

检索日期：2026-07-29

## 1. 结论先行

**值得作为后续研究方向，但不能只做“AgentDoS 换一种资源类型”的增量工作。**

综合评分：**8/10（选题收敛得好）**；如果只是增加 CPU、网络或 API 费用耗尽，则约 **5/10**。

最值得做的方向不是再提出一种 DoS 攻击，而是：

> **面向 LLM Agent 完整轨迹的统一资源安全分析与预算执行：同时覆盖 token、时间、工具调用、内存、磁盘、网络、API 费用和跨轮持久状态，并提供可验证的检测与防御。**

理由：

- AgentFuzz 和 AgentDoS 已证明“程序分析 + 语义种子 + 灰盒反馈”能在真实 Agent 中发现大量漏洞。
- 2026 年出现了工具调用链放大、无限 Agent 循环、推理级 DoS、Guardrail DoS 和 MCP 计算劫持，说明 availability/cost security 已成为独立研究簇。
- 现有论文各自盯住一种资源或一个层次，缺少跨资源、跨层次、跨会话的统一模型。
- 现有防御多是 max tokens、timeout、tool-call limit 等局部阈值，容易误杀合法长任务，也难处理嵌套 Agent、并行工具和资源转移。

## 2. 检索范围与方法

研究问题：AgentDoS 所代表的“LLM Agent 实现层资源耗尽 + 灰盒 Fuzzing”是否仍有可发表、可持续的研究空间？

范围：

- 时间：2023-07 至 2026-07；
- 类型：同行评审论文、正式会议页面、arXiv/OpenReview 预印本；
- 主题：Agent vulnerability detection、greybox fuzzing、resource exhaustion、economic/latency DoS、infinite loop、tool-chain amplification、MCP resource abuse；
- 纳入标准：直接研究 LLM Agent，或方法对 AgentDoS 的程序分析、反馈、预言机和资源模型有直接借鉴价值；
- 排除：仅讨论普通 Web/智能合约 Fuzzing、没有 Agent 关联的泛化 LLM 安全论文。

数据源：Semantic Scholar、arXiv、Crossref、OpenAlex、USENIX 官方页面、期刊 DOI 页面。

主要查询：

- `LLM agent fuzzing vulnerability detection greybox AgentFuzz`
- `"resource exhaustion" "LLM-based agents"`
- `"denial of service" "LLM agents"`
- `LLM agent cost attack resource abuse denial service`
- `"infinite agentic loops" OR "tool calling chains"`
- `MCP computational resource exploitation agent`

## 3. 核心证据表

| 工作 | 年份/状态 | 核心对象与方法 | 与 AgentDoS 的关系 | 证据级别 | 核验 |
|---|---|---|---|---|---|
| AgentFuzz, *Make Agent Defeat Agent* | USENIX Security 2025 | 对 taint-style 漏洞做定向灰盒 Fuzzing；语义种子、多维反馈、功能/参数变异 | AgentDoS 的直接方法前身 | 官方全文 | USENIX 官方记录，Verified |
| AgentDoS, *Autonomy Comes with Costs* | USENIX Security 2026 预印本 | 静态分析资源操作与生命周期，以资源消耗指导语义 Fuzzing | 基准工作 | 本地全文 | 官方预印本/会议材料，Partially verified |
| Aegis | arXiv:2508.19504 | 将超过 turn/token 预算归为 agent-environment resource exhaustion，并做环境优化 | 说明资源耗尽既是攻击面也是可靠性问题 | 摘要/部分正文 | arXiv + DBLP，Partially verified |
| *Beyond Max Tokens* | arXiv:2601.10955 | 操纵 MCP 工具返回，引导长工具链；保持答案正确，同时放大 token、费用和能源 | 从实现层内存/磁盘扩展到经济与工具链 DoS | 摘要 | arXiv，Partially verified |
| ChainFuzzer | arXiv:2603.12614 | 从 source-to-sink 数据流抽取多工具链，使用 trace-guided prompt solving 与 sink oracle | 将 AgentDoS 的“单组件/资源 sink”推广到工作流级漏洞 | 摘要 | arXiv + Semantic Scholar，Partially verified |
| VeriGrey | arXiv:2603.17639 | 使用工具调用序列作为覆盖反馈，做灰盒 prompt mutation | 提供比代码距离更通用的 Agent 行为覆盖信号 | 摘要/算法页 | arXiv，Partially verified |
| OTora | arXiv:2605.08876 | 保持任务正确，但放大推理深度和工具预算，形成 reasoning-level DoS | 将资源预言机扩展到 reasoning tokens 和 latency | 摘要 | arXiv，Partially verified |
| *From Shield to Target* | arXiv:2606.14517 | 诱导 Agent guardrail 进入长推理，放大 token 和延迟 | 说明安全组件自身也属于资源攻击面 | 摘要 | arXiv，Partially verified |
| *When Agents Do Not Stop* | arXiv:2607.01641 | Agent IR + Agentic Loop Dependence Graph，静态检测未受限反馈环 | 与 AgentDoS 的资源生命周期互补：一个建模“累积”，一个建模“循环” | 摘要 | arXiv，Partially verified |
| LeechHijack | arXiv:2512.02321 | 恶意 MCP 工具在权限范围内劫持用户计算资源 | 从资源耗尽拓展到资源盗用和成本归属 | 摘要 | arXiv，Partially verified |
| ThinkTrap | arXiv:2512.07086 | 黑盒优化使 LLM 进入超长/无限推理 | 模型服务层 DoS 对照组，不是 Agent 实现层 | 摘要 | arXiv，Partially verified |
| Gasmi et al., *Bridging AI and software security* | Information Sciences 740 (2026) | 对 Function Calling 与 MCP 做统一攻击分类和 3,250 个场景比较 | 证明传统软件 DoS 与 Agent 专属风险需要统一研究 | 摘要 | DOI 10.1016/j.ins.2026.123231；Crossref/OpenAlex 一致，Verified |

说明：除 AgentDoS 和 AgentFuzz 外，大部分 2026 新论文仅检查了官方摘要或有限正文，因此这里只使用其公开的高层方法和作者报告结果，不把它们当作已经独立复现实验的事实。

## 4. 相关工作形成的研究版图

### 4.1 漏洞发现方法已经从“prompt 攻击”走向程序分析

AgentFuzz 的关键转折是把 Agent 当作软件系统：从安全 sink 反向分析调用链，再让 LLM 生成能够到达 sink 的自然语言输入。AgentDoS 延续该范式，但将反馈和预言机改成资源生命周期与资源消耗。

ChainFuzzer 又向前推进一步：漏洞不一定存在于单个工具中，而可能只在多工具 source-to-sink 组合中出现。VeriGrey 则说明，在无法稳定使用行级代码覆盖时，“工具调用序列”本身可以作为 Agent 行为覆盖。

因此，后续工作若仍只使用单一 sink distance，会落后于当前进展。新的反馈模型应该联合：

- 代码控制流和数据流；
- 工具调用序列与状态转移；
- 资源增量和资源生命周期；
- 语义目标完成度；
- 危害/费用是否跨安全边界传播。

### 4.2 DoS 已经分裂成多个层次

目前至少有六种不同的 availability/cost failure：

1. **模型推理层**：输入诱导超长或无限 reasoning，例如 ThinkTrap。
2. **Agent 规划层**：保持答案正确，但增加推理深度和工具预算，例如 OTora。
3. **工具交互层**：工具返回引导长链交互和上下文膨胀，例如 Beyond Max Tokens。
4. **Agent 实现层**：内存、磁盘和历史状态无界增长，即 AgentDoS。
5. **控制流层**：模型调用、工具调用、工作流节点或 Agent handoff 形成无界循环，即 Infinite Agentic Loops。
6. **安全基础设施层**：Guardrail 自己被拖入长推理，成为共享瓶颈。

现有工作大多各测一层。真实部署中的攻击却可以跨层传播，例如：

```text
恶意工具响应
  → Agent 重规划循环
  → 对话历史增长
  → Guardrail 每轮重复扫描
  → token、延迟、内存和费用同时放大
  → 同租户请求饥饿
```

这正是统一资源安全研究的空间。

### 4.3 现有预言机过于局部

不同论文分别使用：

- 内存/磁盘阈值；
- token 或 latency amplification；
- 是否到达危险 sink；
- 是否出现新工具序列；
- 是否形成未受限循环；
- 最终答案是否仍然正确。

缺少能够回答以下问题的统一 oracle：

- 增长是合法任务需求，还是异常放大？
- 资源属于哪个用户、Agent、子任务或工具？
- 任务成功但成本高 100 倍，是否应该判失败？
- 资源增长是否会影响同租户或其他用户？
- 强制终止后，系统是否留下半完成外部副作用？

## 5. 研究空白

### Gap A：统一的 Agent Resource IR

目前没有被广泛采用的中间表示，同时表达：

- LLM 调用、工具调用、Agent handoff；
- 内存对象、磁盘对象、网络流量、token 和费用；
- 资源的创建、别名、转移、释放和持久化；
- 单步、任务、会话、用户、租户和全局生命周期；
- 显式循环和由框架语义产生的隐式反馈环。

可以在 AgentDoS 的生命周期模型和 IAL-Scan 的循环依赖图之间建立统一表示。

### Gap B：任务感知的资源预言机

固定阈值会把长篇研究、代码构建、批量数据处理等合法任务误判为攻击。需要基于任务规模建立“合理成本基线”，检测：

- 资源放大率；
- 单位有效进展的边际成本；
- 重复或无新信息的工具调用；
- 停止概率随轨迹长度的变化；
- 与相似成功轨迹相比的异常偏离。

### Gap C：跨资源、跨层放大

大部分工作只优化一个目标，如 token、内存或延迟。值得研究多目标 Fuzzing：

\[
\text{maximize }(\text{token},\text{latency},\text{memory},
\text{disk},\text{API cost},\text{side effects})
\]

同时约束任务仍然可完成、输入自然、危害可复现。

更安全的表述和实验方式是将其用于受控环境中的防御评测，而不是开发现实攻击载荷。

### Gap D：分层预算与预算传播

现有系统通常只有全局 max tokens 或 timeout。嵌套 Agent 和工具调用需要预算契约：

- 父任务向子任务分配多少预算；
- 未用预算是否返还；
- 重试是否消耗新预算；
- 并行分支如何共享预算；
- 不可信工具能否诱导 Agent 扩大预算；
- 哪些安全步骤不能因预算不足被跳过。

### Gap E：终止后的安全恢复

DoS 防御不能只做 kill。Agent 可能已经：

- 发出部分邮件；
- 写入半个文件；
- 完成部分支付；
- 创建临时云资源；
- 修改持久记忆。

需要研究 budget exhaustion 下的事务化回滚、补偿动作和可恢复性 oracle。

### Gap F：统一、可复现的 benchmark

AgentDoS 通过多个系统发现真实漏洞，但该领域缺少稳定公共基准。一个好的 benchmark 应包含：

- 多种 Agent 框架和 MCP/Function Calling 架构；
- 短生命周期、会话级和跨会话资源；
- benign long-running 与 malicious amplification 成对任务；
- CPU、内存、磁盘、网络、token、费用与外部副作用；
- ground-truth 资源边界、修复版本和回归测试；
- 多租户干扰与公平性指标。

## 6. 建议选择的具体课题

### 首选：RABench + ResourceGuard

暂定题目：

> **Resource-Aware Greybox Validation for Stateful LLM Agents**

研究问题：

1. 如何构建统一 Agent Resource Graph，跨框架恢复资源的创建、传播、累积与释放？
2. 如何用“单位任务进展的资源成本”指导灰盒测试，而不是仅用 sink distance？
3. 如何自动合成与任务语义一致的长程测试，覆盖单轮、跨轮、跨 Agent 和跨工具链放大？
4. 如何执行层次化预算契约，并在终止时安全回滚？

预期贡献：

- 一个框架无关 Resource IR；
- 一个任务感知、多资源灰盒测试器；
- 一个包含 benign/adversarial 对照的公开 benchmark；
- 一个运行时预算执行与恢复原型；
- 对多个真实 Agent 框架的实证研究。

新颖性：高于单纯扩展 AgentDoS，因为它从单一漏洞检测上升到统一 assurance。

风险：工程量大，需要先限定 2-3 个框架和 3 类资源。

### 次选：Budget Contract for Nested Agents

聚焦多 Agent、子 Agent 和工具链中的预算传播与隔离。

优点：

- 防御导向，伦理风险较低；
- 与工业实际需求强相关；
- 可用形式化不变量和运行时 enforcement 做出清晰贡献。

风险：

- 需要构造足够真实的嵌套 Agent workload；
- 单纯工程限流不够，需要证明比全局 timeout/max-token 更少误杀且更能阻断放大。

### 次选：Differential Resource Testing

对同一任务在不同模型、框架、工具描述和 Guardrail 配置下执行，寻找资源使用的异常差异。

优点：

- 不依赖每个任务的绝对“正确资源阈值”；
- 可以发现模型/框架升级引入的性能与安全回归；
- 容易做成持续集成工具。

风险：

- 非确定性大，需要统计检验、重复运行和环境归一化；
- 差异不一定等于漏洞，需要更强的归因方法。

## 7. 不建议单独做的课题

- “把 AgentDoS 从内存/磁盘扩展到 CPU”：贡献过窄。
- “再设计一种让 Agent 多调用几次工具的 prompt”：已被多篇 2026 工作覆盖。
- “只比较 max token、timeout 和 rate limit”：更像工程评测，研究问题不足。
- “仅用 LLM judge 判断资源攻击是否成功”：资源安全应优先使用可测量的系统 oracle。
- “只在一个 toy Agent 上做攻击成功率”：目前相关论文已普遍使用真实框架和真实应用。

## 8. 可行性评估

| 维度 | 评价 |
|---|---|
| 学术新颖性 | 中高；单点攻击拥挤，但统一资源模型、防御与 benchmark 仍有明显空白 |
| 技术深度 | 高；涉及程序分析、Fuzzing、系统监控、Agent runtime 和统计评估 |
| 数据/系统可得性 | 较好；大量开源 Agent 和 MCP 工具可用于受控测试 |
| 复现实验难度 | 中高；模型非确定性、API 成本和框架快速变化是主要挑战 |
| 伦理风险 | 中；应使用本地/隔离环境、合成资源和负责任披露 |
| 工业价值 | 高；费用失控、卡死、共享服务饥饿是实际部署问题 |
| 投稿潜力 | 取决于贡献形态；漏洞发现适合安全会议，统一测试/IR 可面向 ICSE/ASE/FSE，运行时资源治理可面向系统与安全交叉 venue |

## 9. 最小可行研究计划

### 第 1 阶段：4-6 周

- 复现 AgentDoS 的资源生命周期抽象，不运行或传播未披露漏洞输入；
- 选择 LangGraph、AutoGen/CrewAI、MCP Agent 中的 2-3 个框架；
- 收集正常长任务轨迹，定义统一资源事件 schema；
- 初步测量 token、工具次数、内存、磁盘、网络和任务进度。

### 第 2 阶段：6-8 周

- 构建 Resource Graph；
- 实现任务进度/资源成本反馈；
- 设计安全的合成型资源放大任务；
- 与随机测试、黑盒 LLM red team、AgentFuzz/VeriGrey 风格反馈做比较。

### 第 3 阶段：6-8 周

- 实现层次化预算和安全终止；
- 建立 benign long-task 对照，测量误杀率；
- 做跨模型、跨框架和多租户实验；
- 发布 benchmark、检测规则和经过脱敏的复现材料。

### 建议的核心指标

- vulnerability/violation recall 与 precision；
- time-to-detection；
- 每百万 token 的有效发现数；
- 资源放大率；
- 单位任务进展成本；
- benign task false-positive/abort rate；
- 防御后的任务成功率与额外开销；
- 终止后的状态一致性和副作用回滚率。

## 10. 最终判断

AgentDoS 不是一个已经结束的孤立课题，而是新兴的 **Agent resource security / economic availability** 方向中的早期代表工作。2026 年大量相关论文同时出现，说明需求真实，也意味着简单跟随式工作会迅速失去新颖性。

因此建议继续，但把题目从：

> “如何再发现一种 Agent DoS？”

提升为：

> “如何对有状态、多工具、多 Agent 系统的资源使用进行统一建模、反馈引导测试、预算执行和安全恢复？”

这个版本既继承 AgentDoS 最有价值的程序分析与灰盒 Fuzzing 思想，也能与当前工具链、循环、推理和 Guardrail DoS 工作形成清晰区别。

