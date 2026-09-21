# AgentBoard：结构化阅读笔记

## 1. 基本信息

- **标题**：AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents
- **作者**：Chang Ma, Junlei Zhang, Zhihao Zhu, Cheng Yang, Yujiu Yang, Yaohui Jin, Zhenzhong Lan, Lingpeng Kong, Junxian He
- **年份**：2024
- **会议或期刊**：Advances in Neural Information Processing Systems 37，Datasets and Benchmarks Track（NeurIPS 2024，Oral）
- **DOI**：未核验到正式 DOI，不猜测
- **arXiv ID**：2401.13178
- **正式版本和预印本关系**：2024 年 arXiv 预印本后进入 NeurIPS 2024 Datasets and Benchmarks Track；正式引用优先使用 NeurIPS 版本，arXiv 用作全文入口。
- **代码**：<https://github.com/hkust-nlp/AgentBoard>

## 2. 研究问题

AgentBoard 针对只报告任务成功率所造成的“低分但不知道失败在哪里”问题，研究如何用细粒度、可解释且跨任务可比较的进度指标评测多轮 LLM agent。它进一步考察 grounding、规划、记忆、世界建模、自我反思、空间导航等属性，以及任务难度、轨迹长度、提示方式和历史管理对结果的影响。

## 3. 被测试的智能体类型

- 文本观察和文本动作的单智能体，多数环境部分可观测。
- 四类应用：embodied、game、web、tool；既含具身文本模拟，也含 WebArena 和外部工具查询/操作。
- 基线主要采用 Reflex 风格：给最近历史，直接产生下一动作；另做 ReAct 对照。
- 不直接评估多智能体协作、视觉 GUI 或真实物理机器人。

## 4. 测试或评估方法

第 2 节把任务写成目标条件下的 POMDP `<g,S,A,O,T>`。核心贡献是 **progress rate**：

- 连续状态匹配任务用历史状态与目标的最大匹配度；
- 可分解任务先将目标人工标注为 K 个唯一子目标，计算每一状态满足的子目标比例，再对整条轨迹取最大值；
- 对历史取最大值使已达到的最高进度不会因最后几步回退而消失，便于解释“离成功多远”。

第 3 节还提供细粒度分析面板：成功率、进度曲线、grounding accuracy、任务难度和按能力属性分组的表现。需注意，表 11 的能力标签是对任务所需属性的标注，而非直接探针式测量模型内部的“记忆”或“世界模型”。

## 5. 数据集、环境或基准

论文整合九项任务：

- **Embodied**：ALFWorld、ScienceWorld、BabyAI。
- **Game**：Jericho、PDDL（Gripper、Barman、Blocksworld、Tyreworld）。
- **Web**：WebShop、WebArena。
- **Tool**：Tool-Query（Weather、Movie、Academia）与 Tool-Operation（Todo、Google Sheet）。

表 14 给出的环境数依次为 134、90、112、20、60、251、245、60、40；逐项相加为 **1,012**，而摘要和正文多处称 **1,013**。这是论文内部计数不一致，笔记不替作者猜测哪一数字正确。任务最大轮数从 WebShop 的 3 到 WebArena 的 25；平均上下文长度从约 900 到 WebArena 的约 15,000 tokens，动作空间规模和子目标数也不同。

## 6. 评价指标

- **Success Rate**：最终任务是否完成。
- **Progress Rate**：轨迹中达到的最大连续匹配或子目标完成比例，是论文主张的诊断指标。
- **Grounding Accuracy**：模型输出能否映射为环境合法动作。
- **Progress over Steps**：随交互步数的累计进度曲线，用于观察长程停滞。
- **Easy/Hard 分层**：按任务组成难度比较进度和成功率。
- **属性维度**：按任务所需 memory、planning、world modeling、self-reflection、grounding、spatial navigation 聚合，但不是独立控制变量。
- 人工效度验证使用 Pearson 相关系数和 Fleiss’ kappa，将自动 progress 与四位作者的轨迹评分比较。

