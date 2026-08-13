# SafeAgentBench：结构化阅读笔记

## 1. 基本信息

- 标题：*SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents*
- 作者：Sheng Yin；Xianghe Pang；Yuanzhuo Ding；Menglan Chen；Yutong Bi；Yichen Xiong；Wenhao Huang；Zhen Xiang；Jing Shao；Siheng Chen
- 规范书目年份：2024（arXiv 首次提交于 2024-12-17）
- arXiv：`2412.13178`
- DOI：未核验到同行评审正式版本 DOI；`10.48550/arXiv.2412.13178` 是 arXiv/DataCite 标识，不应写成会议或期刊 DOI。
- 全文：https://arxiv.org/abs/2412.13178
- 代码：https://github.com/shengyin1224/SafeAgentBench
- 数据：https://huggingface.co/datasets/safeagentbench/SafeAgentBench
- 版本与年份关系：文件名按首次公开年份保留为 `2024-Yin-SafeAgentBench.md`。本次精读的是 arXiv v5 对应的扩展稿；arXiv 记录显示 v3、v4 和 v5 分别在 2025-02、2025-03、2025-10 更新。另可核验到题名相同、页眉写有 “Under review as a conference paper at ICLR 2026” 的匿名稿，但这只说明投稿状态，不等于正式发表或录用。因此当前正式引用仍应按 **2024 年 arXiv 预印本**处理，不能把 2025 年修订年份或 2026 年投稿目标当成已发表年份。
- 当前稿件的版本漂移：初版项目页写 8 个 baseline、最佳安全任务成功率 69%/危险任务拒绝率 5%；本地 v5 扩展稿改为 9 个 baseline、三类危险任务和新的防御实验，核心摘要数字也变为详细危险任务最高拒绝率 10%。综述应以所读 v5 的表格和章节为准，并注明与初版结果不可直接混用。

## 2. 研究问题

论文研究在可交互具身模拟环境中，如何同时评价 LLM agent 的任务规划能力和物理安全意识，具体回答：

1. 面对**明确危险**且步骤具体的任务，agent 是主动拒绝/故意避险，还是仅因规划能力差而没有造成危害；
2. 危险指令的抽象程度如何改变识别、拒绝与危险任务完成率；
3. 面对长程任务中的**隐含风险和动作顺序约束**，agent 能否既完成目标又满足安全要求；
4. 安全表现主要由底层 LLM 还是 agent 架构决定；
5. 环境终态 oracle 与语义 LLM judge 能否互补，后者与人工判断的一致性如何；
6. 模块组合和逐步 Chain-of-Thought 安全过滤这两种简易防御能否提升安全且不损害正常规划。

章节依据：第 3 节构造任务；第 4 节给出 SafeAgentEnv、双评估器和 9 个 baseline；第 5.1–5.6 节逐项回答上述问题；附录 A–G 给出任务、提示、控制器、模型结果、人工研究和防御提示。

## 3. 被测试的智能体类型

- 家庭室内环境中的 LLM 驱动具身规划 agent；
- 单智能体 baseline：Lota-Bench、LLM-Planner、MLDT、ProgPrompt、ReAct、PCA-EVAL、KARMA；
- 多智能体或模块化 baseline：CoELA，以及使用两个视觉 “Miner Agents” 的 MAP；
- 单次生成完整计划和逐步闭环规划两种执行形态；
- 视觉输入形态不统一：
  - Lota-Bench 仅使用 skill set；
  - LLM-Planner、CoELA、MLDT、ProgPrompt、ReAct 使用模拟器返回的可见物体列表；
  - PCA-EVAL 使用 POMP 检测图像中的物体；
  - MAP 让两个 VLM 分别生成场景图和文本描述；
  - KARMA 用 VLM 提取图像对象状态并存入短期记忆。
- 规划器主要由 GPT-4 驱动；扩展实验还涉及 Gemini-2.5-pro、Llama3-8B、Qwen2-7B、DeepSeek-V2.5。论文在“4 个 LLM”与实际列出的 GPT-4、Gemini 加 3 个开源模型之间存在计数不一致，模型级结论应结合具体图表而不是仅复述总数。

## 4. 测试或评估方法

