# AI 智能体测试与质量保障：检索日志

## 研究范围

- 研究问题：如何系统测试与保障基于大语言模型的自主智能体质量，覆盖单/多智能体、工具调用、Web/浏览器、编程和具身智能体。
- 时间范围：2020-01-01 至 2026-07-23；重点关注 2023 年以后。
- 语言：英文为主，必要时补充可核验的高质量中文研究。
- 文献类型：优先同行评审会议/期刊；保留有明确技术贡献的重要 arXiv 预印本、基准和工程研究。
- 数据源：Semantic Scholar、arXiv；Crossref 与 OpenAlex 用于元数据交叉核验。
- 检索日期：2026-07-23（Asia/Shanghai）。

## 概念边界

本调研把“智能体测试”定义为：对具有目标驱动、多步决策、环境交互、工具调用、状态/记忆维护或多主体协作能力的 AI 系统，实施离线评测、场景/轨迹测试、对抗与安全测试、故障注入、回归测试及线上监控，以评估其功能正确性和可靠性、安全性、稳定性、可复现性、成本与延迟等非功能质量。仅测试无环境行动闭环的普通聊天模型，不属于核心范围；但 LLM-as-a-Judge、提示注入与生成质量研究在直接支撑智能体测试方法时可作为方法学文献纳入。

## 纳入与排除标准

### 纳入

1. 直接研究 LLM/AI agent 或 agentic system 的测试、评估、基准、可靠性或安全性；
2. 针对规划、推理、记忆、工具使用、轨迹、错误恢复、多智能体协作等智能体能力提供可复现实验；
3. 提供 Web、编程、具身、工具调用或企业工作流智能体的环境、数据集、指标或测试框架；
4. 基本元数据可由论文原文、arXiv、Crossref、OpenAlex 或出版方核验。

### 排除或降级

1. 仅评测普通对话/问答模型，和自主行动闭环无直接关系；
2. 无技术方法或实验的产品宣传、博客或观点文章；
3. 基本身份无法核验；
4. 与已纳入正式版本内容重复的旧预印本（保留版本关系但不重复计数）；
5. 仅作宽泛综述且不能为本研究问题提供独立实证证据。

## 初始检索式

以下检索式按数据库语法作必要调整，不声称各数据库支持相同布尔语法。

### 英文核心检索式

1. `"LLM agent" AND (evaluation OR testing OR benchmark)`
2. `("AI agent" OR "agentic system") AND ("software testing" OR reliability OR robustness)`
3. `("tool use" OR "tool-using agent" OR "function calling") AND (evaluation OR benchmark OR testing)`
4. `("web agent" OR "browser agent") AND (benchmark OR evaluation OR safety)`
5. `("coding agent" OR "software engineering agent") AND (benchmark OR evaluation OR testing)`
6. `("multi-agent" OR "multiagent") AND ("LLM" OR "language model") AND (evaluation OR benchmark OR failure)`
7. `("embodied agent" OR "language agent") AND (evaluation OR benchmark) AND LLM`
8. `("agent safety" OR "agent security") AND (benchmark OR evaluation OR testing)`
9. `("prompt injection" OR "indirect prompt injection") AND (agent OR tool)`
10. `("agent trajectory" OR "trajectory evaluation") AND (LLM OR agent)`
11. `("runtime monitoring" OR observability) AND ("LLM agent" OR "agentic system")`
12. `("fault injection" OR fuzzing OR "metamorphic testing" OR "property-based testing") AND ("LLM agent" OR "AI agent")`
13. `("LLM-as-a-judge" OR "language model as a judge") AND (agent OR trajectory OR evaluation)`
14. `("agent benchmark" OR "agent evaluation") AND (cost OR latency OR reproducibility OR stability)`
15. `(loop OR "state drift" OR cascading OR recovery) AND ("LLM agent" OR "agentic workflow") AND evaluation`

### 中文补充检索式

1. `大语言模型 智能体 测试 评测 基准`
2. `AI 智能体 可靠性 鲁棒性 安全测试`
3. `工具调用 智能体 评测`
4. `多智能体 协作 评测 故障`
5. `浏览器智能体 基准 提示注入`
6. `智能体 轨迹评估 故障注入 变形测试`

