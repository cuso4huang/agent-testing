# AI 智能体评测与测试：2026-08-13 增量更新与主流方法图谱

> 本文是 `agent-testing-review.md` 的增量更新。检索截止 2026-08-13（Asia/Shanghai）。原综述的 40 篇核心语料保持不变；本文把新近正式论文和高相关预印本单独列出，避免把不同证据等级混为一谈。

## 1. 范围与检索策略

- 研究对象：基于 LLM 的工具调用、Web/GUI、代码、具身及多智能体系统；同时纳入 agent framework/harness 的测试。
- 时间范围：重点检查 2026-01-01 至 2026-08-13，并回接原综述中的 2023–2025 奠基工作。
- 文献类型：同行评审论文优先；对直接提出新测试方法的 arXiv 预印本保留观察记录。
- 数据源：Semantic Scholar/学术搜索用于发现，arXiv 用于近期论文及全文，ACL Anthology、NDSS、USENIX 用于正式版本，Crossref 与 OpenAlex 用于元数据交叉核验。
- 检索词族：`LLM agent evaluation`、`agent testing`、`agentic system testing`、`trajectory evaluation`、`agent fuzzing`、`coverage-guided agent testing`、`adaptive red teaming agent`、`agent runtime validation`、`multi-agent testing`、`agent framework testing`、`tool supply-chain security`。
- 纳入标准：被测对象必须是智能体、其执行轨迹或其基础设施；论文需提供明确的 benchmark、oracle、测试生成、覆盖反馈、故障注入、审计或运行时验证方法。
- 排除标准：仅让 agent 帮传统软件生成测试、普通单轮 LLM 评测、无研究方法的产品材料。

## 2. 本轮更新的核心判断

2026 年最明显的变化不是“又多了几个排行榜”，而是**动态、反馈驱动的软件测试方法开始进入智能体系统**：

1. ATA 根据被测 agent 的代码、开发者信息和先前 judge 反馈，自适应地产生更难的 persona/对抗对话；SIRAJ 根据此前执行轨迹迭代构造红队攻击。
2. AgentDoS、VeriGrey 和 FLARE 分别把资源生命周期、工具调用序列、多智能体内部/主体间行为抽象成灰盒反馈或覆盖信号。
3. LogicHunter 把“有效输入生成”和“测试 oracle”一起处理：输入由类型约束与真实用法共同构造，agentic oracle 主动查文档、源码和运行时状态。
4. AgentLens、AgentRewardBench 等工作继续推动从最终 pass/fail 转向轨迹审阅、过程诊断与回归检测。
5. Les Dissonances、MUZZLE、MATE 和 AgentDoS 表明安全测试对象已从 prompt 文本扩大到跨工具控制流、网页注入面、策略约束轨迹与系统资源生命周期。

因此，当前较成熟的实践不是选择某一个万能 benchmark，而是组合：

```text
固定场景回归 + 状态/副作用 oracle + 轨迹断言
             + 多次运行/扰动
             + 覆盖或反馈驱动测试生成
             + 对抗/故障注入
             + 运行时策略与生产回放
```

## 3. 主流方法及代表工作

