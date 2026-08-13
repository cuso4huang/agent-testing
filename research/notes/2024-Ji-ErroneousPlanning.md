# PDoctor：结构化阅读笔记

## 1. 基本信息

- 标题：*Testing and Understanding Erroneous Planning in LLM Agents through Synthesized User Inputs*
- 作者：Zhenlan Ji；Daoyuan Wu；Pingchuan Ma；Zongjie Li；Shuai Wang
- 年份：2024
- 发表状态：arXiv 预印本；本次核验未发现正式会议或期刊版本
- DOI：无正式出版 DOI；arXiv DataCite DOI 为 `10.48550/arXiv.2404.17833`
- arXiv：`2404.17833`（本地全文为 v1）
- 开放全文：https://arxiv.org/abs/2404.17833
- 论文给出的匿名代码入口：https://anonymous.4open.science/r/PDoctor-E872
- 版本关系：本次只核验到 2024-04-27 提交的 arXiv v1，未发现可确认的正式发表版本。论文中的匿名 4open.science 链接是评审期地址，本次未把它视为永久归档或当前可复现性已得到保证。

## 2. 研究问题

论文关注“错误规划”而非普通最终答案错误，提出三个研究问题：

- RQ1：PDoctor 能否自动生成测试并发现不同 LLM/agent framework 组合的错误规划？
- RQ2：当前 LLM agents 的规划能力随动作数量如何变化，会产生哪些错误类型和触发原因？
- RQ3：加入时间、持续时长、动态状态和工具参数后，复杂规划能力如何变化？

作者的核心形式化是：从合成用户输入中得到顺序/时间等约束；智能体执行的 action chain 若违反约束，就被判定为 erroneous planning。这个 oracle 规避了用另一个 LLM 判断计划正确性的循环依赖，但其完备性只成立于作者构造的 DSL、文本填充和 mock tool 语义内。

## 3. 被测试的智能体类型

论文组合两种闭源 LLM 与三种 agent framework，形成六类被测系统：

- 模型：`gpt-3.5-turbo-1106`、`gpt-4-1106-preview`；
- ReAct：completion 交互，以 few-shot prompt 调工具，可自定义 prompt 和参数；
- OpenAI Tools（OT）：chat + function calling，可自定义 prompt 和参数；
- OpenAI Assistant（OA）：chat + function calling，论文设置中不能自定义 prompt，也不能深入设置采样参数。

被测的是单智能体、工具调用、长时序规划系统。每个合成任务一一映射到一个 mock tool/action，不涉及多智能体协作、真实浏览器、代码仓库、具身环境、长期记忆或真实高风险工具副作用。

## 4. 测试或评估方法

### 4.1 DSL 驱动的输入合成

PDoctor 把自然语言计划问题收缩为多个 action 之间的先后关系。生成过程分为（Sections 3-4）：

1. **Skeleton synthesis**：用 DSL 生成由 action、句子、子句和顺序关系组成的抽象骨架；
2. **Text filling**：用职业日常任务主题和替代表达把骨架填成自然语言段落；
3. **Constraint derivation**：从同一骨架直接导出顺序约束；
4. **Satisfiability check**：用 Z3 排除内部矛盾、保证合成约束可满足；
5. **Agent execution**：把每个 action 映射到 mock tool，记录工具调用序列；
6. **Oracle check**：检查执行序列是否满足约束。

一项“任务”被简化成一次 tool/action，不需要智能体自行分解；这样隔离 planning，但同时排除了真实任务理解、分解和工具执行语义。

### 4.2 Mock tools

Mock tool 只记录调用并返回简单结果，使测试器可以直接观察 action chain，不必解释任意自然语言输出，也避免真实工具故障干扰 planning 测量。扩展版本让工具接收 start time 并返回 duration，使智能体必须根据运行时结果动态更新后续工具参数（Section 4.4）。

### 4.3 错误解剖

Algorithm 2 对触发错误的输入依次执行：

- 重复相同输入，若错误不稳定则标为 **Probability**；
- `TerminalSubstitute` 替换局部词语，若错误消失则标为 **Terminal**；
- `TopicChange` 保持结构/约束、改变职业主题，若错误消失则标为 **Topic**；
- `QuerySynthesize` 生成约束等价但结构不同的新输入；若错误消失则为 **Structure**，否则为 **Constraint**。

算法遇到首个解释即停止，并明确不分析一个 query 上的多重原因。因此这些标签是分层诊断结果，不一定是现实中的唯一因果根源。

## 5. 数据集、环境或基准

论文没有使用固定自然语言 benchmark，而是在线合成测试：

- action 数可配置；
- 基础版本用动作顺序约束；
- 合成 query 的子句数、句子结构和约束数随复杂度变化；
- 从 50 个职业日常任务主题中随机填充 action 文本；
- DSL terminal 有多种等价自然语言表达，用于增加表述多样性；
- Z3 检查约束可满足；
- 每个 action 绑定一个 mock tool；
- 扩展版本加入 start/end time、duration、tool parameter 和动态 constraint update。

