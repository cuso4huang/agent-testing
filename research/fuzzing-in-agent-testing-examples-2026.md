# 模糊测试在 LLM Agent 测试中的应用实例

检索日期：2026-07-29

## 1. 如何把传统 Fuzzing 映射到 Agent

传统模糊测试循环是：

```text
seed → mutation → execution → coverage/feedback → oracle → retain or discard
```

用于 LLM Agent 后通常变成：

| 传统概念 | Agent 测试中的对应物 |
|---|---|
| Seed | 自然语言任务、间接注入内容、工具返回、遥测数据、多轮对话状态 |
| Mutation | 语义改写、参数/实体替换、任务与攻击目标绑定、规模/次数放大、工具载荷变异 |
| Coverage | 代码/调用链距离、工具调用序列、跨 Agent 交互边、资源增量、多工具 source-to-sink 链 |
| Execution | 让 Agent 真正规划、调用工具、更新状态并与环境交互 |
| Oracle | 是否到达危险 sink、敏感数据是否进入 sink、资源是否无界增长、是否违反 Agent 规格、是否出现循环/失败调用 |
| Corpus update | 保留产生新工具路径、新交互路径、更近 sink 或更高资源消耗的输入 |

## 2. 核心论文案例

### 2.1 AgentFuzz：污点型漏洞的定向灰盒 Fuzzing

**论文**：Fengyu Liu et al. *Make Agent Defeat Agent: Automatic Detection of Taint-Style Vulnerabilities in LLM-based Agents*. USENIX Security 2025.

测试目标：用户可控自然语言是否能经过 Agent 规划和参数生成，到达 SQL、命令执行、代码执行等安全敏感 sink。

Fuzzing 映射：

- Seed：LLM 根据 Agent 功能、类名和方法名生成特定功能的自然语言请求。
- Mutation：功能变异与参数变异；根据用户 prompt 和运行时参数的重叠，定位应修改的部分。
- Feedback：语义相关性 + 到目标调用链的程序距离 + 是否满足路径约束。
- Oracle：污点是否从用户输入传播到危险 sink，并触发可利用行为。

论文在 20 个开源 Agent 应用中发现 34 个高风险零日漏洞，官方页面报告其中 23 个获得 CVE。

意义：这是把 directed greybox fuzzing 系统性引入 LLM Agent 漏洞检测的代表工作。

来源：https://www.usenix.org/conference/usenixsecurity25/presentation/liu-fengyu

状态：USENIX Security 2025 正式论文，官方全文已检查，Verified。

### 2.2 AgentDoS：以资源消耗为反馈和预言机

**论文**：Jiaqi Luo et al. *Autonomy Comes with Costs: Detecting Denial-of-Service Vulnerabilities Caused by Resource Abusing in LLM-based Agents*. USENIX Security 2026.

测试目标：自然语言请求是否能诱导 Agent 无界下载、保存或累积数据，耗尽内存/磁盘。

Fuzzing 映射：

- Seed：根据资源操作对应的 Agent 功能生成自然语言请求。
- Mutation：语义保持的规模、次数和跨轮状态变异。
- Feedback：到资源操作符的距离、资源消费潜力、实际资源增量。
- State：显式区分单次调用、任务内和会话级长期资源。
- Oracle：内存/磁盘是否异常或无界增长，而不只是是否到达资源 sink。

论文在 20 个真实 Agent 应用上报告 36 个零日漏洞，影响 16 个应用。

意义：展示了 coverage 不一定是代码分支，也可以是领域反馈，如资源生命周期与消费量。

来源：https://www.usenix.org/system/files/conference/usenixsecurity26/sec26_prepub_luo.pdf

状态：USENIX Security 2026 官方预印本；本地全文已检查，Verified（官方会议记录）。

### 2.3 ChainFuzzer：跨工具工作流级灰盒 Fuzzing

**论文**：Jiangrong Wu et al. *ChainFuzzer: Greybox Fuzzing for Workflow-Level Multi-Tool Vulnerabilities in LLM Agents*. arXiv:2603.12614.

测试目标：单个工具可能都安全，但多工具组合后出现 source-to-sink 数据流漏洞。

Fuzzing 映射：

- 静态引导：从高影响操作向上游抽取可能的工具链。
- Seed/求解：Trace-guided Prompt Solving 生成能稳定驱动 Agent 执行目标工具链的 prompt。
- Mutation：针对 guardrail 和具体 sink 变异载荷。
- Feedback：目标工具链是否可达、数据是否沿预期跨工具传播。
- Oracle：sink 专用安全预言机，并要求严格的 source-to-sink 证据。

