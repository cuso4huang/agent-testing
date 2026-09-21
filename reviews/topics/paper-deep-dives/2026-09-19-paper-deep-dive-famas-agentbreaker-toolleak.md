# 三篇“直接测试智能体”论文精读：FAMAS、AgentBreaker 与 ToolLeak

> 核查日期：2026-09-19（Asia/Shanghai）  
> 口径：只讨论把智能体/多智能体系统本身当作被测对象的工作。  
> 证据标签：**[全文]**=已检查开放 PDF；**[官方摘要]**=会议官方页，只能支持摘要层结论；**[制品]**=作者公开 artifact 的 README/源码；**[批判性分析]**=本文基于证据作出的判断，不是作者原话；**[研究设想]**=后续可做的新工作。

## 证据与版本状态

| 论文 | 正式状态 | 本轮证据 | 核查结果 |
|---|---|---|---|
| **Spectrum-Based Failure Attribution for Multi-agent Systems**（预印本题名：*Who is Introducing the Failure? Automatically Attributing Failures of Multi-Agent Systems via Spectrum Analysis*，简称 **FAMAS**） | FSE 2026 Research Paper；正式 DOI `10.1145/3797113` | [FSE 官方页](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/205/Spectrum-based-Failure-Attribution-for-Multi-Agent-Systems)、[arXiv:2509.13782 全文](https://arxiv.org/pdf/2509.13782) | **全文已检查、元数据已核验**。Crossref 与 OpenAlex 的 DOI 精确查询一致确认正式题名、作者、PACMSE 与 DOI；OpenAlex 标记 published version 为 CC BY/hybrid OA，另有可直接读取的 arXiv 全文。 |
| **AgentBreaker: Evaluating Context-Aware Indirect Prompt Injection Risks in Modern Web Agents** | ISSTA 2026 Research Paper；会议将在 2026-10-08 报告，官方页面仍标注 program tentative | [ISSTA 官方摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/74/AgentBreaker-Evaluating-Context-Aware-Indirect-Prompt-Injection-Risks-in-Modern-Web-)、[Figshare artifact v2](https://doi.org/10.6084/m9.figshare.32835578.v2)、[Zenodo artifact](https://doi.org/10.5281/zenodo.21063932) | **未发现论文开放全文**；下述 Problem/Gap/官方结果只用官方摘要，算法实现细节只用公开制品源码，不把制品检查冒充全文精读。尚无可靠论文 DOI；artifact DOI 不能当作论文 DOI。 |
| **Red-Teaming Coding Agents from a Tool-Invocation Perspective: An Empirical Security Assessment**（核心漏洞简称 **ToolLeak**） | ISSTA 2026 Research Paper；会议将在 2026-10-08 报告，program tentative | [ISSTA 官方页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/176/Red-Teaming-Coding-Agents-from-a-Tool-Invocation-Perspective-An-Empirical-Security-A)、[arXiv:2509.05755v6 全文](https://arxiv.org/pdf/2509.05755v6) | **全文已检查**。版本有两个小冲突：arXiv v6 列 10 位作者，ISSTA 当前页列 12 位；arXiv 摘要称 19/25 组合出现泄漏，论文正文/官方摘要称 18/25 组合上 ToolLeak 的 pseudo-recall 为所有方法最佳——两者指标不同，并不直接矛盾。 |

---

## 1. FAMAS：用“多次重跑的行为频谱”定位多智能体系统里谁做错了哪一步

### Problem：解决什么？

多智能体系统失败后，开发者不只想知道“任务失败”，还要知道：**哪个 agent 的哪一个 action 把系统推进了决定性错误状态**。FAMAS 把目标形式化为在失败轨迹中找出 decisive error 对应的 `⟨agent, action, resulting state⟩` 三元组，并同时给出 agent-level 与 action-level 排名。它解决的是 failure attribution / fault localization，不是测试输入生成，也不是一般性的最终答案评分。**[全文：§1–2](https://arxiv.org/pdf/2509.13782)**

### Gap：以前为什么解决不了？

1. MAS 日志同时包含 agent-agent、agent-tool 与模型内部推理交互，长且复杂；action 和 state 又以自然语言记录，语义等价行为可能有不同表述。传统基于代码覆盖的定位方法不能直接拿来用。**[全文：§1](https://arxiv.org/pdf/2509.13782)**
2. 细粒度 benchmark 只是提供更多评分维度，真正归因仍依赖人工。已有 LLM-as-a-judge 方法直接读日志做判断，但论文报告先前 action-level attribution 不到 10%，长轨迹上尤其困难。**[全文：§1、§7](https://arxiv.org/pdf/2509.13782)**
3. 传统 SBFL 只有“组件是否被覆盖”的二元谱，而 MAS 中同一 agent/action 可反复出现、不同 agent 活跃度差异很大，直接套 Ochiai/Tarantula 等公式会丢掉关键频率和角色信息。**[全文：§2.3、§4.2](https://arxiv.org/pdf/2509.13782)**

### Insight：作者最关键的想法？

最关键的类比是：**一次失败轨迹相当于一个 failing test；把同一任务重复运行得到的成功/失败轨迹相当于测试套件；一个 action 若在失败运行中反复出现、在成功运行中较少出现，就更可疑。**

也就是说，作者没有继续让一个 LLM“凭阅读理解猜 root cause”，而是把 agent 行为变成可统计的 spectrum，再把经典 spectrum-based fault localization 移植到 MAS。为避免“活跃 agent 天然覆盖多、重复 action 天然计数高”的偏差，又同时建模 agent activation 与 action activation。**[全文：§1、§3–4](https://arxiv.org/pdf/2509.13782)**

### Technique：怎么实现？

流程分两阶段：

1. **Trajectory replay & abstraction**
   - 对原始失败任务再独立运行 `k` 次；默认 `k=20`，得到原失败日志加若干成功/失败 counterpart logs。
   - 把每条长日志切成可处理的小块，用 **Qwen2.5-72B** 抽取规范化的 `⟨AGENT, ACTION, STATE⟩`。
   - 先按 agent identifier 分组，再让 LLM 按 action-state 语义相似性做层次聚类，把表述不同但语义等价的行为合并成代表三元组。**[全文：§4.1、§5.1](https://arxiv.org/pdf/2509.13782)**

2. **Spectrum analysis**
   - 在 action-triple 和 agent 两个粒度分别构造 coverage matrix、frequency matrix，并记录每条轨迹成功/失败的 outcome vector。
   - 对每个三元组计算四类量：agent 维度的 action coverage ratio `γ` 与 action frequency proportion `β`；action 维度的全局 `λ`-decay SBFL 系数与失败轨迹内的 local frequency enhancement `α`。
   - 以 Kulczynski2 为底座，组合成 `S(η)=α·Kulczynski2_λ·(1+β)·(1+γ)`；默认 `λ=0.9`，最后按 `S` 降序，以无并列的 top-1 作为归因结果。**[全文：§4.2，Eq. 2–8](https://arxiv.org/pdf/2509.13782)**

### Evaluation：怎么证明有效？

- 数据集是 **Who&When**：184 条人工标注失败日志，来自 127 个 MAS（126 个基于 AG2 自动生成的系统，加 1 个基于 Magentic-One 的手工系统；日志拆分为 126 条自动生成系统日志与 58 条手工系统日志）。每条 ground truth 由 3 位专家经多轮共识标注。**[全文：§5.1](https://arxiv.org/pdf/2509.13782)**
- 比较 **12 个 baseline**：1 个随机方法、6 个 LLM attribution 变体、5 个替换传统 SBFL 公式的 FAMAS 变体。指标是 agent/action 两级严格 top-1 accuracy。**[全文：§5.1、Table 2](https://arxiv.org/pdf/2509.13782)**
- 总体结果：agent-level **57.61%（106/184）**，action-level **29.35%（54/184）**。最强 LLM 变体的 action-level 是 **19.68%**，所以 FAMAS 相对提高 **49.13%**；在 58 条较复杂的手工系统日志上，FAMAS 达到 **62.07% agent-level / 41.38% action-level**。**[全文：§5.2–5.3、Table 2](https://arxiv.org/pdf/2509.13782)**
- 消融表明完整公式正确归因 **106 个 agent / 54 个 action**；只用基础 Kulczynski2 时是 **100 / 39**，去掉任一 `λ/γ/β` 组件都会降低 action-level 命中数，其中去掉 `λ` 后降到 **43**。**[全文：§5.4、Table 3](https://arxiv.org/pdf/2509.13782)**
- 代价很高：单次失败归因平均约 **105 分钟**，范围 **38–248 分钟**；真正的 spectrum calculation 通常不到 1 分钟，瓶颈是 20 次 replay、LLM 抽象与聚类。**[全文：§5.2](https://arxiv.org/pdf/2509.13782)**

### Weakness：哪里还能改？

1. **绝对准确率仍不高。** action-level 只有 29.35%，意味着严格 top-1 下约七成日志仍未找准具体 action；“优于 baseline”不能等同于“已经可直接用于生产诊断”。**[全文事实 + 批判性分析](https://arxiv.org/pdf/2509.13782)**
2. **相关性不等于因果性。** 一个 action 经常伴随失败，可能只是被上游错误迫使出现；频谱无法证明“替换该 action 就会修复失败”。论文的 decisive-error 单根因假设也不覆盖多错误、级联故障或多个 agent 共同致错。**[批判性分析；方法定义见全文 §2.2、§4.2](https://arxiv.org/pdf/2509.13782)**
3. **成本和可重放性。** 每个失败任务重跑 20 次，平均 105 分钟；真实系统可能调用付费 API、改变外部状态，甚至无法安全/确定地重放。**[全文 §5.2 + 批判性分析](https://arxiv.org/pdf/2509.13782)**
4. **外部效度窄。** 只有一个公开 benchmark；127 个系统中只有 1 个手工构建系统。论文还限定 turn-based protocol——每个时间步恰好一个 agent 行动——不直接覆盖并行、异步和事件驱动 MAS。**[全文 §2.1、§5.1、§6.2](https://arxiv.org/pdf/2509.13782)**
5. **抽象器本身可能成为误差源。** 三元组抽取和语义聚类依赖 Qwen2.5-72B，但论文主要消融 suspiciousness formula，没有独立量化“抽取错/聚类错”各自贡献了多少定位误差。**[批判性分析；实现证据见全文 §4.1、§5.1](https://arxiv.org/pdf/2509.13782)**

### My Idea：如果让我继续做，我做什么？

我会做 **Causal-FAMAS：自适应反事实重放的多根因定位**。具体是：

1. 先用 FAMAS 低成本地产生 top-k 可疑 action；
2. 对每个候选保持失败轨迹前缀不变，只对该 action 做 `replace / suppress / resample`，观察最终成功率与下游状态是否改变，以 average treatment effect 而不是共现频率排序；
3. 用 sequential testing / bandit stopping 把重放预算集中到排名不确定的候选，避免固定 20 次全量重跑；
4. 输出因果 failure graph，而不是单个 top-1，显式表示“上游错误 → 下游恢复失败 → 最终失败”的链；
5. 在异步 MAS、不可逆工具调用和真实 API 成本下评估定位准确率、修复后成功率与总成本。

这条路线同时补 FAMAS 的三个短板：**只相关不因果、只支持单根因、重放太贵**。**[研究设想]**

---

## 2. AgentBreaker：生成“适配当前网页语境”的 DOM 间接提示注入

### Problem：解决什么？

AgentBreaker 直接测试现代 web agents 对 **indirect prompt injection（IPI）** 的易感性：攻击者把恶意自然语言嵌入网页 HTML/DOM 元素，agent 读取页面后被诱导去点击攻击者指定元素、发布攻击者文本、泄露内部秘密等，而不是继续完成用户原任务。**[官方摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/74/AgentBreaker-Evaluating-Context-Aware-Indirect-Prompt-Injection-Risks-in-Modern-Web-)**

### Gap：以前为什么解决不了？

既有工作要么是静态攻击 benchmark，要么动态生成一段“通用恶意短语”去骗 agent 内的单个 LLM；它们忽略了两个现实：

- 同一句注入文本放在购物、医疗、政府等不同网页上，可信度和功能语义完全不同；
- 现代 web agent 往往有规划、思考、行动等多个专用 LLM/模块，一次对单模型有效不代表端到端 agent 会真的执行恶意动作。

因此，脱离当前页面和用户任务的 payload 对现代 agent 的 ASR 偏低。**[官方摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/74/AgentBreaker-Evaluating-Context-Aware-Indirect-Prompt-Injection-Risks-in-Modern-Web-)**

### Insight：作者最关键的想法？

**不要生成通用 jailbreak，而要把攻击文本当作网页 UI 文案，针对“当前用户目标 + 当前 DOM 语义 + agent 当前会优先做什么”迭代优化。**

更具体地，AgentBreaker 不只问“payload 能否让一个 LLM说出目标动作”，还让一个 LM Tester 排出 agent 最可能的前五个动作，使用目标恶意 action 的排名变化作为搜索反馈：有效策略保留，无效策略进入负面策略库；当恶意 action 排到第一，再把文本真正注入网页并运行目标 agent 验证。**[制品源码：公开 artifact](https://doi.org/10.6084/m9.figshare.32835578.v2)**

### Technique：怎么实现？

根据公开制品，主循环最多优化 **20 epochs**：

1. **Composer** 根据 user goal、网页 HTML、有效/无效策略库生成 context-aware 恶意 UI 文本；首轮无策略，后续轮次显式吸收已验证有效策略并排除无效策略。
2. **LM Tester** 在相同 user goal 和 DOM 下输出 top-5 actions，并返回 top-1 理由；辅助模型抽取目标恶意 action 的 rank（0–4，不在前五则记 10）。
3. **Strategist/feedback** 根据 top-1 action 及理由生成新的欺骗策略；若新策略让目标排名上升，加入 efficient library，否则加入 inefficient library。
4. 当目标 action 达到 rank 0 时，**Deployer** 把 payload 注入目标 HTML，启动真实 agent；**Evaluator** 检查实际攻击是否成功。若模拟排名第一但真实执行失败，框架会修剪弱策略继续搜索。
5. 制品支持四类目标动作：`CLICK`、`INPUT`、`PROMPT`（秘密泄露）与 `TERMINATE`；可用 GPT-4.1 或 Llama-4-Scout-17B 作为生成/测试模型，辅助排名解析使用 GPT-4.1。**[制品 README 与源码](https://doi.org/10.6084/m9.figshare.32835578.v2)**

这里必须强调：以上循环来自 **artifact source inspection**，不是论文全文；但它与官方摘要“autonomously composes adversarial phrases tailored to page-specific context”的表述相互吻合。

### Evaluation：怎么证明有效？

- 官方摘要报告：在 **Online-Mind2Web 抽样的 60 个网页**、**5 个 SOTA web agents** 上，AgentBreaker 的 ASR 为 **71.7%–100%**；提出的防御把 ASR 降到 **1.7%**，并且 context-aware injection 优于现有 IPI frameworks。**[官方摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/74/AgentBreaker-Evaluating-Context-Aware-Indirect-Prompt-Injection-Risks-in-Modern-Web-)**
- 公开制品包含 60 个页面、攻击代码、agent Docker 镜像、实验脚本和样例日志；但可打包复现的是 **3 agents（YuraScanner、Agent-E、Skyvern）× 4 actions × 2 breaker LLMs**。BrowserOS 与 NanoBrowser 因 headful browser 限制未打包。**[制品 README](https://doi.org/10.6084/m9.figshare.32835578.v2)**
- 制品给出的成本估计：demo 单配置（5 页）约 **30 分钟**，Table 1 的 3×4×2 全部配置约 **12 小时**；单个 defense 配置约 **10 小时**。作者也警告商业 API 和 agent 随机性会导致复现实数波动。**[制品 README](https://doi.org/10.6084/m9.figshare.32835578.v2)**

### Weakness：哪里还能改？

1. **论文全文不可得，评价细节仍有空白。** 仅凭摘要无法核实五个 agent 的具体名称、各 baseline、置信区间、显著性检验、71.7%–100% 的逐配置分布，以及“防御降至 1.7%”的具体 threat model。**[证据限制]**
2. **60 个页面仍偏小，而且来自同一 benchmark 抽样。** payload 是否能跨站点模板、语言、动态 UI、视觉-only 元素、登录态和多轮浏览迁移，摘要没有证明。**[批判性分析；样本事实来自官方摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/74/AgentBreaker-Evaluating-Context-Aware-Indirect-Prompt-Injection-Risks-in-Modern-Web-)**
3. **优化器和被测 agent 可能共享模型偏差。** Composer/LM Tester 若与目标 agent 使用相同或相近模型，可能高估 transfer；如果换成新模型、不同视觉编码或隐藏 action policy，排名代理是否仍可靠需要独立检验。**[批判性分析；制品实现](https://doi.org/10.6084/m9.figshare.32835578.v2)**
4. **测试 oracle 偏 action-centric。** “恶意 action 排第一/被执行”能说明劫持，但未必完整衡量真实损害、权限边界、后续恢复，以及用户是否会看到/阻止动作。**[批判性分析]**
5. **复现门槛高且覆盖不完整。** README 要求至少 100 GB 磁盘、32 CPU cores、GPU 与商业 API key；artifact 只容器化 5 个被测 agent 中的 3 个。**[制品 README](https://doi.org/10.6084/m9.figshare.32835578.v2)**

### My Idea：如果让我继续做，我做什么？

我会做 **Contextual IPI Coverage + Metamorphic AgentBreaker**：

1. 定义上下文攻击覆盖空间：`DOM role × 可见性 × 页面区域 × 用户任务阶段 × action 类型 × 权限等级 × memory/session`；生成器不只追 ASR，还优先覆盖未探索的组合。
2. 对同一页面自动生成语义保持的变体，例如换布局、改无关文案、移动恶意节点、改语言、把文本变成图片/aria-label；用 metamorphic relation 检查“正常任务结果应保持不变、恶意 action 不应突然出现”。
3. oracle 从“是否点击”升级为可观察副作用：数据是否真的外传、表单是否真的提交、权限是否越界、下一轮 memory 是否被污染。
4. 防御与攻击共同进化：每轮用当前 defense 反馈生成 adaptive attack，并同时报告 security、正常任务成功率与延迟，避免只靠把 agent 全部拒绝来取得低 ASR。

这会把 AgentBreaker 从一个强攻击生成器提升为一个可度量覆盖、可回归测试、能比较防御代价的 agent security testing system。**[研究设想]**

---

## 3. ToolLeak / Red-Teaming Coding Agents：工具调用不是“安全的结构化输出”，而是一条新的信息流与控制流攻击通道

### Problem：解决什么？

论文直接红队测试 6 个真实 coding agents——**Cursor、Claude Code、Copilot、Windsurf、Cline、Trae**——的 tool invocation 安全性，目标分两步：

1. 从 agent 隐藏上下文中泄露 system prompt、内置工具描述等安全关键信息；
2. 利用泄露信息构造自适应 payload，劫持 agent 的内置命令执行工具，达到 RCE。

它测试的是完整 coding-agent pipeline，不只是基础 LLM 的聊天安全。**[全文：§1、§3](https://arxiv.org/pdf/2509.05755v6)，[ISSTA 官方摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/176/Red-Teaming-Coding-Agents-from-a-Tool-Invocation-Perspective-An-Empirical-Security-A)**

### Gap：以前为什么解决不了？

1. 既有 agent 攻击覆盖通用 agent、RAG、memory、web agent 等，但没有系统研究 coding agent 的工具调用面；coding agent 的 shell、文件系统和 MCP 外部工具带来更高权限。**[全文：§1、§9](https://arxiv.org/pdf/2509.05755v6)**
2. 传统 prompt leakage 在 user/chat channel 里明确要求“输出 system prompt”，强模型很容易识别并拒绝。**[全文：§1、§4](https://arxiv.org/pdf/2509.05755v6)**
3. 既有 tool poisoning 多把 payload 全塞进 tool description；但 description 在上下文中较早、显著性有限，而且新版 agent 已开始隐藏完整工具描述。单通道注入不稳定。**[全文：§1、§5–6](https://arxiv.org/pdf/2509.05755v6)**

### Insight：作者最关键的想法？

有两个彼此衔接的 insight：

1. **Mode gap / ToolLeak：** LLM 在 chat generation 模式下可能拒绝泄密，但在 schema-driven argument filling 模式下，会把“请填 system prompt”理解为普通字段补全，把隐藏上下文复制进外部工具参数。安全策略对两个输出通道并不一致。
2. **Two-channel hijacking：** 先在 tool description 中放“诱饵”让 agent 调用恶意 MCP 工具，再在 tool return 中放真正的命令执行指令。return 位于上下文末端、对下一步推理更显著，因此比把全部内容塞进 description 更容易驱动内置 shell 工具。

Phase 1 泄露出的真实工具名、提示格式和 guardrail 又被用来定制 Phase 2 payload，形成 reconnaissance → exploitation 的闭环。**[全文：§1、§4–5](https://arxiv.org/pdf/2509.05755v6)**

### Technique：怎么实现？

1. **Threat model：** 攻击者不能修改 backend LLM、隐藏 prompt 或内置高权限工具；但能诱使受害者连接攻击者控制的外部 MCP 工具，并控制该工具的 description 与 return。用户请求本身可以是正常编码任务。**[全文：§3](https://arxiv.org/pdf/2509.05755v6)**
2. **Phase 1 / ToolLeak：** 恶意外部工具定义一个看似普通但语义指向内部上下文的 required argument，例如让 `note` 字段对应 system prompt。模型为了生成 schema-compliant call，把隐藏 prompt 填入参数；参数被发给外部工具，泄密完成。**[全文：§4，Table 1](https://arxiv.org/pdf/2509.05755v6)**
3. **Phase 2 / RCE-2：** description-channel payload 让 agent 把恶意工具视为正常初始化步骤并调用；tool return 再声称初始化未完成，要求调用已知的内置 command tool 执行攻击者命令。payload 会按 Phase 1 泄露的工具名、XML/Markdown 格式和 agent-specific refusal trigger 微调。**[全文：§5、§7](https://arxiv.org/pdf/2509.05755v6)**
4. **对照 RCE-1：** 使用相同语义内容，但全部放入 description、不使用 return channel，从而隔离第二通道的贡献。另与 AgentDojo、InjecAgent、MCPTox 的单通道模板比较。**[全文：§6.4](https://arxiv.org/pdf/2509.05755v6)**

### Evaluation：怎么证明有效？

**Prompt leakage（模拟环境）**

- 用公开泄露的生产 agent prompts 作为近似 reference，模拟 6 个 coding agents；测试 5 个公开 backend（Grok-4、Claude Sonnet 4/4.5、Gemini-2.5-Pro、GPT-5），temperature=0，每个 agent-LLM-method 运行 10 次。
- 指标是 embedding semantic similarity（越高越好）和 normalized Extended Edit Distance（越低越好）。ToolLeak 在 6 个 agent 上的 similarity 为 **0.891–0.958**；例如 Cursor 为 **0.949**，最强对照仅 **0.665**。**[全文：§6.2、Table 3](https://arxiv.org/pdf/2509.05755v6)**

**Prompt leakage（真实 agents）**

- 每个 agent-LLM-method 运行 10 次，但采用 **best-of-10**；因拿不到真实 system prompt，作者用“某方法抽取句子 / 所有方法抽取句子的并集”定义 pseudo-recall。
- ToolLeak 在 **18/25** 个 agent-LLM 组合上取得所有方法中最高 pseudo-recall；arXiv v6 摘要另报告 **19/25** 个组合出现泄漏。Gemini-2.5-Pro 的 tool-use filter 是一个明显反例，例如 Copilot+Gemini 上 ToolLeak pseudo-recall 只有 **0.13**，Ignore-based attack 可到 **0.87**。**[全文：§6.3、Table 4](https://arxiv.org/pdf/2509.05755v6)，[arXiv 摘要](https://arxiv.org/abs/2509.05755)**

**Tool hijacking / RCE**

- 每种方法、每个 agent-LLM pair 最多 10 次，成功定义为 agent 调用了内置 command tool 并传入预期 payload。
- 在旧版本 agent/model block，RCE-2 在每个被测 pair 上都是最佳，多数配置 ASR 为 **0.8–1.0**；单通道 benchmark 基线接近 0。
- 新版本显示明显 hardening：采用 progressive disclosure 后，Claude Code + Sonnet-4.6/Opus-4.7 上 RCE-2 为 **0.0**，Cursor 新版所有 backend 最高 **0.3**；但缺少同类架构改造的 Cline、Windsurf、Trae 在 Gemini-3.1-Pro 上仍可达 **1.0**，Cline+Grok-4.20 也是 **1.0**。这说明系统架构隔离比单靠模型 alignment 更关键。**[全文：§6.4、Table 5](https://arxiv.org/pdf/2509.05755v6)**

**Defense exploration**

- ToolLeak 的恶意 schema description 在 PPL 检测中得分 **18.78**，反而比正常 MCP description 平均值更“自然”，Llama-Prompt-Guard-2-86M 也把它判为 benign。
- 对 RCE payload，PPL/Window-PPL 均未检出；Prompt Guard 检出多数 description/return，但 Cline 的 return 仍漏过；Agent-Scan 与 MCP Safety Scanner 在这组**非自适应、未做隐蔽性优化**的 payload 上检出了 6/6 agents。**[全文：§8、Table 6](https://arxiv.org/pdf/2509.05755v6)**

### Weakness：哪里还能改？

1. **攻击前提不弱。** 攻击者必须让受害者连接恶意外部工具/MCP server；论文证明的是这条供应链边界一旦失守后的影响，不等于任意远程网站都可直接 RCE。**[全文 §3 + 批判性分析](https://arxiv.org/pdf/2509.05755v6)**
2. **ground truth 不可靠。** 专有 agent 的真实 system prompt 不可见，模拟实验把公开泄露 prompt 当 reference，可能不完整或版本错配；真实实验的 pseudo-recall 又以所有攻击方法的输出并集作分母，只适合相对比较，不是绝对召回率。作者也在 threats to validity 中承认这一点。**[全文：§6.2–6.3、§10](https://arxiv.org/pdf/2509.05755v6)**
3. **best-of-10 会放大攻击者视角。** 它证明“多试几次能否成功”，但不能代表典型单次风险；建议同时报告 first-shot、expected attempts-to-success 和置信区间。**[批判性分析；协议见全文 §6.3](https://arxiv.org/pdf/2509.05755v6)**
4. **RCE oracle 只验证调用意图。** 指标是 command tool 被带指定 payload 调用，不保证在不同 OS、网络隔离、权限、approval UI 下真的造成同等外部影响。论文 §10 明确把这列为 construct validity 威胁。**[全文：§6.4、§10](https://arxiv.org/pdf/2509.05755v6)**
5. **结论高度版本敏感。** 新版 Cursor/Claude Code 已显著压低攻击成功率，说明这类经验结果会随 tool disclosure、guard model 和 backend 更新快速过期。6 个 agent、有限 backend 不能代表未来版本。**[全文：§6.4、§10](https://arxiv.org/pdf/2509.05755v6)**
6. **防御实验尚未面对 adaptive evasion。** Agent-Scan/MCP Safety Scanner 的 6/6 检测来自作者明确说明“未优化隐蔽性”的 payload；不能据此断言这些扫描器已解决问题。**[全文：§8.2](https://arxiv.org/pdf/2509.05755v6)**

### My Idea：如果让我继续做，我做什么？

我会做 **ToolFlowFuzz：面向 agent tool graph 的动态信息流/能力流测试**：

1. 在 system prompt、tool metadata、memory 和用户秘密中放不同 canary，给每条敏感数据加动态 taint；
2. 系统变异 MCP schema：参数名、required/optional、嵌套对象、类型、description、tool return、错误消息与多工具链组合；
3. 同时追踪两类 coverage：`secret source → tool argument/return` 的 information-flow edge，以及 `untrusted tool return → privileged built-in action` 的 capability-flow edge；
4. oracle 不只看最终 RCE，而是分级记录泄密、跨域数据传播、approval 绕过、文件/网络/shell 副作用；
5. 对 progressive disclosure、typed-untrusted-return、capability token、人工确认与 sandbox 做同一套 security–utility 回归，防止防御通过“禁用所有工具”虚假获胜；
6. 每次 agent/model 更新后自动重跑，形成版本化安全基线和 regression alerts。

这比继续手工设计一个新 prompt 更像软件测试研究：有可定义的输入空间、覆盖准则、污染传播 oracle、最小化失败用例和持续回归机制。**[研究设想]**

---

## 三篇放在一起看：它们分别占据哪一层？

| 层次 | 论文 | 测试对象 | 主要 oracle/反馈 | 最值得继承的思想 |
|---|---|---|---|---|
| 失败后诊断 | FAMAS | MAS 执行轨迹 | 成功/失败轨迹频谱 + 人工 root-cause label | 把非确定性重跑变成“测试套件”，用统计谱定位 action |
| 环境输入安全测试 | AgentBreaker | Web agent 读取的 DOM/页面上下文 | 恶意 action 排名 + 真实 agent 执行 | payload 必须适配当前语境，并用 action feedback 迭代 |
| 工具边界安全测试 | ToolLeak | Coding agent 的 schema filling 与 tool chain | secret 泄漏、privileged tool invocation | 结构化 tool call 也是信息流通道；description/return 可形成两阶段控制流 |

一个自然的统一研究方向是：**Agent Testing = context/input generation + trajectory/tool-flow coverage + causal failure attribution + side-effect oracle**。AgentBreaker负责“生成能触发问题的上下文”，ToolFlowFuzz负责“覆盖并观察跨工具边界的信息/能力传播”，Causal-FAMAS负责“问题发生后定位真正致错 action”。