## 检索与筛选流程

1. 用 Semantic Scholar 宽搜并以高相关种子论文扩展引用、参考文献与相似论文；
2. 用 arXiv 补充近期预印本和可访问全文；
3. 按规范化 DOI、arXiv ID、规范化标题+年份、模糊标题+重叠作者依次去重；
4. 记录预印本、会议、期刊扩展及修订版本关系，引用优先采用正式版本；
5. 使用 Crossref 与 OpenAlex 核验 DOI、作者、年份、venue 和文献类型；
6. 先以题名/摘要筛选，再对高相关文献全文筛选与结构化精读；
7. 所有纳入/排除决定写入 `evidence/screening-log.csv`，所有证据等级写入证据表。

## 执行记录

- 2026-07-23：初始化研究目录、范围、检索式、纳排标准及证据字段。
- 2026-07-23：以 `"LLM agent" evaluation benchmark`、`agent trajectory evaluation`、`tool-use evaluation`、`web agent benchmark`、`coding agent benchmark`、`agent prompt injection safety benchmark`、`multi-agent failure evaluation`、`agent observability fault injection` 为 Semantic Scholar 宽检索入口。服务在并发扩展时多次返回限流；不把未完整返回的排序或引用次数写入证据，改用精确题名检索、arXiv 原始记录和出版方页面补齐。
- 2026-07-23：从 AgentBench、WebArena、ToolLLM、SWE-bench、AgentDojo、ToolEmu、τ-bench、ToolSandbox、AgentBoard 等种子扩展参考文献和相似工作，形成“通用能力—应用环境—安全—测试方法/可观测性”四组候选。
- 2026-07-23：在 arXiv 以精确题名/ID 核验并获取可访问全文，核心 ID 包括 `2308.03688`、`2401.13178`、`2307.13854`、`2404.07972`、`2310.06770`、`2307.16789`、`2406.12045`、`2408.04682`、`2309.15817`、`2406.13352`、`2403.02691`、`2410.09024`、`2412.14470`、`2504.08942`、`2404.17833`、`2411.05285`、`2311.12983`、`2401.13649`、`2412.13178`、`2407.20242`、`2010.03768`、`2203.07540`。
- 2026-07-23：补充安全、稳定性和应用覆盖的 arXiv 记录：`2312.14197`、`2503.00061`、`2410.02644`、`2407.12784`、`2407.20859`、`2503.13657`、`2403.07714`、`2503.01935`、`2412.05467`、`2405.14573`、`2407.18901`、`2306.06070`、`2407.05291`、`2304.08244`、`2306.14898`。
- 2026-07-23：补充方法学种子 `AI Agents That Matter`（`2407.01502`）、`Agent-as-a-Judge`（`2410.10934`）和 `AgentSpec`（`2503.18666`），用于成本/统计不确定性、轨迹评审和运行时策略约束。
- 2026-07-23：用 Crossref/OpenAlex 验证脚本及出版方页面交叉核验标题、作者、年份、venue 和 DOI。若 Crossref 的“最佳模糊匹配”不是同一论文，而 arXiv/OpenAlex/正式页面精确一致，则记录为“Crossref 无精确记录”，不把它误写成元数据冲突。
- 2026-07-23：将已纳入的开放 PDF 下载到 `literature/papers/`，按“正式发表年份优先；若无正式版本则用预印本年份—第一作者—短标题”命名。临时解析文本保留在 `.codex-data/arxiv-papers/` 或 `/tmp`，未复制到最终论文目录。
- 2026-07-23：对核心论文开展全文精读，并同步创建结构化笔记；其余候选只按摘要明确内容进入证据表，详细实验结论不由摘要级证据支撑。
- 2026-07-23：确认项目使用 Git；新增 `.gitignore`，仅忽略 `literature/papers/` 和本地 `.codex-data/` 解析缓存，证据表、筛选日志、笔记、BibTeX、检索日志、综述和研究方向继续由 Git 跟踪。

