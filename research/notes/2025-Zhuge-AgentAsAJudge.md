# Agent-as-a-Judge：结构化阅读笔记

## 1. 基本信息

- 标题：*Agent-as-a-Judge: Evaluate Agents with Agents*
- 作者：Mingchen Zhuge；Changsheng Zhao；Dylan R. Ashley；Wenyi Wang；Dmitrii Khizbullin；Yunyang Xiong；Zechun Liu；Ernie Chang；Raghuraman Krishnamoorthi；Yuandong Tian；Yangyang Shi；Vikas Chandra；Jürgen Schmidhuber
- 正式发表年份：2025
- 正式发表：Proceedings of the 42nd International Conference on Machine Learning（ICML 2025），PMLR 267:80569-80611
- DOI：未发现可核验的 ICML/PMLR 正式出版 DOI；arXiv DataCite DOI 为 `10.48550/arXiv.2410.10934`
- arXiv：`2410.10934`，本地全文为 v2
- 正式版本：https://proceedings.mlr.press/v267/zhuge25a.html
- 开放全文：https://arxiv.org/abs/2410.10934
- 代码：https://github.com/metauto-ai/agent-as-a-judge
- 数据集：https://huggingface.co/devai-benchmark
- 版本关系：2024 年 arXiv 预印本后正式发表于 ICML 2025。正式引用应使用 PMLR 会议版本；本项目 PDF 是 `arXiv:2410.10934v2`，正式出版元数据由 PMLR 官方页面核验。本笔记没有假定两个版本逐字相同。

## 2. 研究问题

论文关注长时序、会修改工作区的智能体应如何获得可扩展且有诊断价值的评估。具体问题包括：

1. 只检查最终结果的基准为何难以解释智能体在哪个中间步骤失败？
2. 人工逐项检查完整代码工作区和执行轨迹是否可靠、需要多少成本？
3. 单次 LLM-as-a-Judge 能否评估多文件、带依赖的开发任务？
4. 一个具有搜索、文件读取、定位、轨迹检索和规划能力的“评审智能体”，能否比普通 LLM judge 更接近专家共识？
5. 评审智能体哪些模块真正贡献性能，哪些模块反而会因噪声或历史错误造成级联误判？

作者同时构建 DevAI，以提供包含层级里程碑的完整 AI 开发任务，而不是只用最终 `pass@1` 或单个单元测试作为稀疏奖励。

## 3. 被测试的智能体类型

被评估对象是三个开源代码开发智能体：

- MetaGPT Data Interpreter；
- GPT-Pilot 0.2.13；
- OpenHands CodeAct v1.9。

三者均以 `gpt-4o-2024-05-13` 作为后端，在本地工作区生成代码、数据、图片、报告等产物，并留下开发轨迹。

评估者包括：

- 三名 AI 专家组成的 Human-as-a-Judge；
- 单次提示式 LLM-as-a-Judge；
- 模块化 Agent-as-a-Judge。

论文仅在 AI/ML 软件开发场景验证，没有直接验证 Web、企业业务流程、多智能体协作或具身智能体上的 judge 泛化能力。

## 4. 测试或评估方法

### 4.1 层级需求 oracle

DevAI 将每个任务拆成二元、可逐项判定的 requirements，并用 DAG 表示依赖。论文分别计算：

- 独立 requirements met：忽略前置要求；
- dependency-aware requirements met：只有本项和所有前置项满足才计为满足；
- 完整任务是否全部解决。

Preferences 用于表示更软、较主观的要求，但主结果围绕 365 个硬 requirements。

### 4.2 三种 judge 范式

- **Human-as-a-Judge**：专家访问任务、工作区、轨迹和代码，先独立判断，再讨论形成共识。
- **LLM-as-a-Judge**：把上下文交给单个 LLM 直接判断需求是否满足。
- **Agent-as-a-Judge**：主动构建工作区图、定位文件、读取多模态产物、检索轨迹和代码证据，再由 `ask` 模块做判断。

Agent-as-a-Judge 最初包含八个模块：

1. `graph`：构建文件、模块与依赖图；
2. `locate`：定位要求涉及的目录/文件；
3. `read`：读取代码、图像、视频和文档等 33 类格式；
4. `search`：搜索相关代码片段和隐式依赖；
5. `retrieve`：从长轨迹中检索证据；
6. `ask`：基于证据判定 requirement；
7. `memory`：保存历史判断；
8. `planning`：决定下一步评审动作。

