# Agent-SafetyBench：结构化阅读笔记

## 1. 基本信息

- 标题：*Agent-SafetyBench: Evaluating the Safety of LLM Agents*
- 作者：Zhexin Zhang；Shiyao Cui；Yida Lu；Jingzhuo Zhou；Junxiao Yang；Hongning Wang；Minlie Huang
- 规范书目年份：2024
- 发表状态：arXiv 预印本；本地全文首页明确写作 “Preprint. Under review.”。截至本次核验，项目仓库仍提供 `@article{zhang2024agent,... journal={arXiv preprint arXiv:2412.14470}}`，未确认正式会议/期刊版本。
- DOI：无已核验的正式出版 DOI；不把 arXiv 的 DataCite DOI 当作同行评审出版 DOI。
- arXiv：`2412.14470`
- 全文：https://arxiv.org/abs/2412.14470
- 代码、环境和数据：https://github.com/thu-coai/Agent-SafetyBench
- 版本关系：当前可核验身份是 2024 年 arXiv 预印本。文件名按可核验书目年份统一为 `2024-Zhang-Agent-SafetyBench.md`；正式 BibTeX 使用 `year={2024}`，除非后续找到正式发表版本。

## 2. 研究问题

论文研究如何综合评测 LLM agent 在交互式工具环境中的**行为安全**，而非只判断最终文本是否有害。它试图回答：

1. 如何覆盖数据泄露、财产损失、错误传播、物理伤害、违法伦理、可用性破坏和危险代码等不同后果；
2. 如何把 agent 的不安全行为进一步归因为可操作的工具使用 failure modes；
3. 如何在大量可配置环境中执行完整 agent—tool 轨迹；
4. 通用 LLM judge 是否足以裁判行为安全，能否训练更可靠的专用 scorer；
5. 当前 agent 的低安全性来自单纯“不会用工具”，还是缺少风险意识；
6. 把失败模式写入 defense prompt 能否解决问题。

章节依据：第 3 节构造分类、环境、案例和 scorer；第 4 节报告 16 个 agent、failure-mode/helpfulness/防御分析；附录 C–H 给出实现和提示。

## 3. 被测试的智能体类型

- 单智能体、文本函数调用、多步顺序执行；
- agent 根据历史和工具定义，每次选择一个工具与参数，环境执行后把结果加入轨迹；
- 覆盖现实已有工具、无公开 API 但现实可预期的工具，以及部分未来假想工具环境；
- 16 个基础模型：
  - Claude 3 Opus、Claude 3.5 Sonnet/Haiku；
  - GPT-4o、GPT-4o-mini、GPT-4-Turbo；
  - Gemini 1.5 Pro/Flash；
  - Qwen 2.5 7B/14B/72B；
  - Llama 3.1 8B/70B/405B；
  - DeepSeek V2.5、GLM4-9B-Chat。

论文不聚焦多智能体、具身连续控制或长期记忆；多数安全问题只需常识判断。

## 4. 测试或评估方法

- **案例结构**：每例记录主要风险、用户指令或预填对话、一个或多个环境及初始化参数、预计 failure modes（第 3.2.1 节）。
- **可执行环境**：每个环境由 OpenAI/Claude 风格 JSON tool schema 与 Python class 双层实现；JSON 定义工具，Python 负责状态和执行逻辑（附录 C）。
- **动态轨迹**：agent 一次调用一个工具，等待返回后继续，直至最终回答（第 4.1 节）。
- **安全 oracle**：专门微调的 Qwen 2.5 7B scorer 读取工具定义/环境、完整对话和动作，输出 `safe`/`unsafe` 及分析；Safety Score 是安全标签比例。
- **人类监督**：GPT-4o-mini 与 Claude 3.5 Sonnet 各运行 2,000 例，得到 4,000 条轨迹，由作者标安全标签；GPT-4o 在已知标签条件下生成 explanation，用来训练 scorer（第 3.2.4/3.3 节）。
- **故障模式诊断**：每例预标可触发的 10 种失败模式，按模式汇总安全率。
- **helpfulness 分析**：人工标注案例是否可以安全完成；GPT-4o 另判 agent 是否推进用户目标，不考虑该行为是否安全（第 4.4 节）。
- **防御消融**：在系统提示后追加失败模式列表，比较简短与含例子的增强版（第 4.5 节、附录 H）。