## 专项检索与筛选补充

### 功能与应用基准

- 通用：AgentBench、AgentBoard、GAIA。
- Web/浏览器：Mind2Web、WebArena、VisualWebArena、WorkArena++、BrowserGym、AndroidWorld。
- 工具/企业工作流：ToolLLM、API-Bank、StableToolBench、ToolSandbox、τ-bench、AppWorld。
- 编程：InterCode、SWE-bench。
- 具身：ALFWorld、ScienceWorld。

### 安全与失效

- 间接提示注入：BIPIA、InjecAgent、AgentDojo、Adaptive Attacks。
- 工具/通用智能体安全：ToolEmu、ASB、Agent-SafetyBench、AgentHarm。
- 记忆与知识库污染：AgentPoison。
- 具身安全：SafeAgentBench、BadRobot。
- 多智能体级联：Why Do Multi-Agent LLM Systems Fail?
- 恶意故障放大：Breaking Agents。

### 评测器、可靠性与运行时方法

- 轨迹和子目标：AgentBoard、ToolSandbox、AgentRewardBench、Agent-as-a-Judge。
- 重复可靠性、成本与统计：τ-bench、AI Agents That Matter。
- 可观测性和运行时约束：AgentOps、AgentSpec。
- 自动测试输入合成：PDoctor（Erroneous Planning）。

## 去重与版本处理

1. arXiv 与正式版本视为同一研究记录，不重复计数；证据表的 `version_status` 写明关系。
2. 正式引用优先采用 ACL Anthology、NeurIPS、ICLR/OpenReview、PMLR 或期刊版本；arXiv URL 保留为全文入口。
3. 目前明确处理的版本关系包括：
   - AgentBench、WebArena、ToolLLM、SWE-bench、ToolEmu：arXiv 后发表于 ICLR 2024；
   - τ-bench、AgentHarm、BadRobot、AndroidWorld：arXiv 后发表于 ICLR 2025；
   - VisualWebArena、AppWorld：正式 ACL 2024；
   - ToolSandbox：正式 Findings of NAACL 2025；
   - AgentDojo、AgentBoard、OSWorld、AgentPoison、WorkArena++：正式 NeurIPS 2024；
   - BIPIA：正式 KDD 2025；
   - Adaptive Attacks：正式 Findings of NAACL 2025；
   - MultiAgentBench：正式 ACL 2025；
   - BrowserGym：正式 TMLR 2025；
   - Breaking Agents：正式 EMNLP 2025；
   - `Agent-SafetyBench` 当前按 2024 arXiv 预印本处理；2026 AAAI workshop 记录不是同一层级的正式主会出版依据；
   - `SafeAgentBench` 当前按 2024 arXiv 版本处理；检索到的 ICLR 2026 评审页不足以证明已正式发表；
   - `AgentOps` 与 PDoctor 当前按 arXiv 预印本处理；
   - `AgentSpec` 已有 ICSE 2026 官方接收线索，但 DOI 尚未从 Crossref/OpenAlex 精确核验，因此暂不填写 DOI。
4. `ToolBench` 是 ToolLLM 工作中的核心基准，不另作为一篇论文重复计数；`SWE-bench Verified` 是数据集子集/修订资源，不作为独立论文重复计数。

## 全文可访问性说明

- arXiv 可访问论文以原始 PDF和解析文本精读；正式出版页用于核验版本身份。
- 闭源 API 模型的旧快照可能已不可调用。即使论文、代码和提示公开，也只能把复现性标为“部分可复现”，不能保证数值级完全复现。
- 对只读取摘要或出版方元数据的候选，证据表会使用“仅阅读摘要”或“仅核验元数据”；这些记录不会支撑论文表格数字、实验过程或作者未在摘要声明的局限性。

## 本阶段结果汇总