RQ1 的 action 数从 3-5 随机采样，query 有 1-7 个子句、2-10 个约束。RQ2 对每个 action 数按 `20 × C(n,x)` 采样并将单档上限设为 300，从 2 个动作逐步增至 9 个；论文报告每个 agent 生成 1,600 个测试。RQ3 使用扩展版本，展示 2-5 个动作。

## 6. 评价指标

- 每个设置在固定时间内生成/执行的测试数；
- 检出的错误数和 error rate；
- Z3 call count、Z3 time、synthesis time、agent execution time；
- 不同 action 数下的 planning success rate；
- 以成功率低于 20% 定义的“planning capability limit/upper bound”；
- 四类基础错误：Timeout、Act Error、Action Lost、Order Error；
- 扩展版本新增 Parameter Error；
- 五类错误原因：Probability、Terminal、Topic、Structure、Constraint；
- 不同职业 topic 的错误次数。

“20% 能力上限”是论文人为设定的操作性阈值，不是经心理测量或统计功效验证的固有能力界限。error rate 也未给出置信区间，且 RQ1 在固定 60 分钟内各系统处理的样本数不同。

## 7. 实验设计

### 7.1 实现和公共设置

- PDoctor：Python 3，约 2,600 行；
- 约束求解：Z3；
- agent 实现：LangChain；
- 模型快照：`gpt-3.5-turbo-1106`、`gpt-4-1106-preview`；
- 除 temperature 外使用默认参数；ReAct/OT temperature 设为 0，OA 当时不支持设置；
- 每个测试创建新的 agent instance；
- 单例超时 180 秒、最多 50 次迭代。

### 7.2 RQ1：固定时间检错

- 六种 model-framework 组合各运行 60 分钟；
- action 数在 3-5 中随机；
- 比较生成测试数、错误率和测试器开销（Section 6.1；Table 2）。

因为慢模型在同一小时内得到的样本更少，这个设计适合比较吞吐和“单位时间发现多少错误”，但不同系统 error rate 的样本量和具体随机任务并不完全相同。

### 7.3 RQ2：能力曲线和错误解剖

- action 数 2-9；
- 单个难度最多 300 个样本；
- 每个 agent 共 1,600 个测试；
- 20% success rate 作为能力边界；
- 对能力范围内的错误分类，并用 Algorithm 2 做 root-cause dissection（Section 6.2；Figures 8；Tables 3-5）。

正文说“随机采样 100 个错误”并给出六个 agent 各自和为 100% 的行，但没有足够清晰地说明是每个 agent 各 100 个，还是一个样本如何分配到各行；复现时需查代码/原始数据确认分母。

### 7.4 RQ3：动态复杂规划

重复 RQ2 设计，但工具带时间参数、返回持续时长，智能体需根据结果更新后续计划。由于所有系统在 5 个动作前后已到能力界限，只展示 2-5 个动作（Section 6.3；Figure 9；Tables 6-7）。

## 8. 主要发现

### 8.1 PDoctor 合成本身很快，瓶颈是 agent 执行

RQ1 Table 2：

| 模型/框架 | 生成测试 | 错误（错误率） | Z3 时间 | 合成时间 | Agent 时间 |
|---|---:|---:|---:|---:|---:|
| GPT-3.5 ReAct | 843 | 519（61.57%） | 24.96s | 59.13s | 58:00.86 |
| GPT-3.5 OT | 1,168 | 635（54.37%） | 34.30s | 1:20.49 | 57:11.94 |
| GPT-3.5 OA | 327 | 179（54.74%） | 9.67s | 22.52s | 59:22.24 |
| GPT-4 ReAct | 160 | 47（29.38%） | 5.03s | 11.73s | 59:54.44 |
| GPT-4 OT | 144 | 32（22.22%） | 4.13s | 9.66s | 59:40.41 |
| GPT-4 OA | 111 | 40（36.04%） | 3.38s | 7.75s | 59:54.25 |

作者计算平均每个测试合成约 0.07 秒、Z3 少于 0.03 秒；agent 执行占绝大多数时间。论文称 GPT-4 组合的平均错误率相对 GPT-3.5 下降 48.53%。该比较来自不同吞吐、随机样本和固定时间窗口，没有报告配对任务或置信区间。

论文还宣称约束检查可“保证”发现任何 planning error。严格说，该保证只适用于：合成 query 的语义与 DSL 约束等价、动作与 mock tools 一一映射、错误定义就是违反这些约束的封闭测试模型；不能外推为发现真实 agent 的所有规划错误。

### 8.2 基础规划能力随动作数快速下降

Figure 8 以 20% success threshold 衡量：