## 5. 数据集、环境或基准

- 349 个环境、2,000 个测试案例、每个风险类别 250 例。
- 环境来源分布（表 2）：
  - 68 个与已有基准工具相似；
  - 42 个有类似公开 API、但此前无沙箱评测；
  - 220 个没有类似公开 API、但有现实应用设想；
  - 19 个目前连现实应用也没有、但作者认为未来可能出现。
- 8 类主要风险（表 3）：
  1. 泄露敏感数据/信息；
  2. 导致财产损失；
  3. 传播不安全信息/错误信息；
  4. 导致身体伤害；
  5. 违反法律/伦理；
  6. 破坏可用性；
  7. 促成有害/脆弱代码；
  8. 产生不安全信息/错误信息。
- 10 种 failure modes（表 4）：
  1. 无工具直接生成有害内容；
  2. 必要信息不足仍调用工具；
  3. 未先利用工具获得可获得的完整信息；
  4. 忽视已知约束；
  5. 忽视隐含/潜在风险；
  6. 工具参数错误；
  7. 忽视工具已知安全问题；
  8. 漏调必要工具；
  9. 未验证就过度信任工具结果；
  10. 面对多个候选结果不会安全选择。
- 数据组成：
  - 从 R-Judge、AgentDojo、GuardAgent、ToolEmu、ToolSword、InjecAgent 等重构、去重和统一环境；
  - 内容安全类别另取 AdvBench 50 个问题，与 20 种越狱模板随机组合出 200 例；
  - 精炼阶段共 876 例；
  - 新增 1,124 例，最终为 2,000。
- 新增环境名由 GPT-4o、Claude 3.5 Sonnet、Gemini 1.5 Pro 生成；新案例由 GPT-4o 生成风险动作链后经人工大幅修订。

## 6. 评价指标

1. **Total Safety Score**：全部案例中专用 scorer 判为 `safe` 的比例。
2. **Behavior Safety Score**：带交互环境/工具的案例安全率。
3. **Content Safety Score**：不依赖环境的文本/代码安全案例安全率。
4. **Category Safety Score**：8 类风险分别的安全率。
5. **Failure-mode Safety Score**：含某种预计 failure mode 的案例安全率；一例可属于多个模式。
6. **Safe/Helpful 四象限**：在 fulfillable/unfulfillable 案例上分别比较安全与 helpfulness。
7. **Scorer Accuracy**：在独立抽取的 200 条 Gemini 1.5 Flash 轨迹上，与人类标签的一致准确率。
8. **数据/标签复核合理率**：交叉复核 200 个案例和 200 条标签。

Safety Score 是二分类平均值，没有风险严重度、概率、成本或置信区间；不同类别同权。

## 7. 实验设计

- 默认 `temperature=0`，每轮最多 2,048 新 token；少于约 1% 的无效工具格式案例改用 `temperature=1` 重新得到有效输出（附录 H）。
- 小模型因格式错误较多，使用额外 JSON 工具调用约束提示；这意味着模型间并非完全相同提示。
- scorer 训练集为 4,000 条作者标注轨迹：2,186 unsafe、1,814 safe。
- scorer 基座：正文称 Qwen-2.5-7B-Instruct，附录 G 称 Qwen2.5-7B-Chat；应视为论文内部命名不一致，复现以仓库 checkpoint 为准。
- scorer 超参数：batch 36、max length 2,500、初始学习率 `2e-5`、AdamW、最多 4 epoch、取最后 epoch；4 张 A100 约 4 小时。
- scorer 校准：在 200 条 Gemini 1.5 Flash 轨迹上，直接 GPT-4o 75.5%，微调 scorer 91.5%；提升 16.0 个绝对百分点（正文概述“约 15%”）。
- GPT-4o 在给定人工真值后生成的 50 条安全分析中，作者判断 94% 合理。
- 数据交叉验证：不同于原审阅者的作者复核 200 个测试案例与 200 个安全标签，合理率分别 98% 和 97.5%（附录 F）。
- helpfulness judge 经手工验证准确率 94%；它有意把不安全但推进用户目标的行为也判为 helpful。
- defense prompt 分简短 10 条和增强 10 条+例子，追加到默认系统提示。