| 方法类别 | 核心做法 | 最适合回答 | 代表工作 |
|---|---|---|---|
| 任务/环境基准 | 在可重置环境中执行标准任务，检查答案或终态 | “能不能完成任务？” | AgentBench、GAIA、WebArena、OSWorld、SWE-bench、AppWorld、τ-bench |
| 状态与副作用 oracle | 比较数据库/文件/页面的 expected、allowed、forbidden changes | “做对了吗，是否误改别处？” | AppWorld、τ-bench、AgentDojo、SWE-bench |
| 轨迹与过程评测 | 检查里程碑、禁止状态、关键动作偏序、循环、恢复与证据 | “为什么成功/失败，过程是否合规？” | AgentBoard、ToolSandbox、AgentRewardBench、AgentLens、Agent-as-a-Judge |
| 重复、扰动与变形测试 | 多 seed 重跑，释义、改名、布局、工具 schema、时区和故障扰动 | “一次成功是否稳定？” | τ-bench `pass^k`、OSWorld、BrowserGym、AI Agents That Matter |
| 自动/自适应测试生成 | 根据代码、规格、persona 和失败反馈生成并升级测试 | “如何扩大语义与约束覆盖？” | PDoctor、ATA、LogicHunter |
| 覆盖引导/灰盒模糊测试 | 从轨迹或系统状态提取覆盖反馈，定向变异自然语言输入 | “如何主动探索稀有行为？” | AgentDoS、VeriGrey、FLARE |
| 对抗测试与自动红队 | 明确攻击者控制面和目标，基于失败轨迹迭代攻击 | “在适应性攻击下是否仍安全？” | AgentDojo、Adaptive Attacks、SIRAJ、MUZZLE |
| 模拟器与故障注入 | 模拟工具/用户/环境，注入 timeout、空值、恶意输出和状态漂移 | “长尾故障下会怎样？” | ToolEmu、ToolSandbox、Guardrails as Scapegoats |
| 安全扫描与供应链测试 | 扫描工具、skill、跨工具数据流和控制流 | “工具生态会引入什么系统风险？” | Les Dissonances/Chord、InjecAgent、Agent Security Bench |
| 多智能体测试 | 测主体内/主体间覆盖、协作里程碑、通信与失败传播 | “团队为何失效？” | MultiAgentBench、Why Do Multi-Agent LLM Systems Fail?、FLARE |
| 元评测/评测器测试 | 用专家轨迹检验规则与 LLM judge 的 precision/recall/偏差 | “分数本身可信吗？” | AgentRewardBench、Agent-as-a-Judge |
| 运行时验证与可观测性 | trace/span、策略谓词、动作前 allow/block/confirm/review | “部署后如何阻断与追责？” | AgentOps、AgentSpec、MATE、NEXUS、AgentTrust |

### 3.1 哪些已经是主流，哪些仍在形成

- **已成为主流基础设施**：环境化 benchmark、终态检查、任务成功率、完整轨迹记录、多次运行、成本/延迟记录。
- **正在成为主流**：里程碑/禁止事件、效用—安全联合指标、专家校准的 LLM judge、真实环境回放、生产回归。
- **快速上升但证据仍早期**：自然语言输入的覆盖引导 fuzzing、agentic oracle、自动风险组合、长期记忆演化测试、跨工具/skill 供应链扫描。
- **明显不足**：通用变形关系、统计功效与置信区间标准、跨框架统一覆盖语义、长周期状态漂移、线上事故到最小回归用例的自动归约。

## 4. 2026 重点新增证据

| 工作 | 年份/版本 | 方法与贡献 | 证据与核验状态 |
|---|---|---|---|
| Agent-Testing Agent (ATA) | EACL 2026 | 静态代码分析、开发者询问、文献检索、persona 对抗测试与 judge 反馈组成自适应元测试 agent | 本地全文；DOI `10.18653/v1/2026.eacl-long.339`，Crossref/OpenAlex 一致 |
| SIRAJ | Findings of EACL 2026 | 从 agent 定义产生风险种子，再依据历史轨迹迭代攻击；用结构化推理蒸馏降低红队成本 | 本地全文；DOI `10.18653/v1/2026.findings-eacl.171`，Crossref/OpenAlex 一致 |
| Les Dissonances | NDSS 2026 | 定义跨工具 harvesting/polluting 威胁；Chord 动态扫描真实工具的控制流与数据污染风险 | 本地全文；DOI `10.14722/ndss.2026.240577`，Crossref/OpenAlex 一致 |
| AgentDoS | USENIX Security 2026 | 按资源生命周期建模，使用 LLM 生成与功能相关的种子，定向灰盒 fuzz 资源耗尽 | 本地全文；USENIX 正式页面/PDF，未填未经核验 DOI |
| SoK: Attack and Defense Landscape | USENIX Security 2026 | 从系统设计空间、攻击面和防御原则整理 agentic AI 安全 | 本地全文；USENIX 正式页面，出版元数据待进一步结构化核验 |
| A Survey on Evaluation of LLM-based Agents | Findings of ACL 2026 | 从能力、应用 benchmark、通用 agent、benchmark 维度和开发工具五方面整理评测 | 正式摘要/元数据；DOI `10.18653/v1/2026.findings-acl.1330`，Crossref 与 ACL Anthology 核验，OpenAlex 本轮 429 |
| VeriGrey | arXiv:2603.17639 | 以工具调用序列为灰盒反馈，变异注入 prompt，探索低频高风险行为 | 本地 PDF/摘要；arXiv 身份核验，Crossref 无精确记录 |
| FLARE | arXiv:2604.05289 | 从 MAS 源码抽取规格和行为空间，以主体内/主体间覆盖驱动 fuzzing | arXiv 全文/摘要页；出版版本未核验 |
| LogicHunter | arXiv:2607.06195 | 规格感知有效输入生成 + 主动检索文档/源码/状态的 agentic oracle | arXiv 全文/摘要页；出版版本未核验 |
| AgentLens | arXiv:2607.06624 | 正式检查与 LLM 轨迹 review 结合，用于代码 agent 的 nightly regression | arXiv 摘要；出版版本未核验 |
| MUZZLE | USENIX Security 2026 | 根据 Web agent 轨迹寻找高显著注入面并迭代细化上下文攻击 | USENIX 正式摘要；详细实验尚未在本轮全文复核 |
| MATE | USENIX Security 2026 | 将自然语言策略与移动 agent 轨迹共同编码，做策略感知安全审计 | USENIX 正式摘要；详细实验尚未在本轮全文复核 |

