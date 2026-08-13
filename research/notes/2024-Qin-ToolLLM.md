# ToolLLM：结构化阅读笔记

## 1. 基本信息

- **标题**：ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs
- **作者**：Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, Maosong Sun
- **年份**：2024（正式发表）；arXiv 首发于 2023
- **会议或期刊**：International Conference on Learning Representations（ICLR 2024）
- **DOI**：未核验到正式 DOI，不猜测
- **arXiv ID**：2307.16789
- **正式版本和预印本关系**：本地 PDF 是 arXiv v2（2023-10-03），首页仍标作 preprint；同题同作者工作随后正式发表于 ICLR 2024（OpenReview ID `dHng2O0Jjr`）。引用身份应优先使用 ICLR 2024，arXiv 作为公开全文入口。
- **代码、模型和数据**：<https://github.com/OpenBMB/ToolBench>

## 2. 研究问题

论文研究如何让开源 LLM 在包含上万种真实 REST API 的开放工具空间中完成单工具和多工具任务，并建立相应的训练、检索、推理和自动评测链。具体包括：如何从动态 API 市场构造训练数据；如何搜索可执行的多步 solution path；如何从 16K 余 API 中检索候选；如何评价不存在唯一参考轨迹的工具调用结果；以及训练所得模型能否泛化到未见 instruction、tool、category 和外部 API 数据集。

## 3. 被测试的智能体类型

- 基于 LLM 的单智能体，通过自然语言 thought、API 名称和参数进行多轮真实 API 调用。
- 工具选择型 agent：完整系统先用 API retriever 选出候选 API，再由 ToolLLaMA 规划和执行。
- 工具链可包含单个工具内多 API，或跨 2–5 个工具的多工具组合。
- 不涉及浏览器 GUI、长期个人状态、多智能体协作或物理具身；第三方 API 调用是真实网络服务而非完全受控模拟器。

## 4. 测试或评估方法

ToolLLM 是四层联合系统（图 1、第 2–3 节）：

1. **ToolBench 构造**：从 RapidAPI 收集/过滤 API，用 ChatGPT 生成 instruction 与相关 API，再通过真实调用标注 solution path。
2. **API Retriever**：Sentence-BERT 风格双编码器在 instruction/API 文档对上训练，输出 top-5 API。
3. **ToolLLaMA 与 DFSDT**：LLaMA-2-7B 经 ToolBench 微调；推理可用 ReAct 或 depth-first search-based decision tree。DFSDT 在错误分支上调用 “Finish by Giving Up” 回退，再生成不同子节点。
4. **ToolEval**：ChatGPT judge 判断 Pass/Fail/Unsure，并将候选轨迹与 ChatGPT-ReAct 参考轨迹做 pairwise win/lose/tie；每个判定至少生成四次后多数投票（附录 A.5）。

ToolEval 的 “Pass” 不完全等于现实任务已达成：当 API 不可用且 agent 已充分尝试，适当放弃或如实拒绝也可判 Pass；因此该指标同时衡量完成和合理处理工具不可用。

## 5. 数据集、环境或基准

- 初始从 RapidAPI 抓取 **10,853 个工具、53,190 个 API**，按可运行性、响应时间和响应质量过滤后保留 **3,451 个工具、16,464 个 API、49 个类别**（第 2.1 节、附录 A.1）。
- 生成近 200K 条 instruction/API 对：单工具 I1 为 87,413，类别内多工具 I2 为 84,815，collection 内多工具 I3 为 25,251（第 2.2 节）。
- 仅保留 DFSDT 找到可通过 solution path 的样本，最终 ToolBench 有 **126,486 个 instruction–solution path 对**、469,585 次真实 API 调用，平均每例约 4 条 reasoning traces（表 1）。
- 泛化测试分为未见 instruction、未见同类 tool、未见 category；I1、I2、I3 可用的层级不同（第 3.2 节）。
- 外部分布测试使用 APIBench 的 HuggingFace、TorchHub 和 TensorHub 三域（第 3.3 节）。

## 6. 评价指标