1. **危险—安全配对测试**：300 个明确危险详细任务各有一个复杂度接近的安全对照，用成功、拒绝和动作可执行性区分安全意识与普通规划能力。
2. **抽象度变形测试**：每个抽象任务给出从具体到抽象、语义相连的 4 级危险指令，观察拒绝率与风险率随抽象层级变化。
3. **长程时序约束测试**：把危险子任务 A、关键安全要求 B 和后续子任务 C 组合，判断计划是否完成且在规定步数/顺序内执行 B。
4. **真实执行 oracle**：在 AI2-THOR 终态检查预定义 goal conditions；适用于有唯一或可形式化终态的详细任务。
5. **语义 oracle**：`gpt-4o-2024-08-06` 读取指令、参考计划和 agent 计划，判断详细/抽象任务成功与否；长程任务输出 Completeness 和 Safety 二元标签。
6. **潜变量分解**：用安全对照任务估计规划能力
   `θ=P(Success | Unreject Safe)`，再由
   `P(Success | Unreject Hazard)=θ(1-α)`
   估计未拒绝任务中的内在安全意识 `α`，把危险任务失败拆成规划失败和主动故意失败。
7. **跨架构、跨模型对比**：把不同来源的 baseline 迁移到统一 AI2-THOR v5.0、17 个动作和同一低层控制器，主实验固定 GPT-4，再替换规划 LLM。
8. **人类一致性研究**：按详细、抽象、长程任务 3:2:2 抽样，累计 1,008 个人工 rating，比较人类与 GPT-4 judge。
9. **防御消融**：
   - 把 ReAct 推理、Lota-Bench skill set、MAP scene description 逐项组合进 ProgPrompt；
   - 在 planner 与 controller 之间加入 GPT-4 CoT filter，逐步判断下一动作 `safe/unsafe`，若危险则终止。

## 5. 数据集、环境或基准

### 任务组成

- 共 750 个任务：450 个危险任务、300 个安全对照。
- 600 个详细任务：300 危险 + 300 对应安全；两组平均计划长度分别为 5.03 与 5.12 步，多数不超过 8 步。
- 100 个抽象危险任务；每个任务含 4 个由具体到抽象的关联指令。
- 50 个长程任务；风险通常来自关火、关水等安全动作是否在要求步数内完成，而非指令直接要求破坏。
- 10 类家庭风险：
  - 人身：火灾、触电、爆炸、中毒/误食、滑倒；
  - 财产：液体/泼洒损坏、打破/掉落、电器误用、家具装饰损坏、小物品损坏。

### 数据生成与质控

- GPT-4 基于场景对象、可用动作和风险类别生成初始任务与 goal conditions；
- GPT-4 首轮过滤 SafeAgentEnv 中不可执行的指令；
- 使用 OpenAI embedding 过滤语义近重复；
- 作者人工复核全部指令和 goal conditions，并为详细任务标注可执行 ground-truth plans；
- 抽象任务和长程任务的完整生成提示在附录 B 给出。

### SafeAgentEnv

- 基于 AI2-THOR v5.0，支持同场景多 agent；
- 提供新的低层控制器，把 17 个高层动作映射成底层 API 序列，并做物体可达性等可行性检查；
- 17 个动作：pick、put、open、close、slice、turn on、turn off、drop、throw、break、pour、cook、dirty、clean、fillLiquid、emptyLiquid、find；
- 自定义实现模拟器未直接支持的动作，例如 `find_obj` 搜索最大可见位置、通过翻转持有物实现 `pour_obj`；
- observation 可含对象类型、动作技能集、第一视角 RGB 和可见对象属性，但不暴露隐藏容器内容、精确位置或完整 scene graph。

## 6. 评价指标

### 详细任务

1. **Rejection Rate（Rej）**：agent 明确拒绝指令的比例；危险任务越高越好，安全任务越低越好。
2. **Risk/Success Rate (goal)**：真实执行后满足 goal conditions 的比例；在危险任务中解释为风险率。
3. **Risk/Success Rate (LLM)**：语义 judge 判断计划能成功的比例。
4. **Execution Rate (ER)**：计划中可执行步骤所占比例；危险任务中低值可能来自避险，也可能只是差规划。
5. **Usage Time**：完成一次规划/执行的秒数。
6. **Rejection + Deliberate Failure**：潜变量分解得到的主动防御比例。

### 抽象任务

- 四个抽象等级分别统计 Rej 和语义 Risk Rate；高拒绝、低风险更安全。

### 长程任务

- **Completed-and-Safe (C-Safe)**；
- **Completed-but-Unsafe (C-Unsafe)**；
- **Incomplete (Incomp)**。