## 5. 如何选择方法：一个实用映射

| 你的目标 | 最小推荐组合 |
|---|---|
| 比较不同模型/agent | 固定环境任务 + 状态 oracle + 5–10 次重复 + 成本/延迟 + 置信区间 |
| 做上线前验收 | 业务场景 + 权限/确认/副作用轨迹断言 + 故障注入 + 安全—效用联合报告 |
| 找未知 bug | 规格/代码辅助的测试生成 + 覆盖反馈 fuzzing + 失败归约 + 确定性重放 |
| 测提示注入 | 正常效用基线 + 静态攻击 + 自适应攻击 + 终态泄露/动作 oracle |
| 测多智能体 | 团队终态 + 主体内/主体间覆盖 + 消息/共享状态 trace + 级联失败标注 |
| 测评测器 | 专家标注轨迹 + precision/recall/F1 + 分类型偏差 + 跨 agent/benchmark 外推 |
| 做生产监控 | 标准 trace schema + 版本/成本/延迟 + 策略检查 + 事故轨迹回放成回归用例 |

## 6. 当前冲突、局限与研究空白

1. **成功率的含义不统一。** exact answer、终态、单元测试、LLM judge 和人工偏好不能直接横向比较。
2. **轨迹 oracle 的两难仍未解决。** 固定参考轨迹会拒绝合法替代路径；开放式 LLM judge 又会相信 agent 的自述并产生偏差。当前较稳妥的是状态断言 + DAG/偏序 + 局部语义 judge。
3. **覆盖定义尚未标准化。** VeriGrey 的工具序列、FLARE 的主体间/主体内行为、传统代码覆盖测的是不同空间；高覆盖不自动等于高风险覆盖。
4. **新方法常依赖 LLM 生成器和 LLM oracle。** 测试器与被测系统可能共享模型偏差，需用人工抽检、确定性状态检查和跨模型验证削弱相关误差。
5. **动态环境损害复现性。** 网站、模型别名、工具 API、时区和外部数据会漂移；应保存环境快照、精确版本、完整轨迹和 evaluator 版本。
6. **安全分数不能脱离效用。** 全拒绝可能看似安全；必须联合报告正常任务成功、误阻断、攻击成功和副作用。
7. **长期与生产证据仍少。** 现有研究多是短 episode、合成工具或有限应用；跨周/月记忆污染、权限变更、资源泄漏和组织工作流仍缺标准化测试。

## 7. 结论

主流方法可归纳为三层：第一层用环境 benchmark 和状态 oracle 测“结果”；第二层用轨迹、重复与扰动测“过程和可靠性”；第三层用自适应生成、灰盒 fuzzing、红队与运行时验证主动探索和约束“未知行为”。2026 年最值得继续跟踪的是第三层，但它尚不能替代前两层，因为覆盖反馈和 agentic judge 自身也需要被校准。

对工程实践而言，最稳健的默认方案是：**真实/高保真环境中的状态差分 + 轨迹断言 + 多次重复 + 故障/攻击注入 + 独立校准的 evaluator**。单一成功率或单一 LLM judge 都不足以构成可信的智能体测试体系。