- 候选筛选记录：56 条；
- 纳入：40 篇；排除：16 条（含低优先级论文、通用 LLM evaluator、版本/数据集重复和研究边界不符工作）；
- 全文精读：25 篇，均已建立 14 节结构化笔记；
- 摘要级纳入：15 篇；
- 最终论文 PDF：40 份，全部通过 `pdfinfo` 可读性检查；
- 经过核验的 BibTeX：40 条；
- DOI：15 条由出版方记录或 Crossref/OpenAlex 精确身份核验；其余无可核验 DOI 的论文保持为空，不以 arXiv/DataCite 标识冒充正式出版 DOI。

2026-07-23 的批量 DOI 复核中，Crossref 对部分并发请求返回 HTTP 429；同一批记录的 OpenAlex 精确 DOI/题名仍返回，且 ACL Anthology、ICLR/OpenReview、NeurIPS/PMLR 等正式页面已用于补充核验。限流记录被保留，不把“只返回单源”误写成双源成功。

## 下一次更新建议

1. 复查 AgentSpec 的 ICSE 2026 DOI 是否已进入 Crossref/OpenAlex；
2. 跟踪 SafeAgentBench 是否由 under-review 状态变成正式出版；
3. 对 ReliabilityBench、MAS-FIRE、VeriGrey、PrefixGuard、Consistency 等 2026 新预印本做版本审计；
4. 增补 AgentTelemetry、运行时提前预警、MCP/工具供应链和隐私保护 trace 的同行评审证据；
5. 对当前 15 篇摘要级纳入文献按研究问题优先级继续全文精读；
6. 对闭源模型、网站和工具 API 的复现实验记录调用日期与精确版本，避免历史结果被静默更新覆盖。

## 增量检索（2026-08-13）

- 目标：更新 2026 年智能体评测/测试方法，特别检查动态测试生成、灰盒 fuzzing、agentic oracle、轨迹审计与工具供应链。
- 查询词：`LLM agent evaluation 2026`、`agent testing fuzzing 2026`、`coverage-guided agent testing`、`trajectory evaluation benchmark agent`、`adaptive red teaming LLM agent`、`USENIX Security 2026 agentic AI testing`。
- 来源：Semantic Scholar/学术搜索、arXiv、ACL Anthology、NDSS、USENIX Security；Crossref/OpenAlex 用于身份复核。
- 正式新增重点：ATA（EACL 2026）、SIRAJ（Findings EACL 2026）、Les Dissonances（NDSS 2026）、AgentDoS 与 Agentic AI Security SoK（USENIX Security 2026）、Yehudai 等的 agent evaluation survey（Findings ACL 2026）。
- 高相关预印本：VeriGrey（2603.17639）、FLARE（2604.05289）、LogicHunter（2607.06195）、AgentLens（2607.06624）。
- USENIX Security 2026 定向发现：MUZZLE（自适应 Web 注入测试）与 MATE（策略感知移动 agent 轨迹审计）；本轮仅依据正式摘要，不使用摘要之外的细节。
- 核验：ATA、SIRAJ、Les Dissonances 的 DOI 在 Crossref/OpenAlex 完全一致；ACL survey 由 ACL Anthology/Crossref 核验，OpenAlex 请求遇到 HTTP 429；VeriGrey/FLARE/LogicHunter 未获得精确 Crossref 记录，因此保持 arXiv 身份，不把模糊匹配当正式版本。
- 去重：正式版本与对应预印本视为同一工作；本次增量不改变原 40 篇核心语料统计，详情见 `reviews/overview/2026-08-13-agent-testing-update.md`。

## 综述论文专项检索（2026-08-13）

