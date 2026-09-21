# AI智能体行为轨迹评测论文阅读清单

检索主题：agent trajectory representation / process evaluation / workflow coverage / anomaly detection / failure attribution / risk traceability

检索日期：2026-09-20

说明：优先收录论文原文、正式出版页面和公开预印本。引用数会因数据库和日期变化，本清单按与研究需求的相关性、方法价值和可复现性排序，而不是单纯按引用数排序。

## 一、建议先读的12篇

如果时间有限，先读下面12篇，基本可以搭出老师要求的研究框架。

| 顺序 | 论文 | 年份/来源 | 对应研究内容 | 先读原因 |
|---|---|---|---|---|
| 1 | [Survey on Evaluation of LLM-based Agents](https://arxiv.org/abs/2503.16416) | 2025，arXiv | （1） | 先建立智能体评测的总体分类：规划、工具、记忆、反思、应用和评测框架 |
| 2 | [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) | 2023，ICLR | （2） | 最基础的 thought–action–observation 轨迹形式 |
| 3 | [ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs](https://arxiv.org/abs/2307.16789) | 2024，ICLR | （2）（3） | 工具、参数、真实响应和多路径搜索的代表性工作 |
| 4 | [Mind2Web: Towards a Generalist Agent for the Web](https://arxiv.org/abs/2306.06070) | 2023，NeurIPS | （2）（6） | 把每一步表示为“目标元素—操作”，并记录DOM、页面快照和执行轨迹 |
| 5 | [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854) | 2024，ICLR | （2）（6） | 用状态、行动、观察和转移构造可执行网页环境，强调最终状态验证 |
| 6 | [TRAJECT-Bench](https://arxiv.org/abs/2510.04550) | 2025/2026，ICLR | （2）（3） | 直接评估工具选择、参数、顺序、并行调用和轨迹满足度 |
| 7 | [AgentProcessBench](https://arxiv.org/abs/2603.14465) | 2026，预印本 | （2）（4）（5） | 逐步标注正确、探索/中性、错误动作，并分析错误传播 |
| 8 | [Testing Agentic Workflows with Structural Coverage Criteria](https://arxiv.org/abs/2605.26521) | 2026，预印本 | （3） | 与“基于行为轨迹覆盖度量的场景生成”最直接相关 |
| 9 | [Detecting Silent Failures in Multi-Agentic AI Trajectories](https://arxiv.org/abs/2511.04032) | 2025，预印本 | （4） | 直接研究循环、漂移、遗漏等轨迹异常，并构造异常轨迹数据集 |
| 10 | [Trajectory Guard](https://arxiv.org/abs/2601.00516) | 2026，预印本 | （4） | 研究序列感知的实时异常检测，适合参考模型设计和在线检测 |
| 11 | [AgentTrace: Causal Graph Tracing for Root Cause Analysis](https://arxiv.org/abs/2603.14688) | 2026，预印本/工作坊版本 | （5） | 把执行日志重建为因果图，反向定位根因事件 |
| 12 | [A Survey for LLM Agent Trajectory Analysis](https://doi.org/10.1109/TSE.2026.3717765) | 2026，IEEE TSE | （1）（4）（5） | 直接覆盖失败归因、监测、增强、数据集和基准，是写综述和研究空白的入口 |

## 二、按老师六项需求分类

### （1）国内外AI智能体行为轨迹评测技术发展现状

必读：

1. [Survey on Evaluation of LLM-based Agents](https://arxiv.org/abs/2503.16416)：评测对象、基准和评测框架的总体分类。
2. [Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/abs/2507.21504)：从“评测目标”和“评测过程”两个维度组织智能体评测。
3. [基于大型语言模型的AI智能体评估的演化视角](https://arxiv.org/abs/2506.11102)：关注环境、智能体、评估者和指标的演化，可作为国内研究团队相关综述入口。
4. [Large Language Model Agent: A Survey on Methodology, Applications and Challenges](https://arxiv.org/abs/2503.21460)：适合补充智能体架构、协作、工具和应用场景。
5. [A Survey for LLM Agent Trajectory Analysis](https://doi.org/10.1109/TSE.2026.3717765)：重点看轨迹失败归因与评测缺口。

国内标准和行业材料也要看，但不要把它们与论文混为一类：

- [工信部智能体标准方向](https://www.miit.gov.cn/cms_files/filemanager/1226211233/attach/202311/7240bd43f3fc4b598351f9b135e68e4a.pdf)
- [具身智能基准测试方法](https://std.samr.gov.cn/hb/search/stdHBDetailed?id=549C0BA44F7D1569E06397BE0A0A62F3)
- [人工智能预训练模型评测指标相关国家标准草案](https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2023003159%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F20_WD_2023003159_%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD+%E9%A2%84%E8%AE%AD%E6%A8%A1%E5%9E%8B+%E7%AC%AC2%E9%83%A8%E5%88%86%EF%BC%9A%E8%AF%84%E6%B5%8B%E6%8C%87%E6%A0%87.pdf)

### （2）任务执行行为轨迹表征与评测指标

重点看这些论文如何记录一次行为事件：

| 论文 | 关键表征 | 对你的启发 |
|---|---|---|
| [ReAct](https://arxiv.org/abs/2210.03629) | thought、action、observation | 建立最小轨迹单元 |
| [Toolformer](https://proceedings.neurips.cc/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html) | API调用、参数、返回结果 | 工具调用的结构化序列 |
| [ToolLLM](https://arxiv.org/abs/2307.16789) | Thought、API Name、Parameters、Observation | 工具使用过程和失败分支 |
| [AgentBench](https://arxiv.org/abs/2308.03688) | 多环境、多轮交互轨迹 | 跨任务和跨环境评测 |
| [Mind2Web](https://arxiv.org/abs/2306.06070) | 目标元素、操作、页面状态 | 状态依赖的动作表示 |
| [WebArena](https://arxiv.org/abs/2307.13854) | (S,A,O,T) 环境模型 | 不用单一路径匹配，而用环境结果验证 |
| [AgentTuning](https://aclanthology.org/2024.findings-acl.181/) | 多轮交互、思考、行动、反馈、任务奖励 | 如何构造训练/评测轨迹数据 |
| [ACON](https://arxiv.org/abs/2510.00615) | 历史压缩、状态、因果关系、决策线索 | 长轨迹压缩时哪些信息不能丢 |

建议重点比较五种表示：线性事件序列、类型化工具调用、状态差分、依赖/分支图、语义经验摘要。

### （3）基于行为轨迹覆盖度量的评测场景生成

这是当前最接近你老师第三项要求的论文组：

1. [Testing Agentic Workflows with Structural Coverage Criteria](https://arxiv.org/abs/2605.26521) —— 将多智能体工作流表示为类型化协调图，并对可达智能体、工具边、受限工具边和委派边定义覆盖义务，再生成测试场景。
2. [TRAJECT-Bench](https://arxiv.org/abs/2510.04550) —— 生成并行工具调用和有依赖的顺序工具链，适合参考“行为宽度/深度”覆盖。
3. [PlanBench](https://arxiv.org/abs/2206.10498) —— 用自动规划领域生成计划测试任务，适合借鉴状态、动作和目标状态覆盖。
4. [Agent Alpha](https://arxiv.org/abs/2602.02995) —— 用树搜索统一生成、探索和评估计算机使用轨迹，适合借鉴轨迹搜索和分支探索。
5. [Synthetic Scenario Generation for Evaluation of Industry 4.0 Agents](https://arxiv.org/abs/2607.22563) —— 面向工业智能体的证据约束、覆盖预算、混合验证和去重，和复杂工作流场景生成非常接近。
6. [ScenarioNet](https://arxiv.org/abs/2306.12241) —— 虽然主要面向自动驾驶场景，但对场景覆盖、难度和生成式评测有方法借鉴价值。

你需要从这些论文中抽象出自己的“行为覆盖矩阵”：任务、工具、参数、状态、转移、故障、恢复、安全和跨智能体协作。

### （4）基于行为指纹的质量判定与异常识别

这一方向的直接文献还不多，不能只搜索“behavior fingerprint”这个词。建议组合阅读：

1. [Detecting Silent Failures in Multi-Agentic AI Trajectories](https://arxiv.org/abs/2511.04032) —— 轨迹级异常、循环、漂移和遗漏。
2. [Trajectory Guard](https://arxiv.org/abs/2601.00516) —— 用序列自编码器和对比目标检测错误计划与结构异常。
3. [AgentProcessBench](https://arxiv.org/abs/2603.14465) —— 逐步过程质量和错误传播。
4. [Plan-RewardBench](https://aclanthology.org/2026.acl-long.1062/) —— 使用偏好轨迹、干扰轨迹和困难负样本训练计划/轨迹奖励模型。
5. [ToolPRMBench](https://aclanthology.org/2026.findings-acl.602/) —— 将工具轨迹转化为逐步过程奖励测试样例。
6. [AgentTrace: A Structured Logging Framework](https://arxiv.org/abs/2602.10133) —— 从运行时观测、认知过程和上下文三层采集结构化日志。

此外，[Trajectory Behavioral Fingerprinting](https://github.com/pranilraichura/colm-agent-eval) 是一个工程实践型项目，可参考其行为一致性、漂移和行为稳定性分析，但不建议把它作为核心学术证据。

建议你的指纹至少包括：工具序列、参数模式、状态转移、分支/循环结构、恢复模式、成本/延迟、风险动作和语义表示。

### （5）复杂工作流异常轨迹溯源与风险评测

重点阅读：

1. [AgentTrace: Causal Graph Tracing for Root Cause Analysis](https://arxiv.org/abs/2603.14688) —— 从顺序边、通信边和数据依赖边构建因果图，并从最终错误反向追踪根因。
2. [AgentTrace: A Structured Logging Framework](https://arxiv.org/abs/2602.10133) —— 重点看运行时遥测和可观测性设计。
3. [What Did It Actually Do?](https://arxiv.org/abs/2603.28551) —— 研究计算机使用智能体的权限、触碰资源、持久化副作用和事后审计。
4. [ATBench](https://arxiv.org/abs/2604.02022) —— 轨迹级智能体安全评测，强调长上下文和延迟触发的风险。
5. [AgentProcessBench](https://arxiv.org/abs/2603.14465) —— 研究错误传播和首个错误步骤。
6. [A Survey for LLM Agent Trajectory Analysis](https://doi.org/10.1109/TSE.2026.3717765) —— 用于归纳失败分类、归因方法和监测工具。

这一组论文共同支撑你的技术路线：

```text
运行日志 → 事件依赖图 → 首错定位 → 传播路径 → 影响范围 → 风险等级
```

### （6）典型AI智能体行为轨迹评测案例

建议重点看以下基准如何设计环境、任务、轨迹和结果验证：

| 案例 | 论文/基准 | 适合借鉴的内容 |
|---|---|---|
| 工具/API | [ToolBench/ToolLLM](https://arxiv.org/abs/2307.16789) | 工具池、参数、API响应、工具链 |
| 用户—智能体—工具 | [$τ$-bench](https://arxiv.org/abs/2406.12045) | 多轮对话、业务规则、数据库最终状态、pass^k可靠性 |
| 网页操作 | [Mind2Web](https://arxiv.org/abs/2306.06070)、[WebArena](https://arxiv.org/abs/2307.13854) | DOM、页面状态、多条合法路径、功能正确性 |
| 真实电脑使用 | [OSWorld](https://arxiv.org/abs/2404.07972) | 跨应用工作流、执行式评测和可复现环境 |
| 长程电脑使用 | [OSWorld 2.0](https://arxiv.org/abs/2606.29537) | 长时任务、隐式状态、跨来源推理和安全报告 |
| 多环境智能体 | [AgentBench](https://arxiv.org/abs/2308.03688) | 跨环境、跨任务和多轮交互 |
| 具身智能 | [Voyager](https://arxiv.org/abs/2305.16291) | 状态快照、技能库和可复用行为 |

## 三、推荐阅读顺序

### 第一周：理解轨迹是什么

ReAct → ToolLLM → Mind2Web → WebArena。

目标：能够自己画出一条轨迹的数据结构，并区分观察、行动、状态变化和环境反馈。

### 第二周：理解如何评测过程

AgentBench → TRAJECT-Bench → AgentProcessBench → ToolPRMBench。

目标：掌握工具选择、参数正确性、依赖顺序、逐步标签、错误传播和过程奖励。

### 第三周：理解覆盖和场景生成

PlanBench → Testing Agentic Workflows with Structural Coverage Criteria → Agent Alpha → Synthetic Scenario Generation。

目标：形成自己的行为覆盖矩阵和场景生成算法草案。

### 第四周：理解异常、溯源和风险

Detecting Silent Failures → Trajectory Guard → AgentTrace Causal Graph → ATBench → TSE轨迹分析综述。

目标：形成“指纹—异常—首错—传播—风险”的完整方法链。

## 四、建议你做的阅读笔记模板

每篇论文只回答下面八个问题：

1. 评测对象是什么：单智能体、多智能体、工具调用、网页还是复杂工作流？
2. 一条轨迹由哪些字段构成？
3. 轨迹是线性的、树状的还是图状的？
4. 论文评测最终结果还是中间过程？
5. 使用了哪些指标？哪些指标可以迁移到自己的课题？
6. 是否区分正常、失败、恢复和危险行为？
7. 场景是人工编写、模板生成、变异生成还是搜索生成？
8. 论文留下了什么空白，能否对应老师的六项需求？

## 五、最值得形成的研究空白

建议重点关注这一句：

> 当前研究已经能够记录和评价工具调用轨迹，但还缺少一个贯通“行为单元定义—覆盖度量—场景生成—指纹比较—异常溯源—风险评估”的统一框架。

这句话可以作为你后续开题报告中“现有研究不足”的核心表述。特别是“行为指纹”目前不像工具调用评测那样已经形成成熟的标准术语，因此更适合作为你的综合创新点：把过程质量、行为稳定性、策略风格、风险动作和工作流结构统一编码为可比较的轨迹指纹。
