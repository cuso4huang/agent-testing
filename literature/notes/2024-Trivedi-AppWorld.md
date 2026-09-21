# AppWorld：结构化阅读笔记

## 1. 基本信息

- **标题**：AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents
- **作者**：Harsh Trivedi, Tushar Khot, Mareike Hartmann, Ruskin Manku, Vinty Dong, Edward Li, Shashank Gupta, Ashish Sabharwal, Niranjan Balasubramanian
- **年份**：2024
- **会议或期刊**：Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics, Volume 1: Long Papers（ACL 2024）；Best Resource Paper Award
- **DOI**：10.18653/v1/2024.acl-long.850
- **arXiv ID**：2407.18901
- **正式版本和预印本关系**：本地 arXiv v1 日期为 2024-07-26；ACL Anthology 的正式版本于 2024 年 8 月出版，作者、题名与核心内容一致。引用应优先使用 ACL 正式版本及 DOI。
- **代码/环境**：<https://github.com/stonybrooknlp/appworld>

## 2. 研究问题

AppWorld 研究怎样在无真实副作用、可冻结时间和数据库的环境中测试“交互式编码 agent”完成日常跨应用任务。此类任务不只是顺序调用 1–4 个 API，而需要先读取环境、理解自由文本/结构、根据结果写循环和条件代码、处理错误，再修改多个应用状态。论文还研究如何允许多种正确实现，同时严格发现未请求的 collateral damage。

## 3. 被测试的智能体类型

- 单个 LLM 驱动的 interactive coding agent，在 IPython/Jupyter 风格 shell 中多轮生成并执行 Python。
- 通过直接 Python 函数或 REST 请求操作个人应用 API，覆盖查询、跨应用数据关联和有副作用写操作。
- 可调用 ApiDocs 探索文档，并从 Supervisor 获得测试用户的账户信息。
- 不是 GUI agent，也不含多 agent 协作；任务由一个模拟用户交给一个 assistant。

## 4. 测试或评估方法

AppWorld 由 Engine 与 Benchmark 两部分组成（图 2）：

- Engine 提供应用、数据库、冻结时间、状态化执行 shell 和受控 API。
- 每个 Task Scenario 用 `Setup` 从 Base DB 生成 instruction、Task DB、时间和隐藏 expected values，并确保 well-defined、含 distractor/hurdle、与同场景实例组成 contrast set（第 3.1 节、图 3、表 1）。
- `Validation Solution` 是作者编写的端到端可执行解，用于持续验证任务可解与 evaluator 正确，不要求 agent 复现该轨迹（第 3.3 节）。
- `Evaluation` 比较开始/结束数据库差异 `D∆`：所有 expected changes 必须出现，除此之外只允许白名单 `allowed changes`。这同时检测目标完成和非预期修改（第 3.2 节）。

数据库 diff 按表计数器、row hash 和字段比较分层计算；普通 MacBook Pro 上单任务评价平均低于 0.6 秒（附录 D）。

## 5. 数据集、环境或基准

- **Engine**：9 个日常应用，含 Gmail、Venmo、Amazon、Spotify、Todoist、SimpleNote、Splitwise、Phone 和 FileSystem；另有 ApiDocs、Supervisor 两个 helper app。
- 共 **457 个 API、1,470 个参数、101 个数据库表、726 个字段**；约 106 名 19–60 岁虚构用户及其关系/多年活动，Base DB 约 370K rows（第 2 节）。
- API 实现约 26K 行；1,780 个 API unit tests、约 34K 测试代码、98% coverage（第 2.2 节）。
- **Benchmark**：250 个 scenario，每个 3 个 contrastive tasks，共 750。划分 Train 105、Dev 60、Test-N 168、Test-C 417；Test-C 至少使用一个未见应用 Amazon 或 Gmail（第 3.4 节）。
- 表 2：Test-N/Test-C 平均应用数 1.5/2.0，unique APIs 8.2/10.5，API calls 42.5/46.8，solution code lines 41.3/56.9，evaluation tests 5.9/8.0；最大分别可达 3/6 apps、17/26 APIs、244/649 calls、134/128 lines、19/24 tests。
- 约 15% 是只需返回答案的 QA，其余会修改状态。

## 6. 评价指标