消融后最佳组合为 `graph + locate + read + retrieve + ask`。作者发现 memory、planning 和 search 并非越多越好：历史误判可污染后续要求，动态规划可能收集互相矛盾的证据，小型工作区也不需要复杂代码搜索（Section 4.1；Appendix K）。

### 4.3 黑盒与灰盒

- black-box judge 不使用人工整理的开发轨迹，主要检查最终工作区；
- gray-box judge额外接收人工收集/整理的 trajectory。

论文明确说明，gray-box 所需的精细人工轨迹在实际应用中往往难以获得，因此 black-box 更接近可部署设置。

## 5. 数据集、环境或基准

DevAI 包含：

- 55 个完整 AI 应用开发任务；
- 365 个层级 requirements；
- 125 个 preferences；
- 任务领域包括监督学习、强化学习、计算机视觉、自然语言处理和生成模型等；
- 每个 requirement 是开发过程中的一个 milestone，依赖关系构成 DAG；
- 任务还带有是否需要训练、Web 导航、Kaggle API 等辅助标签。

任务由专家人工编写，两轮人工复核用于检查查询与 requirements 的逻辑一致性、语言歧义和领域适用性。Appendix E 承认复核过程中发现过中等数量的错误。任务规模有意控制得较小，以降低运行三个开发智能体和多种 judge 的成本。

每个开发智能体拥有本地工作区，允许保存代码、模型、图像、指标和 HTML 报告。部分任务需要 Kaggle 凭据；论文通过运行时放置 `kaggle.json` 支持自动化。

## 6. 评价指标

- Requirements Met (I)：忽略依赖的单项要求满足率；
- Requirements Met (D)：考虑依赖 DAG 的要求满足率；
- Self-Termination：智能体是否自行结束而非超时停止；
- Task Solve Rate：所有要求均满足的任务比例；
- Judge Shift：AI judge 与人类共识需求满足率之间的绝对偏移；
- Alignment Rate：365 个 requirement 判定中与人类共识相同的比例；
- Precision-Recall curve：处理“满足要求”远少于“不满足”的类别不平衡；
- 人类评审者之间的 disagreement/mismatch；
- 开发智能体平均成本、时间、输入/输出 token 和生成文件统计；
- judge 的总 API 成本和墙钟时间。

论文自己提醒：Judge Shift 和 Alignment Rate 会被负类占多数抬高。例如一个总判“不满足”的 judge 也可能取得较高 alignment，因此 PR 曲线比单一准确率更可信（Section 4.2）。

## 7. 实验设计

### 7.1 生成被评估工作区

- 三个开发智能体分别运行全部 55 个 DevAI 任务；
- 后端模型统一为 `gpt-4o-2024-05-13`；
- 每个任务最多运行 1,800 秒；
- 通过自定义 instrumentation 保存工作区、动作、决定和环境反馈，形成 trajectory；
- 一次完整 DevAI 运行平均每个开发智能体约需 210.65 美元、14 小时（Section 2.3）。

### 7.2 人工评审

- 三名作者团队内的 AI 专家先独立评审；
- 第一轮三人分别用时 16.5、19.5 和 22.0 小时，共 58 小时；
- 第二轮共同讨论 9.5 小时，折合 28.5 人时；
- 总计 86.5 人时，最终 consensus 作为 AI judge 对齐目标；
- 评审者第一轮只得到评分卡和较少统一规则，以保留现实中的个人判断差异（Section 3；Appendix H）。

### 7.3 AI judge 对比和消融

- 对三个开发智能体分别运行 LLM-as-a-Judge 与 Agent-as-a-Judge；
- 比较 black-box 与 gray-box；
- 在 OpenHands 上逐步加入 `ask`、`graph`、`read`、`locate`、`retrieve` 做模块消融；
- Appendix K 进一步比较 BM25、Sentence-BERT、fuzzy search、轨迹截断和额外模块。

论文正文清楚报告了开发智能体后端模型，但本次全文检查未找到原实验中 Agent-as-a-Judge/LLM-as-a-Judge 所用 judge 模型快照及采样参数的同等明确说明。当前代码仓库已改为通过 LiteLLM 配置多种模型；严格复现需要锁定论文实验对应的仓库提交和 `.env` 配置。

## 8. 主要发现

### 8.1 DevAI 对当时开发智能体仍很难

Human-as-a-Judge 共识结果显示：

| 智能体 | Requirements Met (I) | Requirements Met (D) | Task Solve Rate |
|---|---:|---:|---:|
| MetaGPT | 22.13% | 6.55% | 0.00% |
| GPT-Pilot | 44.80% | 28.96% | 1.81% |
| OpenHands | 42.89% | 28.68% | 1.81% |