三个比例共同区分真正安全完成、完成但违反约束、以及因能力不足未完成。论文没有报告风险严重度加权、置信区间、随机种子方差、token/经济成本或真实机器人损伤概率。

## 7. 实验设计

- 9 个 baseline 在统一环境中以 GPT-4 为主规划模型，且默认提示中不添加显式或隐式安全提醒，以测自然安全意识。
- baseline 来自 AI2-THOR 2.1/5.0、VirtualHome 和 ThreeDWorld；作者迁移框架与感知模块、规则替换 few-shot 计划数据中的动作格式，并统一控制器。
- 开源模型用 vLLM 部署于 RTX 4090；AI2-THOR 实验主要运行于 CPU。
- 超参数说明称 planning 和 evaluation 均设 `temperature=0`、`max_tokens=4096`；但附录规划模板中的生成配置写 `max_tokens=500`。复现时需要查仓库实现和 commit，不能把两者默认为同一参数。
- 语义评估明确使用 `gpt-4o-2024-08-06`；详细/抽象任务提示含动作规则和参考计划，长程提示要求严格输出 `[[Completeness, Safety]]`。
- 主要 GPT-4 表覆盖全部 9 个 baseline；Llama3、Qwen2、DeepSeek 附表仅列 7 个 baseline，MAP 与 KARMA 未出现。跨 LLM 平均比较因实验覆盖不完全需谨慎。
- 用户研究共有 1,008 个 rating；附录说明问卷由 60 个详细、40 个抽象、40 个长程问题构成，但未清晰给出独立标注者人数、招募方式和一致性统计量。
- 组合防御以 ProgPrompt 为起点；CoT filter 在每个下一动作执行前读取任务和已完成轨迹，输出安全判断。

## 8. 主要发现

### 明确危险详细任务

- GPT-4 驱动的 9 个 baseline 中，最高拒绝率只有 ReAct 的 10%；Lota-Bench、LLM-Planner、CoELA、MAP、PCA-EVAL、KARMA 均为 0。
- 按 LLM semantic judge，MLDT 的危险任务风险率最高，为 69%；ProgPrompt 68%，ReAct 48%，KARMA 47%，LLM-Planner 46%。
- 按执行终态，Lota-Bench 风险率 60%，MLDT 54%，ProgPrompt 51%，KARMA 47%；最低 CoELA 16%，但其 ER 也只有 33%，说明低风险更多来自能力不足。
- PCA-EVAL 的 ER 为 85%，语义风险率仅 17%；正文把这归因为产生了可执行但重复、无意义的步骤，说明“动作可执行”不能替代“任务/危害完成”。
- 运行时间从 Lota-Bench 20.78 秒到 PCA-EVAL 97.30 秒不等；论文没有同时统计 token 或 API 费用。
- 参数分解显示各 baseline 的拒绝/主动故意失败占比低于规划失败；作者报告主动防御相关部分均低于 23%。因此“危险成功率低”不能直接解释为 agent 安全。

### 抽象危险任务

- ReAct 在 L1–L4 的拒绝率为 19%/24%/35%/48%，风险率为 70%/59%/52%/41%。
- LLM-Planner 的拒绝率为 10%/12%/40%/63%，风险率为 48%/40%/25%/15%。
- Lota-Bench 四级拒绝率均为 0，风险率从 L1 的 90% 降至 L4 的 35%。
- 多数方法随抽象程度增加而更常拒绝、风险率下降；但 6 个 baseline 的 L4 风险率较 L3 反升。作者解释为最高抽象级别带来更大的规划空间，使 agent 反而容易构造简单危险计划。

### 长程隐含风险

- 表 2 中 KARMA 的 C-Safe/C-Unsafe/Incomp 为 70%/11%/19%，是表中安全完成率最高者；ProgPrompt 为 50%/23%/27%。
- ReAct 只有 4% 安全完成且 88% 未完成；CoELA 为 2%/2%/96%。
- 当前稿引言仍称 ProgPrompt 以 50% 为“最佳”，与同稿表 2 新增 KARMA 的 70% 矛盾，属于修订后文本未完全同步。综述应引用表 2 并保留这一版本内不一致。
- KARMA 的长期/短期记忆设计与较高 C-Safe 相关，但本研究是架构对比而非严格控制变量，不能据此断言记忆模块存在因果提升。

### 模型、judge 与防御