- **Task Goal Completion（TGC）**：通过该 task 全部 state-based tests 的任务百分比。
- **Scenario Goal Completion（SGC）**：一个 scenario 的三个 contrast tasks 全部通过才算成功，用于衡量需求/初态变化下的一致性。
- **API Predictor**：F1、precision、recall。
- **难度分层**：按人工 1–3 级、solution code 行数、unique API 数等分析 TGC/SGC。
- **运行成本**：附录 E.8 报告按方法的估计美元成本；主实验未把延迟或 token 作为质量指标。
- 单个 test 失败即整题失败；论文没有单独的 partial progress 或最早失败步骤指标。

## 7. 实验设计

- 六类 agent 方法：ReAct、Plan-and-Execute、FullCode+Reflexion、Iterative Parallel Function Calling、ToolLLaMA、CodeAct（第 4.1 节、附录 E）。
- 前四种分别搭配 GPT-4o、GPT-4 Turbo、Llama-3-70B、DeepSeek-Coder-33B；后两种使用各自 Mistral-7B/LLaMA 专用模型。
- 具体 snapshot：`gpt-4o-2024-05-13`、`gpt-4-turbo-2024-04-09`、`gpt-4-0613`、`meta-llama/Llama-3-70b-chat-hf`、`deepseek-ai/deepseek-coder-33b-instruct`；全部 greedy、temperature=0、top-p=1（附录 E.7）。
- 主提示从三个随机 Train examples 派生；ReAct 因上下文长仅用一个 demonstration。轨迹超过 20,000 字符时保留最近两步环境输出，逐步删除旧 observation/块并标记截断（附录 E）。
- FullCodeRefl 最多五次 retry；IPFunCall 最多 15 turns；ReAct/PlanExec 通过特殊 `task_completed` 或 LLM call 上限停止。
- Oracle API 消融把 validation solution 使用的 API 直接提供给 agent，以区分检索与执行瓶颈。

## 8. 主要发现

1. **当前最强方法仍只完成少数复杂场景。** 表 3 中 GPT-4o+ReAct 的 Test-N TGC/SGC 为 48.8/32.1，Test-C 为 30.2/13.0。TGC 到 SGC 再下降 30%–50%，说明同一意图轻微改变初态/约束后不稳定。
2. **模型差异大于许多 prompting 差异。** GPT-4 Turbo 最佳 TGC 为 Test-N 32.7、Test-C 17.5；最佳开源组合 Llama-3+FullCodeRefl 为 24.4/7.0。ToolLLaMA 与 CodeAct 在全部任务为 0，作者将其归因于专门训练分布过窄。
3. **任务复杂度显著影响结果。** 第 4.3 节/图 4 中 GPT-4o+ReAct 从难度 1 的 TGC 58.3 降到难度 3 的 21.0；需要 60 行以上 validation code 的任务，各方法 TGC 均低于 20。
4. **API retrieval 不是主瓶颈。** GPT-4o API predictor 在 Test-N/Test-C 的 F1 为 87/71；给 oracle API 后最优 ReAct TGC 从 48.8/30.2 提升到 54.8/35.2，仍远未解决任务。FullCodeRefl 的 Test-C 增益最大，为 19.2→29.0（第 4.3 节、附录 F.1）。
5. **更多/更相似示例没有可靠跨分布收益。** 表 5 的 FullCodeRefl 在 Test-N 可提高最多 6.6 TGC，但 Test-C 没有一致提升；demonstration 顺序也产生波动（表 6）。
6. **人工错误分析揭示系统性故障。** 第 4.3 节列出：不与环境交互而 hallucinate 用户数据；虚构参数或响应字段；调用方向相反的 API；只完成 instruction 一部分；混淆常识/日期；忘记已执行动作并重复直至耗尽预算。
7. **状态差分能捕获 collateral damage。** evaluator 不只检查期望新增/更新，还拒绝不在 allowed set 中的任意数据库变化；这比对照参考调用序列更适合多解任务。
8. **成本很高且方法差异明显。** 按 2024-06 定价，GPT-4o 在 Test-N 每例约 ReAct $0.70、PlanExec $1.33、IPFunCall $0.33、FullCodeRefl $0.02；全部实验约 $10K（附录 E.8）。

## 9. 局限性

第 7 节明确指出：

- 仅测试 API 模态；不少应用功能只通过 Web/移动 UI 暴露，尚未测试视觉 grounding。
- 仅有单 supervisor—单 assistant，不含多用户 agent 间协调。
- 为保证高质量，750 题规模不足以训练模型；扩增可能牺牲质量。