## 7. 实验设计

- 主实验覆盖闭源 API 与开源模型，包括 GPT-4、GPT-3.5、Claude 2/3、Gemini 1.5 Flash、Llama 2/3、Mistral、DeepSeek、AgentLM、xLAM 等。
- 主设置为 Act-only/Reflex agent，使用最近历史的滑动窗口；第 4 节和附录 F 比较 ReAct、硬截断及历史摘要。
- 附录 I 报告模型标识和推理环境，例如 Azure GPT-4 API version 2023-05-15、Claude 2 API 2023-06-01、Claude 3 Haiku 2024-03-07；开源模型经 vLLM 推理。
- 主设置说明 greedy、temperature=0；附录置信区间讨论又称专有模型因较高温度偏差更大，文本存在轻微表述张力，复现时应以配置代码和具体模型调用记录为准。
- 任务经三轮质量控制；对自动 progress，八类任务各抽 60 条由四位作者以 0/25/50/75/100 人工评分。

## 8. 主要发现

1. **进度比二元成功率提供更多区分度。** 表 3 中 GPT-4 平均 progress 70.0、success 47.9；Claude 2 为 48.9/26.2，Gemini 1.5 Flash 为 43.5/20.6，Llama-3-70B 为 41.9/20.2。许多失败轨迹仍完成部分子目标。
2. **自动进度与人工判断高度一致。** 图 3 报告各任务 Pearson 相关均高于 0.95；Fleiss’ kappa 约 0.73–0.91（WebShop 最低 0.73，WebArena 最高 0.91），支持该指标作为诊断近似，而非证明其在所有新环境中无偏。
3. **Grounding 是必要但不充分条件。** 表 4 中 GPT-4 平均 grounding accuracy 85.6；Text-Davinci-003 为 58.9，却能在部分任务取得与 GPT-3.5 接近的总体表现。动作合法不等同于规划和任务完成。
4. **组合难度显著拉低最终成功。** 表 5 中 GPT-4 在 easy/hard 上平均 progress 为 79.2/62.7（下降 16.5 点），success 为 65.6/34.4（下降 31.2 点），二元成功率对长链错误更敏感。
5. **多数模型的长程进展很快停滞。** 图 4 显示 GPT-4、Claude 2 在 ALFWorld/PDDL 可持续到约 30 步，而多种开源模型约 6 步后几乎不再增加；WebArena 和 tool 任务即使对强模型也较早进入平台期。
6. **agent tuning 可改善但未解决问题。** AgentLM-70B 相比 Llama-2-70B 的平均 progress 提升 9.5 点、success 提升 10.2 点；xLAM-70B success 为 20.4，仍远低于 GPT-4 的 47.9。
7. **历史管理本身影响分数。** 附录 F 表 10 中 GPT-3.5 的滑动窗口为 41.4/19.7，硬截断为 32.8/13.7，摘要为 33.5/14.4；这表明 benchmark 结果也是模型与 agent memory 策略的联合结果。
8. **ReAct 并非稳定优于 Act。** 附录 F 表 9 中不同任务方向不一致，例如 ALFWorld 的 ReAct progress 略升但 success 下降，Tool-Operation 则提升，不能把某一提示范式当作普适最优。

## 9. 局限性

论文第 7 节明确指出：

- 子目标需要人工标注，扩大到新任务成本高；
- 大多数环境是模拟环境，真实世界 ground truth 会变化且伴随安全风险；
- 当前集中在文本 agent，视觉输入和 GUI grounding 未覆盖。

测试视角还应注意：

- “对历史取最大 progress”会忽略之后撤销正确操作或造成副作用；它衡量最高到达进度，不等于最终状态质量。这是由公式直接推得的边界，不是作者实证结论。
- 唯一子目标集合会压缩替代路径、顺序约束和不可逆错误；进度正则表达式也可能只验证表面状态。
- 能力分析是任务属性分组，不能严格归因为单一认知能力。
- 模型温度描述存在轻微不一致，闭源 API 版本也会漂移。
- 未评估提示注入、权限越界、数据泄露、token/货币成本和线上稳定性。
- 论文声称 1,013 个环境，而表 14 数字求和为 1,012，数据规模报告需要后续用发布仓库核对。