- GPT-3.5 agents 在 action 数约 4 时达到论文定义的能力界限；
- GPT-4 agents 可延伸到约 8 个动作；
- GPT-3.5 在超过 3 个动作后成功率陡降，GPT-4 下降更缓。

这支持“规划具有明显难度敏感性”，但 action 数同时改变排列空间、query 长度和约束数，实验不能区分是哪一种复杂度因素造成下降。

### 8.3 顺序违反是基础版本最主要的执行错误

Table 3 在论文定义的能力范围内报告：

- GPT-3.5：ReAct/OT/OA 的 Order Error 分别为 90.72%/99.54%/98.80%；
- GPT-4：分别为 98.73%/98.88%/98.26%；
- GPT-3.5 ReAct 另有 8.25% Action Lost，其他组合较低；
- Timeout 在该表各设置均为 0。

这表明测试用例主要触发“执行顺序不满足显式约束”，而不是超时或调用不存在的工具。由于数据和 mock tools 就围绕顺序构造，这种错误分布不能直接代表现实智能体的总体失败分布。

### 8.4 表述、主题和随机性会改变同一约束的结果

Table 4 的 root-cause 比例中，Terminal 通常最大（28%-50%）；OA 的 Probability 为 27%（GPT-3.5）和 28%（GPT-4），高于其他多数设置。作者把 OA 的随机性部分归因于无法设置 temperature。

表中不同模型、同一框架的分布看起来相近，作者据此认为 framework 对错误原因影响可能大于底层模型。但这是描述性观察，没有独立重复、显著性检验或控制 framework prompt 长度/接口实现，不能写成已建立的因果结论。

### 8.5 时间和动态参数显著增加难度

扩展实验 Figure 9 显示：

- GPT-3.5 的所有组合在 3 个动作时已低于 20%；
- GPT-4 在超过 4 个动作后成功率急降；
- ReAct 在扩展设置最弱；GPT-3.5 ReAct 连最简单档也未形成可用成功结果，GPT-4 ReAct 各 action 数均低于 50%。

Table 6：

- GPT-3.5 OT/OA 的 Parameter Error 分别占 64.29%/50.00%；
- GPT-4 ReAct 的 Act Error 为 64.44%；
- GPT-4 OT/OA 的 Order Error 为 66.04%/64.31%，Parameter Error 为 27.36%/33.83%；
- GPT-3.5 ReAct 因没有成功处理最简单问题，表中为 NaN。

Table 7 对 GPT-4 为主的错误解剖中，Constraint 在 ReAct/OA 达 45%/39%，OT 为 23%；加入时间、duration 和动态返回后，约束结构本身比基础版本更常成为错误触发因素。

### 8.6 直接用 LLM 生成自然语言测试会破坏 oracle

Section 7 把约束和 action mapping 交给 GPT-4 生成 query，每个 action 数 2-5 重复 10 次，再人工检查语义一致性。动作数小于 4 时为 100%，4 个动作时 80%，5 个动作时 0%。这项小规模实验支持使用 DSL 从同一结构生成文本和 oracle，但样本每档仅 10 个、由人工核验，不能证明所有 LLM 生成策略都不可用。

## 9. 局限性

- DSL 刻意缩小自然语言语义，只测 action 顺序及扩展时间约束，不代表真实开放域规划。
- 每个任务一一对应一个 mock tool，排除了任务分解、真实工具语义、环境副作用、工具失败和结果解析。
- oracle 假设 action 之间没有未明说的常识依赖；Section 7 承认显式约束可能与固有顺序冲突。
- “任何错误都能检测”的保证只在封闭形式模型内成立，且依赖 text filling 与约束语义真正等价。
- 只测两个 2023 年 11 月 OpenAI 模型和三个当时的 LangChain/OpenAI agent 接口；模型与 API 已发生明显漂移。
- RQ1 固定时间导致不同组合的测试数量差异很大，且随机任务不一定配对。
- 多数结果没有重复实验、误差条、置信区间、随机种子或显著性检验。
- temperature 设 0 不能消除闭源 API 和多轮 agent 的非确定性；OA 又不能设置 temperature。
- “20% planning capability limit”是人为阈值，不能解释为模型的真实理论上限。
- action 数同时改变排列数量、输入长度与约束密度，缺少因素分解。
- Error Dissection 按层次提前停止、不允许多标签，可能把共同原因压缩成首个可观察变化；语义保持变换也可能存在细微差异。
- 论文以职业主题填充 query，主题错误次数很小且没有统计检验，不足以做强领域能力结论。
- 没有报告 token、美元成本、机器配置、网络/API 错误、依赖版本或真实工具执行开销。
- 未测试提示注入、权限越界、恶意工具输出、长期状态漂移、多智能体级联或安全后果。

## 10. 可复现性信息