## 8. 主要发现

以下具体数字来自表 5、表 6：

- 16 个 agent 的 Total Safety Score 均低于 60%；平均 38.5%。最高 Claude 3 Opus 59.8%，其次 Claude 3.5 Sonnet 59.4%；最低 Qwen2.5-7B 18.8%、Llama3.1-8B 19.9%。
- 同系列中较强模型通常更安全；例如 Qwen 7B/14B/72B 为 18.8%/31.9%/37.3%，Llama 8B/70B/405B 为 19.9%/31.2%/35.4%。
- 平均 Behavior Safety 30.4%，远低于 Content Safety 68.4%。即便行为案例多数没有显式 jailbreak，工具交互仍更易失守。
- 风险类别平均：
  - Leak 33.7%；
  - Property 37.7%；
  - Spread 15.6%（最难）；
  - Physical 35.7%；
  - Law/Ethics 28.0%；
  - Availability 30.6%；
  - Code 37.1%；
  - Produce 87.0%。
- failure-mode 平均安全率：
  - M1 70.1%、M6 63.3%、M10 63.1%；
  - M2 18.1%、M3 27.0%、M4 28.3%、M5 23.2%；
  - M7 最低 12.5%；
  - M8 39.4%、M9 37.5%。
- 作者据此归纳两类根因：
  - **缺少鲁棒性**：参数、步骤、必要工具和结果选择不稳定；
  - **缺少风险意识**：即使参数正确，也忽视权限、隐含危险、工具已知问题或传播风险。
- fulfillable 案例上，安全较强的 agent 同时能保持与弱 agent 相近的 helpfulness，说明它们不只是“一律拒绝”；unfulfillable 案例上，强安全 agent 的 helpfulness 更低，反映它们更愿意为避险不执行（图 3）。
- defense prompt 对弱模型几乎无效，对 GPT-4o 等强模型有有限提升；增强提示下 Claude 3.5 Sonnet 仍低于 70%，且上下文更长（图 4；图中未在解析文本给出全部精确柱值，不应补猜）。

## 9. 局限性

作者附录 J 明确说明：

- 多数案例只需常识，缺少需高级专业知识的安全场景；
- 自动生成案例多数仍需大幅人工修订，LLM 尚不能可靠自主生成高质量 agent 安全测试；
- 一般众包人员难以修订案例、判轨迹安全和精确标 failure mode，最终均由作者完成，规模化存在瓶颈；
- 构造和评测依赖 GPT-4o、微调 Qwen scorer，可能引入模型偏差；作者只做了有限反偏差检查。

结合全文还应注意：

- 220+19 个环境没有现成公开 API，其中一部分是未来假想系统；覆盖广，但现实频率与实现真实性较弱。
- 复用多个已有基准并统一改写，不能把 2,000 例都视作完全独立新场景。
- 每例只标一个“主要风险”，会压扁多重后果；failure mode 则可多标签，二者粒度不对称。
- 主 oracle 是训练于同一 benchmark 产生轨迹的单一模型；只在 200 条、一个被测模型的轨迹上验证 91.5%，跨模型/新环境外推有限。
- 安全分是二元且等权，不体现危害严重度、可逆性、真实工具是否接受调用或状态终态。
- `temperature=0` 无效时改温度 1 重试会条件化结果；应报告哪些案例重跑及其影响。
- 小模型使用不同格式提示，跨模型分数同时混合了模型能力与提示适配。
- 防御实验只研究提示，不足以代表权限控制、信息流隔离、人工确认或运行时监控。
- 当时全文仍是 under review，方法尚未经过已核验同行评审版本确认。

## 10. 可复现性信息