## 10. 可复现性信息

- **代码与数据**：GitHub 公开 AgentBoard、任务适配和评测面板。
- **任务配置**：表 14 给出环境数、轮数、动作空间、平均子目标和上下文长度；附录任务章节说明各环境来源。
- **子目标与质控**：手工子目标、正则匹配和三轮检查过程有说明。论文称编辑影响总体不到 5%，但 ScienceWorld 需修改 36 个、约 40%，任务间差异较大。
- **提示**：附录提供 Act/ReAct 等模板；主设置采用近期历史滑动窗口。
- **模型/参数**：附录 I 给出闭源 API 日期/版本和开源 checkpoint；主设置为 greedy、temperature=0，使用 vLLM。
- **资源**：表 18 报告参考运行时间，例如 GPT-4 约 1.5 秒/轮、全套约 5.5 小时；DeepSeek-67B 在 8×V100 上约 18.5 小时，Llama-2-70B 在 8×V100 上约 28 小时或 4×A100 上约 13.5 小时。
- **缺失/风险**：没有完整 API 输出快照；环境总数矛盾与温度表述应在复现实验前核查。

## 11. 与“智能体测试”研究的关系

AgentBoard 将 agent 测试从单一 pass/fail 扩展到“过程完成了多少”，适合定位长链任务中最早停滞的位置。其价值不在于替代最终状态 oracle，而在于把 progress、success 和 grounding 组成多层指标：动作是否合法、局部子目标是否推进、最终目标是否完成。论文也实证显示 agent scaffold（历史窗口、ReAct/Act）可显著改变模型得分，因而质量保障对象应是整个系统配置。

## 12. 可借鉴的工程实现

- 给业务工作流定义可验证子目标和最终不变量，同时保留严格最终态检查。
- 每步计算 progress delta；长时间无增量时触发循环/停滞告警，而不是只等到最大轮数。
- 将 `parse_valid`/grounding、`subgoal_progress`、`final_success` 分层记录，分别归因语法、执行与规划故障。
- 可视化每条 trajectory 的 progress 曲线，并在模型/提示/记忆策略升级时做曲线级回归。
- 使用人类分层评分抽样校准自动 oracle；报告相关性和一致性，不把高相关误写为完全等价。
- 对撤销、破坏性动作和顺序约束增加负向状态或 safety invariant，弥补历史最大值指标。
- 把模型 ID、API 日期、采样参数、历史压缩策略与环境版本绑定到每次测试运行。

## 13. 证据等级和全文访问情况

- **证据等级：已阅读全文。**
- **全文来源**：本地解析文本 `/tmp/agent-review-text/2024-Ma-AgentBoard.txt` 及 arXiv 2401.13178 本地全文。
- **阅读范围**：正文全部章节、表 2–5、图 3–4，并阅读附录中的任务属性、人工验证、置信区间、提示/历史消融、模型设置、数据质量和运行资源（尤其表 9–14、18）。
- **访问限制**：无论文全文限制；闭源 API 和在线工具状态不能由静态论文完全重放。

## 14. 可以支持综述中哪些结论

- 智能体评测需要把最终成功率与轨迹级进度、动作合法率结合。
- 长程任务会放大局部错误，且许多模型在少数步骤后进入进度平台。
- 记忆窗口和提示/推理框架是测试配置的一部分，比较模型时必须固定和披露。
- 自动轨迹指标可以经人工评分校准，但子目标标注成本和 oracle 偏差仍是瓶颈。
- Grounding 准确率不能单独代表任务完成能力。
- 现有分析型基准对视觉、安全、副作用、成本和真实在线环境覆盖不足。