- 研究问题：哪些综述、系统综述和 SoK 能高质量覆盖 LLM 智能体评测、测试、benchmark 与安全验证？哪些提供开放全文和作者配套 GitHub？
- 查询：`survey evaluation LLM-based agents`、`evaluation and benchmarking LLM agents survey`、`systematic review agentic AI evaluation testing validation metrics`、`LLM agent security survey SoK evaluation`、`multi-turn agent evaluation survey`、`computer-using agent safety survey`、`multi-agent LLM evaluation survey`，并对题名定向搜索 GitHub。
- 来源：ACL Anthology、ACM/KDD、Springer、Frontiers of Computer Science、USENIX Security、arXiv、DBLP 与作者 GitHub。
- 核心纳入：Findings ACL 2026 agent evaluation survey、KDD 2025 evaluation/benchmarking survey、FCS 2026 evolutionary evaluation survey、Artificial Intelligence Review 2026 PRISMA review、USENIX Security 2026 agentic security SoK。
- 专题纳入：多轮对话 agent 评测、Computer-Using Agent 安全、长期状态化 agent 安全、多智能体与 OS/GUI agent 综述。
- 降级：主要讨论 agent 架构/应用且只有少量 evaluation 章节的通用 survey；没有透明检索方法或无法核验身份的泛化 arXiv survey。
- 开源判定分为开放 PDF、作者维护的资料库、可执行 benchmark/代码三层，不把免费 PDF 直接写成“开源实现”。
- 结果文件：`reviews/overview/agent-evaluation-surveys-curated.md`。

## 综述全文阅读与反向引用追踪（2026-08-13）

- 全文阅读：Findings ACL 2026 agent evaluation survey（25 页）、KDD 2025 evaluation/benchmarking survey（11 页）、FCS 2026 evolutionary evaluation survey（30 页）、Toward Secure LLM Agents（42 页）及本地 USENIX Security 2026 Agentic AI SoK。
- 抽取主题：task completion/state oracle、stepwise/trajectory evaluation、reference-based/reference-free judge、reliability/pass^k、robustness/fault injection、safety–utility、cost/latency、model–harness disentanglement。
- 原始论文复核：利用本地全文和 `literature/notes/` 检查 AgentBoard、ToolSandbox、AgentRewardBench、τ-bench、AppWorld、AgentDojo、AI Agents That Matter 等方法、指标、局限和开源状态。
- 版本原则：综述只用于分类和发现；具体实验结论回到原始论文。近期预印本与正式同行评审论文分层报告。
- 输出：`reviews/overview/survey-to-primary-agent-testing-map.md`。

## 2024–2026 八条文献线扩展（2026-08-13）

- 时间窗：2024-01-01 至 2026-08-13；2025–2026 全面检索，2024 仅保留奠基性或直接方法价值较高的工作。
- 八组查询：环境/状态 oracle，轨迹与 evaluator，重复可靠性与变形测试，fuzzing/覆盖/故障注入，记忆与多 session，多智能体级联，安全/权限/MCP 供应链，runtime verification/observability/生产回放。
- 来源：Semantic Scholar、arXiv、ACL Anthology、ACM、IEEE、USENIX、NDSS、OpenReview、Springer；Crossref 与 OpenAlex 用于题名、作者、DOI 和版本关系复核。
- 纳排边界：纳入直接测试 agent、轨迹、harness 或 agent 基础设施的研究；排除仅让 agent 测试传统软件以及只有通用能力榜单、没有测试方法贡献的工作。
- 结果：证据库 85 篇，80 篇处于目标时间窗，60 篇为 2025–2026；45 篇全文证据、40 篇摘要证据，73 篇 Included、12 篇 Watchlist。本轮新增 21 篇全文笔记。
- 去重：依次使用 DOI、arXiv ID、规范化题名和作者；正式版本与预印本合并到单条记录，版本关系写入 `version_status` 或备注。
- 证据纪律：摘要级论文只支持题名、研究目标和作者明确陈述的高层结论；方法、实验数值和局限只从全文笔记进入综合报告。
- 异常：Crossref/OpenAlex 部分批量请求出现 HTTP 429；此类记录改用 ACL Anthology、出版方或 arXiv 原始页面核验，并保留单源/未核验状态，不把模糊匹配升级为正式版本。
- 输出：`reviews/overview/2024-2026-expanded-agent-testing-review.md`、`literature/evidence/evidence-table.csv`、`literature/evidence/screening-log.csv`、`literature/notes/` 与 `literature/bibliography/references.bib`。

## 2026 年最新进展补充检索（2026-07-23）