摘要报告：在 20 个开源 Agent 应用的 998 个工具中确认 365 个可复现漏洞，其中 302 个必须经过多工具执行。

意义：把 fuzzing 单位从“一个危险函数”提升为“长程 Agent 工作流”。

来源：https://arxiv.org/abs/2603.12614

状态：arXiv 预印本，摘要已检查，Partially verified。

### 2.4 VeriGrey：使用工具调用序列作为覆盖率

**论文**：Yuntong Zhang et al. *VeriGrey: Greybox Agent Validation*. arXiv:2603.17639.

测试目标：发现间接 prompt injection、危险工具调用和恶意 Agent skill。

Fuzzing 映射：

- Seed：初始间接注入 prompt。
- Mutation：把正常任务与注入任务语义绑定，使 Agent 认为攻击步骤是完成任务所必需的。
- Coverage：不使用传统代码边覆盖，而使用工具调用序列；产生新序列的输入进入 seed corpus。
- Scheduling：根据已经发现的工具序列分配 mutation energy。
- Oracle：注入任务是否真正通过工具行为完成。

摘要报告：在 AgentDojo 上，相比黑盒基线，使用 GPT-4.1 后端时发现间接注入漏洞的效果提高 33%；还测试了 Gemini CLI 和 OpenClaw。

意义：给出适用于闭源模型权重、但可观测 Agent 工具轨迹的行为覆盖定义。

来源：https://arxiv.org/abs/2603.17639

状态：arXiv 预印本，摘要和算法页已检查，Partially verified。

### 2.5 FLARE：多 Agent 系统的覆盖引导 Fuzzing

**论文**：Mingxuan Hui et al. *FLARE: Agentic Coverage-Guided Fuzzing for LLM-Based Multi-Agent Systems*. arXiv:2604.05289.

测试目标：多 Agent 协调中的无限循环、工具调用失败、错误路由和交互级故障。

Fuzzing 映射：

- Specification：从多 Agent 系统源码和 Agent 定义中抽取规格与行为空间。
- Seed/Mutation：生成并变异会驱动不同 Agent 内部和 Agent 间交互的测试。
- Coverage：分别度量 inter-agent 与 intra-agent coverage。
- Oracle：从抽取的规格构造检查条件，再分析完整执行日志。
- Report：将失败轨迹转化为具体报告。

摘要报告：在 16 个开源多 Agent 应用中达到 96.9% inter-agent coverage 和 91.1% intra-agent coverage，并发现 56 个此前未知、由多 Agent 交互特有的失败。

意义：模糊测试不再只用于安全漏洞，也可以用于一般功能可靠性和协调测试。

来源：https://arxiv.org/abs/2604.05289

状态：arXiv 预印本，摘要已检查，Partially verified。

### 2.6 AIOpsDoom：对 Agent 环境输入做黑盒 Fuzzing

**论文**：Dario Pasquini et al. *When AIOps Become "AI Oops": Subverting LLM-driven IT Operations via Telemetry Manipulation*. USENIX Security 2026.

测试目标：攻击者操纵日志、错误消息等 telemetry，使运维 Agent 形成错误诊断并采取有害修复动作。

Fuzzing 映射：

- Input：不是直接修改用户 prompt，而是通过请求让被管理系统产生 Agent 之后会读取的遥测数据。
- Reconnaissance：先黑盒了解目标系统会产生和消费哪些 telemetry。
- Mutation：Fuzz 请求和 LLM 生成的对抗性错误解释。
- Feedback：遥测是否被成功注入、Agent 诊断和动作是否按攻击目标改变。
- Oracle：Agent 是否执行了危害基础设施完整性的运维动作。

意义：说明 Agent Fuzzing 的输入面不仅是 prompt，也可以是环境观察、工具结果、日志和传感器数据。

来源：https://arxiv.org/abs/2508.06394

状态：USENIX Security 2026 已接收、官方预印本可用，Verified（官方会议记录）。

## 3. 六篇论文横向比较