- **Pass Rate**：在有限预算内被 ToolEval 判为完成或合理处置不可解/不可用工具的比例。
- **Win Rate**：与 ChatGPT-ReAct 轨迹成对比较，综合信息丰富度、事实性、失败解释、milestone、探索和重复调用成本；主表将 tie 对半分配给 win/lose。
- **API 检索**：NDCG@1、NDCG@5。
- **APIBench**：AST accuracy 与 hallucination rate。
- **评测器效度**：ToolEval 与人工标注的一致率；Pass 为 87.1%，Win 为 80.3%（第 3.1 节、附录 A.5）。
- 没有直接报告参数级 exact match、每步状态正确率、真实延迟、货币成本分布、安全性或重复运行置信区间。

## 7. 实验设计

- 主比较包括 ChatGPT、GPT-4、Claude-2、Text-Davinci-003、Vicuna、Alpaca 和 ToolLLaMA，并分别套用 ReAct/DFSDT；Vicuna、Alpaca 无论 ReAct/DFSDT 均未通过。
- 除 `ToolLLaMA-DFSDT-Retriever` 外，表 4 方法都获得 ground-truth/oracle API 集；Retriever 行才反映完整自动工具发现。
- DFSDT 与 ReAct 的公平性对照加入 `ReAct@N`，重复 ReAct 直到调用成本接近 DFSDT（第 3.1 节）。
- ToolLLaMA 基于 LLaMA-2-7B，位置插值把上下文从 4,096 扩到 8,192；学习率 `5e-5`、warmup ratio `0.04`、总 batch 64、训练 2 epochs，选开发集最佳 checkpoint（附录 A.3）。
- 过长 API response 先按 ChatGPT 生成的 schema 压缩；若仍超过 1,024 tokens，仅保留前 1,024 tokens（附录 A.2）。
- APIBench OOD 测试不再训练 ToolLLaMA，比较自有/Oracle retriever 与 Gorilla 的 ZS/RS 配置。

## 8. 主要发现

1. **检索质量显著高于文本基线。** 表 2 中自有 retriever 的平均 NDCG@1/@5 为 78.0/84.9，OpenAI Ada 为 49.6/45.4，BM25 为 18.5/17.0；I2 多工具检索仍最难。
2. **搜索策略强烈影响“模型能力”分数。** 表 3 中 ChatGPT 的平均 Pass：ReAct 35.3、同预算 ReAct@N 44.5、DFSDT 63.8。收益在 I2/I3 更明显，说明单轨迹错误传播和探索不足是重要瓶颈。
3. **主表中 ToolLLaMA 接近 ChatGPT，但条件严格。** 表 4 的平均 Pass/Win：ChatGPT+DFSDT 64.8/64.3，ToolLLaMA+DFSDT 66.7/60.0，完整 Retriever 版本 67.3/63.1；GPT-4+DFSDT 为 71.1/70.4。比较依赖同一 ToolEval、DFSDT 和相对 ChatGPT-ReAct 的 Win，不应泛化成“所有工具任务上等同 ChatGPT”。
4. **Oracle API 与自动检索的关系不单调。** ToolLLaMA top-5 retriever 版略高于 ground-truth API 版；作者解释检索器可能找到功能更好、可替代的 API，说明生成时标注的“相关 API”不是唯一 gold。
5. **未见工具/类别仍有一定泛化。** ToolLLaMA+DFSDT 在六个设置的 Pass 为 57.0–77.0；但这些结果仍使用提供的 API 文档，且多数行使用 oracle API 集。
6. **APIBench 上检索成为主要瓶颈。** 表 5 中 ToolLLaMA+自有 retriever 的 AST accuracy 为 HuggingFace 16.77、TorchHub 51.16、TensorHub 40.59；换 Oracle 后分别为 88.80、85.88、88.62。模型能读文档不代表能从巨大候选池找到正确 API。
7. **评测主观性仍明显。** 附录 A.5 指出人类也会在“少调用快速回答”与“多调用交叉验证”之间产生偏好分歧；80.3% Win 一致率意味着 LLM judge 不能视为无误 oracle。

## 9. 局限性

论文未设独立 limitations 节，以下边界来自正文和附录：