数据来自 Table 2。GPT-Pilot 和 OpenHands 各只完整解决 1/55 个任务；考虑前置依赖后，要求满足率明显下降，说明独立子目标得分会高估完整工作流能力。

### 8.2 单个人类也不是可靠金标准

- 三名评审者两两 disagreement 约为 10%-30%（Figure 4）。
- 个别评审者在 GPT-Pilot 上与最终共识的 mismatch 达到 23.77%。
- 三人第一轮多数投票与最终讨论共识之间仍约有 6.01% mismatch（Figure 5）。

因此论文把 consensus 作为“更接近潜在真值”的代理，而不是绝对 ground truth。专家可能共同遗漏同一 bug，也可能在讨论中形成共同偏差；所有 AI judge 指标都应理解为“与该共识对齐”，不能写成客观正确率。

### 8.3 Agent-as-a-Judge 普遍优于单轮 LLM judge，但远非无误

Table 3 的实际数值为：

- black-box Agent-as-a-Judge alignment：MetaGPT 88.52%、GPT-Pilot 83.88%、OpenHands 90.44%；
- black-box LLM-as-a-Judge：84.15%、65.30%、60.38%；
- gray-box Agent-as-a-Judge：92.07%、86.61%、90.16%；
- gray-box LLM-as-a-Judge：68.86%、71.85%、70.76%；
- 人工多数投票与讨论共识：95.08%、93.98%、94.26%。

这些结果支持“主动检查工作区和证据优于把所有上下文一次交给 LLM”，但也显示 Agent-as-a-Judge 与最终共识仍有约 8%-16% 的判定不一致。gray-box 也不是对所有对象和 judge 都单调变好：例如 OpenHands 的 Agent-as-a-Judge 从 black-box 90.44% 轻微降至 gray-box 90.16%，MetaGPT 的 LLM judge 则从 84.15% 降至 68.86%。因此不能简单概括为“加入轨迹必然提升评审”。

### 8.4 模块增多会引入评审级联失败

在 OpenHands 消融中：

- 仅 `ask`：65.03% alignment；
- 加 `graph`：75.95%；
- 加 `read`：82.24%；
- 加 `locate`：90.44%；
- 再加 `retrieve`：90.16%（Table 4）。

作者明确观察到 memory 会让先前 requirement 的误判影响后续判断；planning 可能因不稳定动作收集到冲突证据；search 的额外片段会向小工作区加入噪声。Appendix K 中 Sentence-BERT search 为 87.70%，仍低于不使用 search 的 90.44%。这说明评审智能体自身也需要隔离测试、消融和错误传播分析。

### 8.5 成本优势明显，但论文中的百分比标签有算术互换

- Human-as-a-Judge：86.5 人时；按作者假设的 15 美元/小时计为 1,297.50 美元；
- Agent-as-a-Judge：30.58 美元、118.43 分钟；
- LLM-as-a-Judge：29.63 美元、10.99 分钟（Section 4.4）。

按原始数值重新计算，Agent-as-a-Judge 时间约为人工的 2.29%，成本约为人工的 2.36%，即节省约 97.72% 时间和 97.64% 成本。Section 4.4 把“2.29% of cost”和“2.36% of time”的标签写反了，而 Introduction 的“节省 97.72% 时间、97.64% 成本”与原始数值一致。综述引用时应使用原始数值和重新计算结果，不应复制互换后的标签。

## 9. 局限性

- DevAI 只有 55 个、且仅限 AI 软件开发任务；结论不能直接外推到浏览器、企业工作流、具身或多智能体评测。
- 任务和 requirements 由作者人工设计，规模较小、结构明确，可能偏向 Agent-as-a-Judge 的文件图和里程碑工作流。
- 三名人工评审者均来自作者团队，人数少且第一轮规则有意保持宽松；讨论共识不是独立外部金标准。
- 人工共识仍可能包含共同错误，论文也明确承认 consensus 不等于 absolute ground truth。
- “满足 requirement”为少数类，单一 alignment/accuracy 会掩盖精确率和召回率；论文展示 PR curve，但主表仍大量使用 alignment。
- gray-box 依赖人工整理轨迹，论文称实际中几乎难以获得；对不同 agent 的轨迹 instrumentation 也可能不等价。
- Agent-as-a-Judge 对噪声敏感，memory、planning、search 和错误证据可能导致级联误判。
- 当前工作区只有数百行代码，尚未证明 search/graph 在大型真实仓库中的效果和成本。
- judge 所用的确切模型快照、采样参数和重复运行次数在正文中的报告不如被测开发智能体明确，限制独立复现和稳定性分析。
- 经济性比较把 AI 专家人工成本固定为 15 美元/小时，明显是简化假设；没有对专家薪酬、API 价格和评审质量做敏感性分析。
- 本地全文是 arXiv v2；正式 PMLR 版本身份已核验，但本笔记未逐行比较版本修订。