| 系统 | 主要输入 | 核心变异 | 反馈/覆盖 | Oracle | 发现对象 |
|---|---|---|---|---|---|
| AgentFuzz | 用户 prompt | 功能与参数语义变异 | 语义 + sink 距离 | taint 到危险 sink | SQL/代码/命令等污点漏洞 |
| AgentDoS | 用户 prompt、多轮状态 | 次数、规模、累积变异 | 资源潜力与增量 | 内存/磁盘耗尽 | 资源管理 DoS |
| ChainFuzzer | 驱动工具链的 prompt | guardrail-aware payload | 工具链可达性、跨工具数据流 | sink-specific | 多工具组合漏洞 |
| VeriGrey | 间接注入内容 | 任务-攻击语义绑定 | 工具调用序列 | 注入目标是否执行 | prompt injection/恶意 skill |
| FLARE | 多 Agent 任务与消息 | 行为路径变异 | Agent 内/Agent 间覆盖 | 规格与日志检查 | 循环、路由、协调和工具失败 |
| AIOpsDoom | telemetry/环境状态 | 请求与错误解释变异 | 环境注入和动作变化 | 是否执行有害运维动作 | AIOps 环境操纵 |

## 4. 这些例子揭示的四种应用方式

### 4.1 安全 sink 导向

代表：AgentFuzz、ChainFuzzer。

从危险操作反向构建路径，通过语义 prompt 求解和变异，让 Agent 到达指定 sink。适合代码执行、SQL、SSRF、敏感数据传播和跨工具组合漏洞。

### 4.2 非代码反馈导向

代表：AgentDoS、VeriGrey。

把资源增量或工具调用序列当作传统 branch coverage 的替代物。适合 LLM 内部逻辑不可见，但执行轨迹可观察的系统。

### 4.3 状态和交互空间探索

代表：FLARE、AgentDoS。

测试不再是独立单轮输入，而是需要跨轮、跨 Agent 或跨工作流累积状态。适合循环、状态泄漏、错误 handoff、重试和资源累积。

### 4.4 环境模糊测试

代表：AIOpsDoom。

变异 Agent 观察到的环境信息，而非只修改直接 prompt。可以进一步推广到网页内容、邮件、移动 UI、文件、MCP 工具返回和数据库结果。

## 5. 容易混淆但应区分的另一类工作

以下论文也包含 Agent 和 Fuzzing，但研究问题相反：**Agent 是测试工具的一部分，被测对象是普通软件**。

- FuzzingBrain V2：多 Agent 辅助 OSS-Fuzz 做传统 C/C++ 漏洞发现与复现，arXiv:2605.21779。
- Coverage-Guided Multi-Agent Harness Generation：多个 Agent 自动生成 Java fuzz harness，arXiv:2603.08616。
- PANGOLIN：LLM Agent 帮助分析多语言 IoT 固件接口并生成参数规格，USENIX Security 2026。

它们对“如何用 LLM 生成结构化 seed、理解代码和修复 harness”很有借鉴价值，但不是直接测试 Agent 行为。

## 6. 当前研究空白

1. **统一覆盖标准缺失**：代码距离、工具序列、Agent 交互边、资源增量和语义状态彼此割裂。
2. **非确定性复现困难**：同一个 prompt 不一定重现同一轨迹，需要统计 oracle、模型响应缓存或确定性环境。
3. **正常长任务与攻击难区分**：尤其是资源和循环测试，需要任务进度感知的 oracle。
4. **跨层 fuzzing 不足**：目前往往只变异 prompt、工具返回或环境中的一层，缺少联合变异。
5. **安全之外的功能测试仍少**：FLARE 是重要例外；规划质量、记忆状态、恢复性和权限边界仍可进一步引入 Fuzzing。

## 7. 最值得复用的设计模板

如果要为自己的 Agent 构建 Fuzzer，可以组合上述论文：

```text
AgentFuzz：代码/sink 距离
    +
VeriGrey：工具调用序列覆盖
    +
FLARE：Agent 内/Agent 间交互覆盖
    +
AgentDoS：资源和跨轮状态反馈
    +
ChainFuzzer：跨工具 source-to-sink oracle
```

最终形成多目标反馈：

\[
F(x)=
\alpha C_{\text{code}}+
\beta C_{\text{tool-seq}}+
\gamma C_{\text{agent-edge}}+
\delta P_{\text{resource}}+
\epsilon R_{\text{risk}}
\]

其中 \(x\) 是自然语言、环境内容和历史状态组成的测试输入。实际研究中不应简单手调权重，而应评估各反馈信号的独立贡献、相关性和单位 token 收益。