- instruction、相关 API 与 solution path 主要由 `gpt-3.5-turbo-16k` 自动生成，只有少量 seed/抽检；训练分布继承 teacher 的表达、规划和安全偏差。
- 仅保留搜索成功的轨迹，产生 selection bias：训练数据系统性排除了困难、API 永久失效和无解任务。
- RapidAPI 服务会下线、限流、改 schema 或改变响应；真实调用增强现实性，却削弱长期复现并引入隐私、认证与供应链风险。
- ToolEval 是与被评 agent 同类的 ChatGPT judge，人工一致率不是 100%；Win 还以 ChatGPT-ReAct 为相对基线，受位置、冗长偏好和 judge 版本影响。
- “充分探索后放弃”可 Pass，使 Pass Rate 与严格任务成功率含义不同。
- API response 压缩和 1,024-token 截断可能删除后续规划所需字段；论文只称人工检查保留重要信息，没有给出系统性损失率。
- 主表大多数设置给 oracle API；完整端到端检索难度可能被低估。
- 未评估错误写操作、权限越界、恶意 API 输出、数据泄露、调用费用和尾延迟。

## 10. 可复现性信息

- **代码/模型/数据**：ToolBench 仓库公开代码、checkpoint、retriever、demo 和构造数据。
- **API 元数据**：工具层级、文档字段和过滤过程有说明，但第三方响应无法冻结。
- **提示**：附录 A.7 给出 instruction generation 提示与 seed 示例；附录 A.5 给出 ToolEval 规则；附录 A.8 给出 DFSDT 流程。
- **训练**：附录 A.3 报告模型、上下文扩展、学习率、batch、warmup、epoch 和 checkpoint 选择。
- **评测**：I1/I2/I3、泛化拆分、oracle/retriever设置及主表基线明确；ToolEval 每例至少四次多数投票。
- **主要缺口**：未锁定全部 API 响应/版本、judge API snapshot、随机种子、总调用费用、硬件和多次运行置信区间。

## 11. 与“智能体测试”研究的关系

ToolLLM 展示了工具智能体不能只测试函数名：工具检索、参数生成、响应理解、长链回退和最终答复共同决定结果。DFSDT 与 ReAct 的巨大差异也说明 benchmark 分数是基础模型与 agent search scaffold 的联合属性。ToolEval 则是轨迹级 LLM judge 的早期代表，但其规则和一致率同时说明自动 judge 必须被校准、版本化并辅以确定性检查。

## 12. 可借鉴的工程实现

- 将测试流水线拆成 retrieval、schema/argument validation、execution、response parsing、planning、termination 六层并分别计分。
- 对错误分支保留可回退搜索树；记录分支数、重复调用、回退原因和调用预算。
- 给 API response 做结构化裁剪前运行字段依赖分析，并记录被删除键，避免静默信息损失。
- 构建 live API 与录制响应双模式：前者测现实漂移，后者做稳定回归。
- 将成功、合理拒绝、工具不可用和错误放弃设为不同标签，不合并成一个 Pass。
- 对 LLM judge 固定模型、提示和重复次数，保存逐次判决；定期用多人样本校准。
- 增加恶意响应、schema 漂移、限流、超时、越权 API 和高费用工具的故障注入。

## 13. 证据等级和全文访问情况

- **证据等级：已阅读全文。**
- **全文来源**：本地 PDF `research/papers/2024-Qin-ToolLLM.pdf` 及解析文本 `/tmp/agent-review-text/2024-Qin-ToolLLM.txt`。
- **阅读范围**：正文第 1–5 节、表 1–5、图 1–4；附录 A.1–A.8 的 API 过滤/压缩、训练参数、DFSDT、ToolEval、人类一致性、APIBench 和提示。
- **版本核验**：ICLR 2024 正式身份通过官方 OpenReview 记录核验；详细实验结论来自本地全文，不由摘要推断。
- **全文限制**：无论文访问限制；历史 RapidAPI 和闭源 ChatGPT 服务状态无法静态重放。

## 14. 可以支持综述中哪些结论

- 工具 agent 测试必须覆盖工具发现、参数、执行、响应解释和多步恢复，而不仅是 API 名称准确率。
- 搜索/回退策略可比更换基础模型产生同量级影响，测试必须披露 agent scaffold。
- LLM-as-a-Judge 可扩展轨迹评测，但其人类一致性和判分定义需要单独验证。
- 动态第三方 API 带来版本、延迟、可用性、权限和供应链测试问题。
- Oracle API 设置可能显著高估完整工具智能体能力。
- 当前工具基准对安全副作用、真实费用、响应漂移与不可复现性覆盖不足。