- arXiv 查询式：`("LLM agents" OR "AI agents" OR agentic) AND (evaluation OR benchmark OR testing OR safety OR observability)`；类别 `cs.AI`, `cs.CL`, `cs.MA`, `cs.SE`, `cs.CR`；日期 `2026-01-01` 至 `2026-07-23`；按 relevance 排序，获得 50 条相关结果后按直接相关性筛选。
- 定向查询/核验题名：`Safety Testing LLM Agents at Scale`、`VESTA`、`ATBench`、`MemEvoBench`、`TIDE`、`ClawArena`、`NEXUS`、`AgentTrust`、`Cold-Start Safety Gap`、`Guardrails as Scapegoats`、`Behavioral Consistency`。
- Web/出版方核验重点：arXiv 原始记录、Hugging Face 数据集页、OpenReview 搜索结果；截至本次检索，补充的 12 条均按 2026 arXiv watchlist 处理，没有把仅有预印本的工作写成正式会议/期刊论文。
- 补充结果：新增 12 条 watchlist 记录、12 份 PDF 和 12 条带 `note={2026 watchlist; abstract inspected only}` 的 BibTeX；它们不计入主体综述的 40 篇正式纳入语料，也不支撑全文级实验结论。
- 2026 年专题见 `reviews/overview/2026-latest-update.md`。后续应优先全文核验 Vera、ATBench、MemEvoBench、TIDE 和 ClawArena，再决定是否提升为正式纳入文献。
- 2026 补充的标题核验脚本显示：Vera、ATBench、MemEvoBench、TIDE 的 arXiv 身份明确，但 Crossref 给出不相关的模糊最佳匹配，OpenAlex 批量请求触发 HTTP 429；因此补充文档明确标为“arXiv 身份核验、出版元数据未确认”。

## 测试方法、故障诊断与 MCP 增量检索（2026-08-14）

- 时间窗：2024–2026；重点查找现有 85 篇证据库之外的直接 agent 测试和测评方法。
- 精确查询：`LLM agent testing trajectory oracle fault injection metamorphic testing`；`AI agent runtime monitoring observability reliability evaluation`；`multi agent system evaluation cascading failure fault injection LLM`；`tool using agent benchmark safety permissions MCP evaluation`。
- 来源：新版 `conference_search.py` 汇合 Semantic Scholar、OpenAlex、Crossref、arXiv、DBLP 和开放获取解析；四组各最多 80 条，不限定会议。
- 源异常：Semantic Scholar 三组 HTTP 429；DBLP 四组 SSL EOF。OpenAlex、Crossref、arXiv 仍成功返回，逐请求状态保存在 `tmp/literature-search-20260814/*/results.json`。
- 重点新增：AgentChaos、AgentTelemetry、ICST `llmmas-otel`、OrchestraBench、Who Broke the System、VerifyMAS、POIROT、MCPHunt、MCPEvol-Bench、OSGuard、When the Manual Lies；并发现证据库遗漏的 2025 正式论文 SafeToolBench 与 ToolSafety。
- DOI 核验：AgentTelemetry、ICST observability/fault-injection、When the Manual Lies、SafeToolBench、ToolSafety 均获 Crossref/OpenAlex 精确一致记录；AgentChaos 仅 OpenAlex 返回，暂为部分核验。
- 模糊匹配处置：MCPHunt、OSGuard、POIROT、VerifyMAS 等题名查询命中不相关 Crossref 记录，未采纳为正式 DOI；`10.48550/arXiv...` 不作为同行评审证明。
- 证据等级：本轮为发现、元数据和摘要筛选，尚未宣称阅读全文。增量证据表、综合与精读顺序见 `searches/logs/2026-08-14-agent-testing-incremental-search.md`。

## 测试方法与故障诊断全文增量（2026-08-14）