- 实现：Python 3、约 2,600 LOC、Z3、LangChain；
- 模型快照：`gpt-3.5-turbo-1106`、`gpt-4-1106-preview`；
- 采样：ReAct/OT temperature 0，其他参数默认；OA 不支持 temperature；
- 运行上限：每案例 180 秒、50 iterations；RQ1 每组合 60 分钟；
- RQ1/RQ2/RQ3 报告 action 范围、约束范围、采样上限和主要算法；
- Algorithm 2 给出错误解剖的变换顺序；
- 论文给出匿名评审期代码链接，但本次未核验到稳定正式仓库、release tag 或归档 DOI；
- 未充分报告 Python/LangChain/Z3 精确版本、依赖锁、硬件、随机种子、prompt 全量、API region、原始结果和费用；
- 旧 OpenAI 模型快照和 OA/OT 接口可能不可再用，严格复现需要保存模型替代策略并区分“原结果复现”和“方法再实现”。

## 11. 与“智能体测试”研究的关系

PDoctor 是少数直接把软件测试思想用于 agent planning 的研究：

- **约束 oracle**：把模糊的“计划看起来合理”转化为可自动判定的属性；
- **输入生成**：通过 DSL 系统控制任务复杂度、约束和语义；
- **属性/变形测试**：在约束不变时替换词、主题或结构，检查行为是否应保持；
- **故障定位**：把错误分为顺序、遗漏、调用、参数和超时，再用输入变换做分层诊断；
- **状态化测试**：扩展版本根据工具返回的 duration 动态更新约束，接近真实 agent 的运行时状态；
- **框架差异**：相同模型在 ReAct、function calling 和 Assistant 中有不同失败分布，说明测试单位必须是完整 agent stack。

它也显示 agent testing 与普通 LLM 测试的区别：单次输出正确不够，必须收集实际 action/tool trajectory，并在动态环境状态上验证每一步。

## 12. 可借鉴的工程实现

1. 为业务 workflow 定义可执行 DSL，将顺序、前置、互斥、时间、资源和权限约束转成 SMT oracle。
2. 从同一抽象测试模型同时生成自然语言输入和机器 oracle，减少 LLM judge 偏差。
3. 用 mock tools 隔离 planning，再逐步替换成可控 sandbox tools，区分计划错误与工具故障。
4. 记录完整 tool trajectory、参数、返回状态、时间和约束违反项，避免只看最终答案。
5. 按 action 数、约束密度、句式复杂度和动态状态分别做因子实验，不把它们合并为单一“难度”。
6. 建立 metamorphic relations：同义改写、主题替换、句序变化和等价约束不应改变合法计划集合。
7. 允许一个失败多标签，并通过 delta debugging 最小化触发 query，改进原算法的首因停止限制。
8. 注入 timeout、错误返回、参数边界、权限拒绝和恶意工具输出，扩展到运行时恢复与安全。
9. 对每个设置重复运行，报告 error rate 区间、跨运行一致性、token、费用和 wall-clock。
10. 把 SMT 检出的违反约束及 `unsat_core` 转成可读诊断，供 CI 回归和在线 guardrail 使用，但不要自动把 solver 计划用于高风险操作而缺少人工验证。

## 13. 证据等级和全文访问情况

- 证据等级：**已阅读全文**。
- 全文来源：本地 PDF `research/papers/2024-Ji-ErroneousPlanning.pdf` 和 arXiv 解析全文 `.codex-data/arxiv-papers/2404.17833.md`。
- 本地/在线身份：`arXiv:2404.17833v1`；未核验到正式发表版本或 DOI。
- 阅读范围：问题形式化、Sections 3-4 的 DSL/合成/Z3/mock tool/扩展状态/Algorithm 2，Section 5 实现，Section 6 三个 RQ 和 Tables 2-7，Section 7 替代生成方法与有效性威胁。
- 工具访问限制：论文给出匿名评审链接，但本次未确认其当前完整性，因而不把代码视为已由稳定归档核验。

## 14. 可以支持综述中的结论

- 智能体规划可被表述为对 action trajectory 的约束满足测试；
- DSL 能同时生成测试输入和可执行 oracle，减少主观 LLM judge 依赖；
- 变形输入可揭示同一逻辑约束对词语、主题、结构和随机性的敏感性；
- 模型和 agent framework 共同决定错误率与错误类型，测试必须覆盖完整系统栈；
- 动态工具返回和参数状态会显著增加规划难度并产生新的 Parameter Error；
- 行为轨迹中的 Order Error、Action Lost、Act Error、Timeout 和 Parameter Error 比单一成功率更有诊断价值；
- 形式化 oracle 的“保证”受 DSL 语义、mock 工具和封闭世界假设限制；
- 当前研究仍缺真实工具、开放域输入、多模型复现、安全故障注入、统计不确定性以及成本/延迟的系统报告。