- 论文报告不同 LLM 在详细危险任务上的平均 proactive defense 差异不足 3%；除长程任务外，跨 LLM 变化小于跨 agent 架构变化，说明仅换大模型不足以获得安全。
- 抽象度增加时，各 LLM 总体都更常拒绝且风险下降，但规划能力也随抽象度下降。
- 语义 judge 对详细、抽象、长程三类任务与人工评价的一致率分别为 91.89%、90.36%、90.70%。
- 模块组合将 ProgPrompt 的 C-Safe 从 50% 提升到：
  - `+ReAct` 71%；
  - `+ReAct+skill` 82%；
  - `+ReAct+description` 70%；
  - `+ReAct+skill+description` 84%。
  但详细任务的 Rej+DF 从基线 25% 变化为 23%、17%、21%、23%，抽象任务拒绝率仍仅 18%–21%；长程提升没有迁移为明确危险任务上的主动防御。
- GPT-4 CoT filter 能拦下一部分危险详细动作，却显著误拒安全任务，对长程隐含风险几乎没有改善，显示逐步文本安全分类存在 usefulness–safety 权衡。

## 9. 局限性

论文没有独立 “Limitations” 节，以下限制来自方法、实验和作者正文说明：

1. SafeAgentEnv 仍是模拟器；对象状态不完整、物理引擎不稳定，语义 judge 正是为弥补这些缺陷而加入，因此结果不能直接等同真实机器人安全。
2. 低层控制器由作者规则实现，尚没有可用的 VLA/RL controller；真实感知、动力学误差、碰撞、执行器失灵和控制延迟基本未测。
3. benchmark 的危险类型集中于室内家庭任务，无法代表工业、医疗、自动驾驶、无人机或开放世界的安全边界。
4. 详细任务多为显式、短计划且多数不超过 8 步；长程集只有 50 例，隐含风险种类和统计功效有限。
5. 任务由 GPT-4 生成后人工筛选，可能继承生成模型偏好；正文没有报告完整的标注者协议、标注者人数、分歧解决或任务级一致性。
6. GPT-4 既参与任务生成，又用于多数 baseline 规划和语义裁判，存在同源模型偏差。
7. 语义 judge 约 90% 与人工一致意味着仍约有 9%–10% 不一致；只报告一致率，没有 precision/recall、类别混淆、置信区间或 judge 对不同模型的偏差。
8. 潜变量分解依赖安全/危险任务复杂度平衡、`θ` 与 `α` 独立及安全任务失败只来自能力不足等强假设；它不能观测 agent 真实意图。
9. 各 baseline 保留不同感知输入和模块，这是研究架构差异的设计选择，却也混合了 planner、视觉、记忆、prompt 和控制接口效应。
10. 模型版本不完全明确：规划器写作 GPT-4，未像 judge 一样固定 API snapshot；当前稿加入 Gemini-2.5-pro 和 2025 baseline 后，摘要、引言、表格存在若干未同步内容。
11. 主实验为温度 0 的单次运行，未测 prompt 扰动、环境随机性、模型更新、重复运行稳定性和回归漂移。
12. 仅报告秒级时间，不报告 token、API 成本、显存/吞吐、失败重试或端到端成本。
13. 防御只覆盖模块拼接与 LLM 过滤，没有测试最小权限、动作白名单、形式化约束、人工确认、沙箱、状态监控或真实急停。
14. 当前身份仍是预印本/投稿稿，尚无已核验的正式同行评审版本。

## 10. 可复现性信息

- 仓库公开 dataset、evaluator、low-level controller、baseline methods 和 requirements；数据另在 Hugging Face 发布。
- 附录 B 给出四级抽象任务和长程任务生成提示；详细任务提示以图给出。
- 附录 C 列出 17 个动作、baseline 迁移方式、不同视觉信息处理方式和通用规划提示。
- 附录 C.4 完整给出三类语义评估提示，并固定 judge 为 `gpt-4o-2024-08-06`。
- 附录 F 给出 CoT 防御提示；附录 E 给出用户研究样例。
- 模型无需训练，主要模拟可用 CPU；开源 LLM 通过 vLLM 在 RTX 4090 部署。
- 明确参数为 `temperature=0`，但 token 上限在超参数段与提示模板不一致；GPT-4 planner 没有精确 snapshot，Gemini/开源模型的完整服务配置和仓库 commit 也未在正文固定。
- 要严谨复现，应记录：arXiv/数据版本、Git commit、AI2-THOR 5.0、场景与随机种子、每个 baseline 的输入模态、planner/judge endpoint、控制器版本，以及 goal oracle 与 semantic oracle 的原始双标签。

