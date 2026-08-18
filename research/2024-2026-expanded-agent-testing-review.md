# 2024–2026 智能体测试与测评：扩展证据综述

> 检索截止 2026-08-13。范围是直接测试、测评或保障 LLM 智能体、轨迹、harness 与运行基础设施的研究；2024 年仅保留奠基性或方法价值较高的工作。

## 证据范围

证据库共 85 篇，其中 80 篇发表于 2024–2026，60 篇发表于 2025–2026；另保留 5 篇可迁移的早期基础工作。45 篇有全文证据，40 篇为摘要级证据；73 篇纳入综合，12 篇列为观察项。本轮新增 21 篇结构化全文笔记。

检索覆盖 Semantic Scholar、OpenAlex、Crossref、arXiv、ACL Anthology、ACM、IEEE、USENIX、NDSS、OpenReview 与 Springer。综述用于发现和分类，方法及实验结论回溯到原始论文；DOI、ACL Anthology、arXiv 和出版方页面用于交叉核验，预印本和正式版本合并记录。

## 八类主流方法

| 方法线 | 能发现的主要故障 | 2024 奠基代表 | 2025 主流代表 | 2026 最新代表 | 开放代表 | 主要局限 |
|---|---|---|---|---|---|---|
| 环境化 benchmark、状态/副作用 oracle | 任务失败、非法状态变化、错误工具副作用 | OSWorld、AppWorld、ToolSandbox、τ-bench | SWE-bench Verified 及环境复现工作 | Gaia2 | OSWorld、AppWorld、ToolSandbox、τ-bench | 环境昂贵；状态 oracle 可能漏掉语义等价路径 |
| 轨迹、过程奖励、evaluator 元评测 | 中间步骤错误、错误归因、judge 偏差 | AgentBoard、ToolSandbox | AgentRewardBench、AJBench | Process Evaluation、Counsel、AgentLens | AgentLens、Process Evaluation | 位置偏差、自述诱导、长轨迹丢失、同源误差 |
| 重复可靠性、扰动、变形与长时执行 | 偶发成功、尾部失败、语言/环境脆弱性、漂移 | τ-bench | repeated trials 与版本漂移评测 | ReliabilityBench、Beyond pass@1、Gaia2 | ReliabilityBench | 需要大量重复，成本高；扰动有效性需人工核验 |
| fuzzing、覆盖引导、故障注入、测试生成 | 边界状态、资源耗尽、隐藏逻辑和恢复缺陷 | PDoctor | 反馈/覆盖引导雏形 | ATA、AgentDoS、VeriGrey、FLARE、LogicHunter | VeriGrey、FLARE、LogicHunter | 覆盖定义不统一，失败最小化不足 |
| 记忆、状态漂移、多 session | 遗忘、错误更新、记忆污染、跨会话不一致 | LongMemEval | MemoryAgentBench | Mem2ActBench、LongMemEvalV2 | LongMemEval、MemoryAgentBench | 常只测回忆，外部状态与行动耦合仍弱 |
| 多智能体协作、通信、级联失败 | 协调失败、消息污染、角色错误和级联 | MultiAgentBench、失败分类工作 | CollabOvercooked、LLM Coordination | SILO Bench、ETOM、MASEval | CollabOvercooked、SILO Bench | 团队总分掩盖局部错误，因果归因困难 |
| 安全红队、权限、工具/MCP/skill 供应链 | 注入、越权、有害行动、跨工具传播 | AgentDojo、AgentHarm | 自适应红队与工具安全评测 | SIRAJ、MUZZLE、Les Dissonances、MATE、MAGPIE、SafeAudit | AgentDojo、AgentHarm、SIRAJ | 功能—安全权衡和组合权限空间难覆盖 |
| runtime verification、observability、生产回放、治理 | 线上策略违规、trace 缺失、升级回归 | AgentOps、AgentSpec | 生产 trace 与安全策略框架 | MATE、NEXUS、AgentTrust、AgentLens | AgentOps/AgentSpec、AgentLens | schema 不统一，隐私、延迟和历史回放失真 |

## 方法综合

### 软件测试方法的迁移

单元测试对应工具契约和确定性节点；集成测试对应 agent—工具—状态链；属性/变形测试对应语义等价输入与关系 oracle；fuzzing 对应提示、工具返回和环境状态变异；混沌工程对应超时、限流、部分成功与 schema 漂移；回归测试对应固定 trace 回放和版本差异。迁移到 agent 后必须增加概率重复、语义 oracle、非幂等副作用和长期状态四个维度。

### evaluator/LLM judge 的可信度

judge 不能自动视为金标准。高可信流程至少包括：与人工标签的一致性、对顺序和措辞扰动的稳定性、抗 agent 自述诱导、置信度校准、跨 judge 复核，以及确定性规则对关键安全约束兜底。过程分数必须能回溯到具体步骤和外部状态证据。

### 长期状态与多智能体

两者的共同难点是错误会潜伏、传播并在远期显现。测试应记录状态版本、记忆来源、消息因果边、角色权限和恢复动作；指标应从最终成功率扩展到污染半径、错误生存期、归因准确率和恢复成本。

### 生产验证与运行时保障

建议采用四层闭环：离线可执行 benchmark；预发布故障注入与安全红队；线上结构化 trace 与策略监控；匿名化生产回放和版本门禁。自动阻断规则必须评估误报，并保留审计和人工升级路径。

## 可形成论文或毕业设计的研究空白

1. 跨 agent 框架统一故障注入协议与可靠性曲线。
2. 结合状态差分、约束规则和校准 judge 的混合轨迹 oracle。
3. MCP/skill 供应链的版本、权限与恶意工具组合测试。
4. 多 session 记忆污染的生成、最小化与因果定位。
5. 多智能体级联失败的消息级覆盖和故障归因。
6. 面向模型升级的隐私保护生产 trace 回放与回归门禁。

## 证据限制与实践建议

2026 年仍有较多预印本，正式状态可能变化；部分出版页面仅能核验元数据或全文受限。摘要级记录不用于支撑精细实验结论，元数据冲突、仅摘要及全文不可访问项均在证据表单独标记。

新测试系统的最小组合应包括：可复现环境、状态差分 oracle、至少 5 次随机重复、工具/状态转移覆盖、故障注入、结构化轨迹、关键规则的确定性检查，以及经人工校准的过程 judge。报告应同时覆盖功能、安全、成本和可靠性，而非只有单一榜单分数。