其他正文/附录边界：

- 九个模拟应用和约百名虚构用户不能覆盖真实供应商行为、认证、网络波动、隐私政策和文化差异。
- `D∆` oracle 可严格检查数据库副作用，却不检查读取了不应读取的数据、危险中间动作或过程权限；安全 shell 也明确是 best-effort，完整隔离需 gVisor。
- SGC 要求一个 scenario 三题全通过，能测一致性但对三题中任一随机失败很敏感。
- 主实验 temperature=0，未测随机采样稳定性；闭源 API 仍可能服务端漂移。
- Test-C 主要通过未见 Amazon/Gmail 构成分布外挑战，不等于任意新应用。
- 任务和日常数字生活设计主要来自北美/欧洲作者，伦理节承认代表性不足。

## 10. 可复现性信息

- **代码/环境/任务**：公开 Engine、Benchmark、task generators、validation solutions、evaluators 和 Docker/gVisor 配置。
- **确定性状态**：每任务 Task DB 与系统日期时间可重置；本地 serverless SQLite/FastAPI TestClient 加载任务平均低于 0.5 秒（附录 C）。
- **可靠性**：API 有 1,780 个单元测试及 98% coverage；每个 benchmark task 又有 end-to-end gold solution 测试。
- **模型/提示**：具体 checkpoint、temperature、top-p、method prompts 和截断逻辑在附录 E/K 披露。
- **成本**：附录 E.8 报告模型/方法级估算及总成本。
- **缺失项**：未见每题 seed、多次运行置信区间、完整 API 输出缓存和统一硬件/墙钟时间表；闭源模型仍需记录实际调用日期。

## 11. 与“智能体测试”研究的关系

AppWorld 是测试工具型 enterprise/personal workflow agent 的强范例：用数据库不变量验证最终业务状态，用 allowed-diff 白名单检测 collateral damage，用 contrast-set scenario 测同一能力在需求和初态变化下是否稳定。它还把 agent 自己生成/执行代码纳入系统测试，因此同时暴露 API 理解、状态记忆、控制流、错误恢复和指令遵循问题。

## 12. 可借鉴的工程实现

- 将每个场景实现为 `setup + validation solution + evaluator`，并在 CI 中先运行 gold solution。
- 用开始/结束状态 diff 表示修改，分开声明 expected 与 allowed changes；其余一律视为副作用。
- 为同一模板生成三类 contrast cases：首选项存在/不存在、默认凭证有效/过期、干扰记录不同。
- 冻结时间、测试身份和数据库快照；将动态日期表达式纳入 regression。
- 给 API simulator 本身建立高覆盖 unit tests，避免把环境 bug 误判为 agent failure。
- 同时报告 TGC 与“场景全通过率”，并保留单元测试级失败原因。
- 将读取越权、秘密泄漏和危险中间状态加入 evaluator，补齐仅靠最终 DB diff 看不到的风险。

## 13. 证据等级和全文访问情况

- **证据等级：已阅读全文。**
- **全文来源**：本地 PDF `literature/papers/2024-Trivedi-AppWorld.pdf` 与解析文本 `/tmp/agent-review-text/2024-Trivedi-AppWorld.txt`。
- **阅读范围**：正文第 1–8 节、表 1–3、图 1–4；附录 A–K 中的交互要求、数据分布、执行 shell、hash diff、六种方法、消融、成本、API tests、task generator 和 prompts。附录 L 的大规模 API 文档作为环境接口清单检查，不逐条当作实验结论。
- **版本核验**：正式作者、ACL 2024、DOI 和 Best Resource Paper 身份由 ACL Anthology 官方记录核验；实验结论来自全文。
- **访问限制**：无论文访问限制；闭源模型 snapshot 的服务端实现不可完全冻结。

## 14. 可以支持综述中哪些结论

- 状态型工具 agent 应用最终业务不变量和副作用白名单判分，而非参考轨迹匹配。
- 同一 scenario 的 contrast set 可揭示总体成功率掩盖的不稳定性。
- API 检索准确并不意味着 agent 能在长代码、环境反馈和错误处理中完成任务。
- 忘记状态、重复执行、参数/schema 幻觉和部分遵循是交互式编码 agent 的典型故障。
- 可控时间、数据库快照、环境单测和 gold end-to-end solution 是可复现 agent 测试的关键。
- 当前模拟 API 基准仍需扩展到 UI、多智能体、隐私读取和过程安全。