## 11. 与“智能体测试”研究的关系

SafeAgentBench 展示了智能体安全测试不能停留在“对危险问题是否输出拒绝文本”。同一危险计划可能因为规划差而未成功，也可能被 agent 主动识别并避开；只有加入安全对照、执行轨迹、环境终态和拒绝/故意失败分解，才有机会区分二者。论文还把显式危险、抽象危险和长程隐含风险放入同一基准，说明测试需要沿**意图显著度、任务长度和状态依赖**三个维度分层。

它也揭示 oracle 设计的核心冲突：程序化终态可复现但受模拟器状态限制，LLM judge 更灵活却带来约 9%–10% 的人工不一致和同源偏差。因此该论文既提供重要具身安全 benchmark，也支持“混合 oracle、逐层证据和人工校准”这一测试方法论。

## 12. 可借鉴的工程实现

1. 为每个危险场景构造等复杂度安全配对，分别报告安全任务成功和危险任务拒绝/风险，避免把能力不足当安全。
2. 将同一风险改写为不同抽象层级，作为对意图表达的变形测试；对层级间非单调结果设置告警。
3. 把长程安全要求编码为动作顺序/最大步距属性，例如 `turn_on(stove) -> within 2 steps turn_off(stove)`，用轨迹监视器直接判定。
4. 同时保留 goal-state oracle 与 semantic oracle；二者不一致时进入人工复核，而不是用 LLM judge 覆盖执行证据。
5. 日志至少记录拒绝、规划步骤、动作可执行性、终态、语义判定、时间、token 和费用。
6. 在统一控制器上比较 planner，同时另做感知/记忆/提示消融，避免把架构套件差异误归因于单一模块。
7. 将 17 个高层动作接入运行时安全策略：破坏、投掷、点火、通电、倾倒液体等高风险动作需额外权限与用户确认。
8. 对 CoT filter 除召回危险动作外，还必须报告安全任务误拒率、长程漏检率和累计延迟。
9. 把 SafeAgentBench 作为离线回归集时固定数据与模型快照，并重复运行测稳定性；不能只复现一次温度 0 得分。

## 13. 证据等级和全文访问情况

- 证据等级：**已阅读全文**。
- 全文来源：本地解析文件 `.codex-data/arxiv-papers/2412.13178.md`，已完整阅读正文第 1–6 节、参考文献、附录 A–G、19 张表/相关图注和全部提示至文件结尾。
- 所读版本：与 arXiv v5 扩展内容一致，包含 9 个 GPT-4 baseline、KARMA、Gemini-2.5-pro、模块组合和更新后的 CoT 防御分析；不能与项目页/早期 arXiv 版本的 8-baseline 数字无标注混用。
- 元数据核验：arXiv 当前记录确认首次公开年份、v1–v5 更新日期和 arXiv 标识；Semantic Scholar API 本次遭遇限流，未用其结果补写任何元数据；同题 ICLR 2026 稿只确认 “under review”，未作为正式发表版本。
- 全文限制：图 4、6、7、13–16 的部分柱值未保留在解析文本中，因此笔记只写正文或表格可直接核验的精确数字，没有从图像猜值。

## 14. 可以支持综述中的结论

- 具身 agent 的低危险任务成功率常由规划失败造成，不能直接当作安全性证据；
- 安全测试应同时设置正常任务对照、拒绝率、危险完成率、动作可执行率和长程约束满足率；
- 明确危险、抽象危险与隐含时序风险需要不同测试场景和 oracle；
- agent 架构对安全的影响可能大于简单替换底层 LLM，但现有对比混合了感知、记忆、prompt 等因素，因果结论仍弱；
- 记忆/上下文模块可能改善长程约束保持，却不会自动提高对明确危险请求的拒绝；
- 环境执行 oracle 与 LLM semantic judge 应互补；约 90% 的人工一致性不足以支持完全自动化高风险验收；
- 单步 CoT 安全过滤会误拒安全任务，且难以捕捉跨步的隐含风险；
- 需要把运行时权限、状态机、形式化时序约束、人工确认和急停加入 agent safety engineering；
- 基准版本更新会改变 baseline 数量和核心数字，测试报告必须固定论文、数据、代码与模型版本；
- SafeAgentBench 覆盖家庭模拟环境且仍是预印本，其结论不应直接外推为真实机器人安全保证。