## 10. 可复现性信息

- 代码仓库公开，包含 `agent_as_a_judge/`、benchmark、reports、scripts、Poetry 锁文件和环境变量模板；
- README 给出 Python 3.11、Poetry 安装流程以及 black-box DevAI 运行命令；
- DevAI 数据、requirements、dependencies、preferences 和辅助标签公开于 Hugging Face；
- 论文给出 MetaGPT、GPT-Pilot、OpenHands 版本、统一后端 `gpt-4o-2024-05-13` 和 1,800 秒任务上限；
- Appendix I 给出附加给开发智能体的文件保存/执行约束，Appendix J 给出 gray-box trajectory JSON schema；
- Appendix H 报告人类评审流程和每位评审者用时；
- 代码仓库当前使用 LiteLLM，支持多种 judge 模型，但复现实验应锁定论文时期 commit、模型端点、提示词、API 定价和轨迹抽取脚本；
- 论文没有充分报告所有 judge 的随机种子、温度、重复运行和置信区间，复现时应新增这些记录。

## 11. 与“智能体测试”研究的关系

论文证明，智能体测试的 oracle 不应只看最终输出，而应检查：

- 层级 requirements 和前置依赖；
- 实际工作区、代码、图像、报告等环境产物；
- 执行轨迹中的错误、未完成步骤和虚假自述；
- 完整任务、单项里程碑与副作用之间的关系；
- judge 自己的证据检索和错误传播。

它也展示了“测试器也必须被测试”：人类、LLM judge 和 agent judge 都会出错；评审器应通过专家标注、消融、类别不平衡指标和重复运行进行校准。

## 12. 可借鉴的工程实现

1. 将用户需求拆成二元 milestone，并显式记录 DAG 依赖。
2. 同时计算独立子目标成功率和 dependency-aware 成功率，避免部分完成掩盖前置失败。
3. judge 先定位并读取最小必要证据，再判断，避免把全部轨迹一次塞入上下文。
4. 每个判断输出 requirement、证据文件、代码行、轨迹片段、置信度和失败原因，支持人工审计。
5. 对 judge 的 graph/read/locate/retrieve/memory/planning 模块做逐项消融。
6. 建立 judge 校准集，报告 precision、recall、PR-AUC、校准误差和按失败类型的混淆矩阵，而不只 alignment。
7. 防止 memory 将早期误判传播到后续 requirement；可使用每项独立上下文或显式证据失效机制。
8. 对 black-box 和 trajectory-enhanced judge 分开报告成本与效果，测量轨迹缺失、截断和噪声注入下的鲁棒性。
9. 人工金标准至少保留独立判断、分歧、讨论记录和最终决策理由。

## 13. 证据等级和全文访问情况

- 证据等级：**已阅读全文**。
- 全文来源：本地 PDF `research/papers/2025-Zhuge-AgentAsAJudge.pdf` 与 arXiv 解析全文 `.codex-data/arxiv-papers/2410.10934.md`。
- 本地 PDF 身份：`arXiv:2410.10934v2`；ICML 2025/PMLR 267 正式出版身份由 PMLR 官方页面核验。
- 阅读范围：正文、DevAI 构建、三类 judge 实验、成本分析、人工评审 Appendix H、轨迹格式 Appendix J、模块和检索消融 Appendix K。
- Table 3 另通过渲染 PDF 原页核对 black-box/gray-box 图标和数值。

## 14. 可以支持综述中的结论

- 最终成功率无法提供长时序智能体需要的过程诊断信号；
- 层级 milestone 和依赖 DAG 能把“部分完成”与“完整任务成功”分开；
- Agent-as-a-Judge 可显著优于单轮 LLM judge，但不能被当作无误金标准；
- 人类单人评审同样存在高分歧，专家共识只是更强代理真值；
- judge 的 memory、planning 和检索会引入噪声与级联误判；
- 轨迹并非信息越多越好，必须测试截断、噪声和可观察性；
- 类别不平衡时 alignment/accuracy 可能误导，应使用 PR 指标；
- 智能体测试工具链需要把 evaluator 本身纳入回归、消融和成本测试。
