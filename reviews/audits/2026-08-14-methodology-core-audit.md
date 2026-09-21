# Agent 测试与测评方法学核心库审计与增量更新

## 1. 审计范围与结论

本轮把核心问题收紧为：**如何设计、执行和验证 Agent 测试**。仅提供领域任务和最终成功率的论文不再与测试方法论文并列。

更新后的证据库共 102 篇：`core-method` 42 篇、`supporting-benchmark` 37 篇、`background` 23 篇。相关度分布从原来的 77 篇满分，调整为 5 分 31 篇、4 分 11 篇、3 分 37 篇、2 分 23 篇。核心方法库处于预定的 30–45 篇范围内。

主要问题及处理：

1. **能力 benchmark 与方法混层。** Mind2Web、GAIA、ToolLLM 等降为背景；WebArena、OSWorld 等具有环境/oracle 载体价值的论文降为 supporting benchmark。
2. **相关度通胀。** 相关度现在由 `review_tier` 约束：5 分仅用于以可复用测试方法为主要贡献的工作，4 分用于独特 oracle 或 evaluator 元评测。
3. **2026 与故障归因偏斜。** 不删除最新方法，但核心综合按生命周期组织，并保留 AI Agents That Matter、AgentBoard、AgentDojo、AppWorld、τ-bench 等早期方法学锚点。
4. **状态不一致。** `include` 统一为 `included`，`exclude` 统一为 `excluded`；watchlist 继续表示证据或出版状态未完成，不再承担主题分层功能。
5. **证据等级混淆。** 相关度与全文访问分离；摘要级核心候选仍可进入 `core-method`，但不得支撑详细方法和实验结论。

## 2. 测试生命周期 × 方法证据矩阵

| 生命周期 | 主要问题 | 核心方法证据 | 尚缺证据 |
|---|---|---|---|
| 测试设计 | 如何生成场景、扰动、hard negative 和攻击 | PDoctor、ATA、SIRAJ、FLARE、MUZZLE、Plan-RewardBench | 需求驱动的系统测试设计、真实事故分布校准 |
| 测试执行 | 如何控制环境、注错并确认触发 | AgentDojo、ToolSandbox、AgentChaos、MAS-FIRE、OrchestraBench | 并发、工具状态和跨服务故障的统一执行协议 |
| Oracle/判定 | 如何检查终态、轨迹、约束和评测器 | AppWorld、AgentBoard、AgentRewardBench、AJ-Bench、Process Evaluation、Plan-RewardBench | 可移植的复合 oracle 与 oracle 不确定性传播 |
| 诊断/归因 | 如何定位 Agent、步骤、错误类型和传播路径 | Agentic CLEAR、AgentDiagnose、Who Broke the System、VerifyMAS、REFLECT、StepFinder、TraceElephant | 因果 ground truth、同源 Judge 偏差和多根因表示 |
| 回归/可靠性 | 如何处理随机性、成本和环境变化 | AI Agents That Matter、τ-bench、ReliabilityBench、Beyond pass@1、VeriGrey | 标准置信区间、跨版本差分与 flakiness 预算 |
| 线上监控 | 如何由 telemetry 发现问题并安全重放 | AgentTelemetry、ICST observability/fault injection、AgentDebugX、AgentTrace、Causal Agent Replay | 隐私—可诊断性指标、生产 trace 的公开验证集 |

## 3. 本轮增量论文

| 论文 | 身份与证据 | 分层 | 增量价值 |
|---|---|---|---|
| AJ-Bench | Findings ACL 2026；DOI 双源核验；全文 | core-method / 4 | 主动访问环境的 Judge 元评测；原记录已从未核验 watchlist 升级 |
| Agentic CLEAR | ACL 2026 Demo；DOI 双源核验；全文 | core-method / 5 | system–trace–node 多层诊断和跨轨迹聚合 |
| AgentDiagnose | EMNLP 2025 Demo；DOI 双源核验；全文 | core-method / 5 | 可扩展轨迹质量 evaluator 与状态/语义可视化 |
| Plan-RewardBench | ACL 2026 Long；DOI 双源核验；全文 | core-method / 4 | 用受控 hard negative 压测长轨迹 reward model/Judge |

四篇均已建立结构化全文笔记。AgentDiagnose 的人工验证仅 30 条轨迹；Agentic CLEAR 和其余 Judge 方法仍受 LLM 判定偏差影响，因此它们被纳入方法库，但没有被写成通用金标准。

## 4. 核心方法库的使用方式

- 完整 42 篇清单通过 `literature/evidence/evidence-table.csv` 的 `review_tier=core-method` 过滤得到；每条保留被测对象、方法、指标、数据集、局限和证据等级。
- `supporting-benchmark` 只在需要说明可执行环境、状态 oracle 或具体领域约束时引用。
- `background` 用于历史和领域覆盖，不进入核心方法综合或“最相关论文”排名。
- 重新分层规则保存在 `scripts/research/reclassify_methodology.py`，避免未来增量检索再次依赖宽泛关键词自动升为最高相关度。

## 5. 冲突、限制与研究空白

1. 部分 2026 核心候选仍是摘要或预印本证据；主题相关不等于方法已被充分验证。
2. 直接以 Agent 状态或轨迹覆盖为反馈的灰盒、变形和差分测试仍少，检索结果大量是“用 Agent 测传统软件”，已排除。
3. 多智能体归因论文使用的“首次错误”“责任 Agent”“根因”和“可修复步骤”并非同一标签，不能直接横向合并。
4. 评测器研究仍高度依赖相关模型家族；需要跨家族 Judge、人工盲评、确定性状态 oracle 和 counterfactual replay 的联合验证。
5. 完整 trace 提升诊断能力但可能泄露凭据、PII、文件和推理数据，目前缺少共同的 privacy–diagnosability 曲线。