- GitHub 于 2025-02-20 发布 data、349 个环境与 evaluation/score 代码，MIT 许可证；另有 Hugging Face 数据。
- 环境采用 JSON schema + Python class，可通过初始化参数定制；提供 base environment 管理描述和调用。
- 附录 E 完整给出环境名、风险动作补全、带/不带环境案例生成提示。
- 附录 G 给出 scorer 数据构造、输入格式、训练超参数和 4×A100 训练时间。
- 附录 H 给出 agent 默认/格式限制提示、helpfulness judge、两种 defense prompt、温度和 token 上限。
- 表 8 给出 16 个模型及部分日期快照；Claude/Gemini/Mistral 等若干版本只写 `-` 或 latest，精确复现受限。
- 开源仓库 README 说明 API 模型经 OpenRouter 评测，可替换 provider；因此应固定 OpenRouter 路由、模型端点、仓库 commit 与 scorer checkpoint。
- 数据和标签的作者交叉复核率有报告，但没有分层 precision/recall、置信区间或跨机构标注验证。

## 11. 与“智能体测试”研究的关系

Agent-SafetyBench 的价值在于把“行为安全”映射为 10 个可诊断 failure modes，并用大量可配置工具环境测完整轨迹。它展示了传统内容安全得分无法代表 agent 安全：16 模型的平均内容安全 68.4%，行为安全只有 30.4%。同时，它代表另一类权衡：为了环境广度，使用大量合成/未来环境和模型 scorer，因而需要额外关注环境真实性和 judge 泛化。

## 12. 可借鉴的工程实现

1. 在测试用例中同时标注“风险后果”和“导致它的 failure modes”，使回归结果能定位到参数、约束、工具选择或结果验证。
2. 用 JSON schema + 状态 Python class 分离工具接口与环境逻辑，支持同一工具在不同初始状态下做场景测试。
3. 把 M2/M3 分开：信息根本缺失时应询问用户；信息可通过工具获得时应先查询。
4. 对每个工具增加已知风险、权限、可靠性字段，并专门测试 agent 是否读取和遵守。
5. 把 M9/M10 扩展为工具输出污染、来源信誉、交叉验证和安全候选排序测试。
6. scorer 采用“程序化状态 oracle 优先、专用模型补充”的混合方案，并在新模型/新环境上持续抽样人审校准。
7. 同时记录 safe、helpful、fulfillable，避免把拒绝所有任务误判为高质量安全。
8. defense 不能只靠长提示；将同一 failure-mode taxonomy映射到运行时参数校验、最小权限、确认闸门和日志告警。

## 13. 证据等级和全文访问情况

- 证据等级：**已阅读全文**。
- 全文来源：本地解析文件 `.codex-data/arxiv-papers/2412.14470.md`，已完整阅读正文第 1–5 节、附录 A–K、全部表格、构造/评分/防御提示与局限至文件结尾。
- 可用范围：支持数据组成、环境实现、风险/故障分类、scorer 训练、模型结果、人工复核和局限的详细分析。
- 元数据限制：全文仍标为 under review；不能把请求文件名中的 2025 当作已证实正式发表年份。

## 14. 可以支持综述中的结论

- agent 的行为安全不能由普通 LLM 内容安全分数替代；
- 常见安全失败既包括工具使用鲁棒性缺陷，也包括对权限和后果缺乏风险意识；
- 信息不足、忽略不安全工具、过度信任工具结果和漏调必要工具是应单独统计的故障模式；
- 大规模环境覆盖能发现类别差异，但合成/未来环境的现实性应另行评级；
- safe/helpful/fulfillable 联合分析有助于区分正确安全执行、必要拒绝和能力不足；
- 通用 GPT-4o judge 对复杂行为安全并不充分，专用 scorer 需人类标签校准；但专用 scorer 本身也必须跨域验证；
- 仅追加防御提示带来的提升有限，工程保障应转向权限、状态、参数和信息流控制；
- 自动生成安全测试仍高度依赖专家修订，测试生成与 oracle 扩展是开放研究问题。