- 范围：2024–2026；直接测试 Agent、Agent 轨迹、harness 或多智能体基础设施。
- 六组查询：`LLM agent fault injection chaos engineering reliability testing`；`LLM agent coverage guided greybox fuzzing metamorphic testing`；`AI agent test oracle state validation trajectory evaluation`；`LLM multi agent failure localization attribution root cause diagnosis`；`LLM agent runtime monitoring telemetry observability fault detection`；`LLM multi agent cascading failure recovery testing fault propagation`。
- 工具与来源：`conference_search.py --start-year 2024 --end-year 2026 --limit 100 --no-conference-only`；汇合 Semantic Scholar、OpenAlex、Crossref、arXiv、DBLP 与开放获取解析。
- 结果：六组各 100 条，共 600 条原始记录；跨查询合并并扣除原 85 条证据记录后为 502 个题名候选。人工排除传统软件 fuzzing、微服务诊断和“Agent 作为测试工具”的论文。
- 数据源异常：Semantic Scholar 四组 HTTP 429；DBLP 五组 SSL EOF、一组 handshake timeout。请求和错误保存在 `tmp/literature-search-20260814-methods/*/results.json`。
- 全文纳入 9 篇：AgentChaos、OrchestraBench、MAS-FIRE、Who Broke the System、VerifyMAS、AgentDebugX、REFLECT、StepFinder、Seeing the Whole Elephant。
- 观察项：AgentTelemetry、ICST observability/fault-injection、AgentTrace、FALAT、Causal Agent Replay。前两篇 DOI 已核验但未确认合法开放全文；后三篇本轮仅使用摘要。
- 元数据：StepFinder、TraceElephant 获 Crossref/OpenAlex 精确一致核验；AgentChaos 为论文首页+OpenAlex 支持、Crossref 待入库；预印本题名的 Crossref 模糊他文匹配全部拒绝。
- 详细综合：`reviews/overview/2026-08-14-agent-testing-methods-fulltext-review.md`。

## 方法学核心范围收紧与增量复核（2026-08-14）

- 核心问题收紧为“如何设计、执行和验证 Agent 测试”；能力榜单不再自动视为测试方法证据。
- 方法约束查询：`agent AND (test oracle OR state invariant OR executable verifier)`；`agent trajectory AND (meta-evaluation OR judge calibration OR evaluator reliability)`；`agent AND (metamorphic OR differential OR regression OR mutation testing)`；`agent AND (fault injection OR chaos engineering OR counterfactual replay)`；`agent evaluation AND (variance OR confidence interval OR reproducibility OR harness)`；`agent AND (runtime verification OR telemetry OR failure detection)`。
- 来源：Semantic Scholar、OpenAlex、Crossref、arXiv、DBLP，以及 ACL、ICSE、FSE、ASE、ISSTA、ICST、USENIX Security、NDSS 官方页面。既有批量检索中 Semantic Scholar 出现 HTTP 429、DBLP 出现 SSL EOF/timeout，因此本轮对新增正式论文使用 ACL Anthology、Crossref 与 OpenAlex 逐篇核验。
- 分层规则：`core-method`（直接测试方法或独特 oracle/evaluator 元评测）、`supporting-benchmark`（承载独特环境或领域约束）、`background`（能力与历史背景）、`excluded`（被测对象不是 Agent 或不满足证据边界）。相关度 5/4/3/1–2 分别对应上述方法贡献强度。
- 重标结果：证据库 102 篇，其中 core-method 42、supporting-benchmark 37、background 23；相关度为 5 分 31、4 分 11、3 分 37、2 分 23。筛选日志的 `include/exclude` 已统一为 `included/excluded`。
- 正式增量与升级：AJ-Bench（Findings ACL 2026，10.18653/v1/2026.findings-acl.1269）、Agentic CLEAR（ACL 2026 Demo，10.18653/v1/2026.acl-demo.74）、AgentDiagnose（EMNLP 2025 Demo，10.18653/v1/2025.emnlp-demos.15）、Plan-RewardBench（ACL 2026 Long，10.18653/v1/2026.acl-long.1062）。四篇均阅读全文并由 Crossref/OpenAlex 精确核验 DOI 与题名。
- 排除纪律：检索到的 REST API、传统软件和一般 LLM 变形测试论文如果只是“使用 Agent/LLM 生成测试”，不纳入以 Agent 为被测对象的核心库。
- 输出：`reviews/audits/2026-08-14-methodology-core-audit.md`；可复现分层规则：`scripts/research/reclassify_methodology.py`。
