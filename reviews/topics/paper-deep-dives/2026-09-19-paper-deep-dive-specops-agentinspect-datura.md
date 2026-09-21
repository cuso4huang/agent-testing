# SpecOps、AgentInspect、Datura：按 Problem–Gap–Insight–Technique–Evaluation–Weakness–My Idea 解读

检索与核查日期：2026-09-19。

证据标记：

- **[全文]**：已检查合法开放的论文正文，可报告章节、表格和实验数字。
- **[摘要]**：只检查了会议官方摘要，只据此陈述高层目的、方法和作者报告的结论。
- **[复现包]**：来自作者公开的代码、轨迹、标注或实验结果；可以说明实现和复算结果，但不等同于论文正文。
- **[我的判断]**：基于上述证据提出的局限或后续研究设计，不是作者原话。

元数据状态：SpecOps 的 DOI `10.1145/3744916.3787778` 已由 Crossref 与 OpenAlex 一致确认，属于 **Verified**；AgentInspect、Datura 的 ISSTA 2026 身份由会议官方 program 确认，但截至检索日未得到论文 DOI 的 Crossref/OpenAlex 双重确认，属于 **Partially verified**。ISSTA 2026 会议安排仍标为 tentative。

---

## 1. SpecOps: A Fully Automated AI Agent Testing Framework in Real-World GUI Environments（ICSE 2026）

来源：[arXiv 开放全文](https://arxiv.org/pdf/2603.10268)、[ICSE 官方论文页](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/250/SpecOps-A-Fully-Automated-AI-Agent-Testing-Framework-in-Real-World-GUI-Environments)、[官方代码/数据](https://github.com/yusf1013/SpecOps)、[DOI](https://doi.org/10.1145/3744916.3787778)。以下技术与数字均为 **[全文]** 证据，主要对应论文 §3–§5、Tables 3–10。

### Problem：解决什么？

SpecOps 解决的是**产品级、真实 GUI 环境中 LLM 智能体的端到端自动测试**。被测对象不是一个孤立模型，而是能够操作 Gmail、浏览器、文件系统、CLI 或浏览器扩展的完整智能体。一次测试必须连续完成：设计任务、布置环境、启动并操控被测智能体、观察其过程、检查真实环境副作用、最后判断是否为缺陷。论文的目标是让这条链路在没有人工参与执行与判定的情况下自动完成，而不是只计算 benchmark 的最终成功率。[全文 §1、§3、§4](https://arxiv.org/pdf/2603.10268)

### Gap：以前为什么解决不了？

作者将困难归纳为三类：

1. **端到端一致性难以维持。** 环境前置条件、给被测智能体的自然语言 prompt、以及最后的 oracle 必须相互一致；早期一个小错误会在后续阶段变成误报或漏报。
2. **平台高度异构。** Web 应用、CLI、浏览器扩展和桌面系统没有统一 API；固定 Selenium/Playwright 脚本无法适应智能体非确定的动作路径。
3. **通用 agent 不具备测试语义。** 静态 LLM 脚本无法运行时恢复，AutoGPT 一类通用 agent 又容易混淆“测试者”和“被测对象”，看到被测智能体报错时会尝试替它修复，而不是记录缺陷；它们也缺少 assertion、checkpoint 和故障隔离。[全文 §3.1–§3.2](https://arxiv.org/pdf/2603.10268)

### Insight：作者最关键的想法？

关键不是“换一个更强的 LLM”，而是把长链测试拆成**具有清晰职责边界的测试组织**：让不同 specialist 分别负责设计、布置、执行和审计，并让所有阶段共享、更新同一份 test specification。这样既减少单个模型的上下文负担，也明确区分 tester 与 testee。更细的一层 insight 是：真实智能体的正确性不能只从最终回答判断，必须同时读取**屏幕证据 + 环境真实状态 + 执行观察**。[全文 §4.1、§4.5](https://arxiv.org/pdf/2603.10268)

### Technique：怎么实现？

SpecOps 是四阶段流水线：

1. **Test Case Generation。** Test Architect 从 feature 生成环境设置、用户 prompt 和 expected behavior；Test Analyst 再检查自然性、prompt 完整性、环境可行性与 oracle 是否允许多种合法路径。这是生成—审查的双 specialist 结构。
2. **Environment Setup。** Infrastructure Manager 把自然语言前置条件翻译成 MCP 工具调用；读取调用结果后可重试、修订 prompt/expectation，或在无法布置时中止，防止把 setup failure 算成被测智能体 bug。
3. **Test Execution。** Engineer 只通过通用键盘/鼠标原语与被测智能体交互；键盘工具会验证文字是否真正出现在屏幕上，屏幕变化时自动截图，以保存 GUI 智能体通常缺失的内部 trace。
4. **Validation & Auditing。** Investigator 独立探查 Gmail、文件系统等环境的真实变化；Judge 汇合截图、运行观察和环境报告，对照 oracle 判断是否存在“不合理偏离、误报、任务完成/质量受损、要求不合理人工介入”。Judge 使用 Meta-CoT：先生成应检查的问题，再逐一回答，降低直接吞下大量异构证据时的幻觉。[全文 §4.2–§4.5](https://arxiv.org/pdf/2603.10268)

### Evaluation：怎么证明有效？

- 对象是 5 个真实 agent：ProxyAI、Self-Operating Computer、TaxyAI、Open Interpreter、Autonomous HR Chatbot；覆盖 Email、File System、HR Q&A 三个领域。最终 feature 数为 Email 17、File System 20、HR Q&A 29；由于前三个 Email agent 共享 17 个 feature，总计执行 **99 个测试**。[全文 Tables 3–5](https://arxiv.org/pdf/2603.10268)
- 与两类替代方案比较：LLM 生成的端到端自动化脚本，以及通用 AutoGPT。三者获得相同 feature 描述、agent 文档和环境/API 条件；AutoGPT 不支持图像，作者用经人工核验的图像文字描述替代。[全文 §5.2](https://arxiv.org/pdf/2603.10268)
- SpecOps 的 prompt 成功率为 **100%**，LLM Scripts 为 **49.5%**，AutoGPT 为 **11.1%**；执行阶段完成 **518/518** 个计划步骤，验证阶段完成 **1551/1615（96.0%）**，而 LLM Scripts 分别为 53.9%/24.8%，AutoGPT 为 33.5%/5.0%。[全文 Tables 7、9](https://arxiv.org/pdf/2603.10268)
- 人工对运行 trace 复核后，SpecOps 报告 **164 TP、15 FP、26 FN**，即 precision **0.92**、recall **0.86**、F1 **0.89**；LLM Scripts 为 13 TP、58 FP、31 FN、F1 0.23；AutoGPT 没能标出 bug。注意“164 个 true bugs”是人类复核后的 TP，不是 Judge 原始报警数。[全文 Tables 8–9](https://arxiv.org/pdf/2603.10268)
- 故障恢复 sanity check 额外人工注入了 **20 个 setup failures**（断网、存储不足、API timeout）；Infrastructure Manager 能重试后把它们识别为环境失败并退出，而不报成 AUT 缺陷。[全文 §5.8](https://arxiv.org/pdf/2603.10268)
- 99 个测试合计约 **12.5 小时、72 美元**，平均低于 8 分钟、约 **0.73 美元/测试**。不同 agent 的均值差异很大，例如 SOC 为 742 秒/1.58 美元，HRC 为 221 秒/0.20 美元。[全文 Table 10、§5.9](https://arxiv.org/pdf/2603.10268)

### Weakness：哪里还能改？

1. **Oracle 还不够可靠。** 15 FP、26 FN 意味着“全自动”并不等于“无需质量兜底”；recall 0.86 在高风险操作上仍可能漏掉关键 bug。[全文 Table 9]
2. **外部效度有限。** 只有 5 个 agent、3 个领域、99 个 feature-level 测试，而且认证信息预先保存在浏览器中；权限升级、支付、跨 session memory、多人协作、长时间环境漂移均未覆盖。[我的判断，依据全文 §5.1、§5.4]
3. **测试器和 oracle 共享模型偏差。** 所有 specialist 使用 Claude 3.7 Sonnet；同一模型家族既生成测试又解释证据，可能形成 correlated blind spot。论文没有跨模型 oracle 或模型替换实验。[我的判断，依据全文 §5.4]
4. **测试空间仍经过人工筛选。** Feature list 经自动抽取、跨 benchmark mining 和 manual augmentation 得到；框架自动化的是单个 feature 的测试执行，不等价于自动发现完整需求空间。[全文 §5.1.2]
5. **基线不够强。** LLM Script 与 AutoGPT 能说明“静态脚本/通用 agent 不够”，却不能证明它优于未来同类专业 agent-testing framework；此外 AutoGPT 只能接收截图文字描述，虽经人工检查，交互能力仍与多模态 SpecOps 不对称。[我的判断，依据全文 §5.2]

### My Idea：如果让我继续做，我做什么？

我会做 **CausalReplay：面向真实 agent 的可重放、可归因测试层**。

- 把每次测试的 GUI 状态、工具调用、环境副作用和权限状态记录成 event-sourced snapshot；同一初始快照可确定性回放。
- 对成功轨迹只改变一个因子：某次工具返回、UI 元素位置、权限、memory 内容或模型版本，形成成对 counterfactual test。
- oracle 不只由一个 LLM 判断，而是“可执行环境不变量 + 差分轨迹 + 两个异构模型 + 少量人工仲裁”。
- 新指标从“找出多少 bug”升级为：因果覆盖（哪个环境变量/工具依赖被扰动）、恢复覆盖、跨模型/跨版本退化和 flaky rate。

这样可以补上 SpecOps 当前最弱的两点：结果难复现，以及发现 bug 后难说明**究竟是哪一个状态变化导致失败**。

---

## 2. AgentInspect: Diagnosing Behavioral Failures in Artificial Intelligence Agents（ISSTA 2026）

来源：[ISSTA 官方论文页/摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/83/AgentInspect-Diagnosing-Behavioral-Failures-in-Artificial-Intelligence-Agents)、[Zenodo 复现包](https://zenodo.org/records/21482543)。截至检索日未发现公开论文全文，所以下面把 **[摘要]** 与 **[复现包]** 分开；不能把复现包分析冒充对论文正文的精读。

### Problem：解决什么？

AgentInspect 解决的是：**LangChain/ReAct 智能体在正常和异常工具条件下，会出现哪些可复现的行为故障，怎样系统地产生输入、注入条件并从轨迹中确定性识别它们。** 它关注的不是最终答案 accuracy，而是智能体遇到 error、空结果、延迟或前后不一致的工具返回时，是否循环、乱调工具、违反 ReAct 格式、在无证据时给结论、崩溃或无法处理工具失败。[摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/83/AgentInspect-Diagnosing-Behavioral-Failures-in-Artificial-Intelligence-Agents)

### Gap：以前为什么解决不了？

官方摘要给出四个根因：LLM reasoning 有随机性、自然语言输入空间巨大、agent 依赖外部工具、执行环境动态变化。因此，传统输入—输出断言既难覆盖中间状态，也难稳定复现偶发工具失败；单纯用真实工具运行，往往永远碰不到低频 timeout、空响应或不一致响应。[摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/83/AgentInspect-Diagnosing-Behavioral-Failures-in-Artificial-Intelligence-Agents)

### Insight：作者最关键的想法？

最关键的想法是把“智能体测试”拆成两个互补世界：

- 先在 **baseline** 中捕获真实工具响应与轨迹；
- 再在 **simulated/hybrid** 中对同一工具—输入对替换响应，观察 agent 的恢复行为；
- 最后不用另一个自由生成 LLM 当 oracle，而用轨迹上的确定性规则判定行为 failure。

也就是说，真实运行提供语义和可执行路径，模拟运行提供稀有故障覆盖；两者结合避免纯 mock 脱离真实轨迹，也避免只靠线上偶然故障。[摘要 + 复现包]

### Technique：怎么实现？

根据公开实现，流程是：

1. **覆盖导向输入生成。** GPT-4o 为每个 agent 生成 30 个唯一测试输入；prompt 要求同时包含 single-tool 与 multi-tool 场景，并按 `correct/error/delayed/incomplete/no response` 五种工具响应条件各生成 6 个输入。官方摘要把它概括为 agent-specific coverage-guided generation。[复现包 `test_generator.py`](https://zenodo.org/records/21482543)
2. **先捕获真实轨迹。** 用 LangChain `AgentExecutor` 执行，保存 action、action input、observation 与 final answer，并把工具响应抽象为 Complete/Error/No Response。[复现包 `original_run.py`、`trace_abstractor.py`]
3. **Capture-and-Simulate。** 对实际出现过的 `(tool, semantically-similar input)` 生成三种 mutant：错误消息、截断到约四分之一的 incomplete response、结构保持但值清空的 no response；另有 delayed（前两次空，之后真实）和 inconsistent（第一次真实，后续以 0.5 概率返回真实或随机 mutant）两种 hybrid 模式。[复现包 `generate_mutants.py`、`mock_run.py`]
4. **六类确定性 failure oracle。** 公开结果表中的类别为 Repetitive Reasoning（RR）、Tool Crash（TC）、Invalid Tool Invocation（ITI）、ReAct Format Violation（RFV）、Inference Without Evidence（IWE）、Tool Execution Failure（TEF）。实现中通过工具名合法性、action-input 格式、工具响应类别、final-answer fallback 词、以及 MiniLM embedding 相似度阈值检测重复调用。[复现包 `trace_analyzer.py`、Results/Table_1_RQ1.xlsx]

### Evaluation：怎么证明有效？

- 官方摘要报告从 GitHub 整理了 **35 个 LangChain agent**，在真实工具响应 baseline 和合成工具响应 simulated setting 中分析轨迹；simulated setting 找到了 baseline 中不会出现的 failure mode。[摘要](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/83/AgentInspect-Diagnosing-Behavioral-Failures-in-Artificial-Intelligence-Agents)
- 复现包每个 agent 有 30 个输入。对 `Table_3_RQ3.xlsx` 逐项求和：baseline 的 1050 条轨迹中有 **489** 条 faulty；在相同 1050 输入上，error、incomplete、no-response、delayed、inconsistent 五种附加设置分别再暴露 **786、856、853、662、335** 条 faulty trajectory。这里是我对公开表的算术汇总，不是摘要直接写出的数字。[复现包](https://zenodo.org/records/21482543)
- 对 `Table_1_RQ1.xlsx` 的 TP/FP/FN 做 micro aggregation，五种 injected setting 的 precision/recall 分别约为：error **0.949/0.975**，incomplete **0.977/0.986**，no response **0.971/0.981**，delayed **0.979/0.976**，inconsistent **0.932/0.985**。这支持摘要所谓“high precision and recall”，但它是基于复现表的独立复算。
- 结果还与 AgentEvals、Galileo 的人工/工具标签作比较，并提供人工标签、Cohen’s kappa、ablation prompts、完整 trajectory dataset，因而比只给平均分更可审计。[复现包目录与 Zenodo 描述](https://zenodo.org/records/21482543)

### Weakness：哪里还能改？

1. **当前无法全文核查。** 会议页只有摘要，复现包没有论文 PDF；因此 coverage criterion 的正式定义、采样协议和作者自己的 threats-to-validity 还不能核对。[证据限制]
2. **确定性 oracle 很脆。** 公开代码把相似度阈值固定为 0.7，用关键词识别工具 error/final fallback，并把不在 tool-name 列表中的 action 判为 invalid；换模型、语言、输出协议时容易失效。[复现包代码]
3. **真实响应 baseline 的表现并非全面“高精度”。** 对公开 Table 1 复算，baseline 总体 micro precision/recall 约 **0.760/0.875**；其中 IWE precision 约 **0.261**，TEF precision/recall 约 **0.410/0.561**。优势主要集中在受控 fault-injection 条件，不能泛化成所有真实运行下都接近完美。[我的复算]
4. **故障模型偏“响应可用性/形状”。** error、空、截断、延迟、不一致很重要，但没有系统覆盖“格式完整却语义错误”的工具输出，例如陈旧数据、单位错、身份错配、跨工具冲突和权限欺骗。[我的判断，依据复现包 mutation operators]
5. **适用范围窄。** 目前面向 LangChain/ReAct，35 个 GitHub agent 的结果不能直接外推到 LangGraph、OpenAI Agents SDK、CrewAI、MCP server、GUI agent 或生产级多智能体系统。[摘要 + 我的判断]

### My Idea：如果让我继续做，我做什么？

我会做 **Contract-and-Causality Coverage for Agents**：

- 从工具 schema、文档和真实轨迹推断 tool contract，不只做 error/empty mutation，还生成 stale、wrong-unit、conflicting-identity、permission-drift、cross-tool contradiction 等**语义 fault**。
- 定义四维覆盖：`工具响应故障 × 在依赖链中的位置 × agent 恢复策略 × 最终环境副作用`，而不是只统计有没有进入某类 response。
- 对同一输入重放多个模型种子，只有 failure 与受控 mutation 有稳定因果关联时才报警，降低关键词/embedding oracle 的误报。
- 做一个 framework-neutral trace schema，把 LangChain、LangGraph、OpenAI Agents、CrewAI、MCP 和 GUI action 都映射到统一事件，再验证 detection rules 的跨框架迁移。

这样能把 AgentInspect 从“面向几种工具异常的轨迹检查器”推进成真正可比较的 agent coverage 与 fault-model 标准。

---

## 3. Datura: Progressive Red Teaming Testing for Tool Invocation Chain in LLM Agents（ISSTA 2026）

来源：[作者主页公开的 24 页全文](https://chengcheng-wan.github.io/paper/26-ISSTA-Datura.pdf)、[ISSTA 官方论文页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/10/Datura-Progressive-Red-Teaming-Testing-for-Tool-Invocation-Chain-in-LLM-Agents)、[公开 artifact](https://github.com/ycshao12/Datura_RedTeaming_Testing)。以下技术与数字为 **[全文]**，对应 §3–§9、Tables 4–6。

### Problem：解决什么？

Datura 测试的是**工具调用链的安全性**：攻击者不在用户 prompt 里直接说“做坏事”，而是让一个看似正常的第三方工具/MCP server 在多步执行中逐渐污染 metadata 和 tool output，使 agent 把恶意动作理解为合理的系统流程。单步都像正常操作，组合起来却导致数据外泄、支付欺诈、权限提升或防御规避。[全文 §1、§3](https://chengcheng-wan.github.io/paper/26-ISSTA-Datura.pdf)

### Gap：以前为什么解决不了？

1. 直接 prompt injection 或静态 jailbreak 太明显，容易被输入过滤器挡住，不能测试 agent 对**累积工具上下文**的隐式信任。
2. 工具没有完整形式规约，何时算“agent 已被误导”存在 oracle 问题；metadata 中权威语气、名称和描述带来的 bias 又常被忽略。
3. 工具链是有状态依赖的。随便拼接恶意返回会导致轨迹不连贯，agent 因格式错误或逻辑矛盾拒绝；这测到的是 malformed input，而不是可信工作流被劫持。
4. 多轮黑盒攻击依靠反复对话试探，非确定性与查询开销高，也没有系统操控 tool output/metadata。[全文 §1.1–§1.2](https://chengcheng-wan.github.io/paper/26-ISSTA-Datura.pdf)

### Insight：作者最关键的想法？

核心 insight 是：agent 的安全弱点不是只存在于“恶意内容”，还存在于它对**系统式证据和流程连续性**的信任。作者先做经验研究，观察到：biased metadata 的工具选择率为 **100%**；system-level bridge 引导目标工具的成功率为 **99.72%**；完整 progressive context 的恶意执行率约 **99%**，而只给最后恶意一步是 **0%**；中性机器日志语气达到 **95%**，命令式或乞求式都是 0%。于是攻击无需显眼 jailbreak，只要每一步都像可信系统日志，并把下一工具塑造成“唯一合理后继”。[全文 §4.2–§4.3](https://chengcheng-wan.github.io/paper/26-ISSTA-Datura.pdf)

### Technique：怎么实现？

Datura 有五阶段：

1. **Bias Injection。** GPT-4o 从 benign query 和 toolset 生成长度至少 3 的合理工具链；只对第一个工具叠加七类 metadata bias：assertive cue、active maintenance、usage example、name-dropping、numerical claim、lengthening、sorting。
2. **Malicious Goal Planning。** 用进度 `U = step/total_steps` 把链分为 early `<0.4`、middle `0.4–0.7`、final `≥0.7`；目标由研究/诊断逐渐过渡到假设性集成，再到真实恶意动作，同时用中性、机器人式措辞替换显眼攻击词。
3. **Tool Bridge Construction。** mutation model 在运行时生成四部分的日志式 output：具体结构化结果、随阶段升级的 urgency、为何必须执行下一步的依赖解释、明确声明下一工具可用。它把语义断点伪装成因果依赖。
4. **Test Execution。** 将生成 output 动态返回给目标 agent；若拒绝或偏离链，回溯并重写上一步的语义 framing/urgency。连续两次生成失败时退回确定性模板，保证测试不中断。
5. **Report Generation。** GPT-4o Judge 输出 PHR（prompt 看起来无害的比例）、ASR（agent 已承诺执行恶意目标，即使模拟 API 最后没真正成功）和 AR（完全或部分协助恶意目标）。[全文 §5.1–§5.6](https://chengcheng-wan.github.io/paper/26-ISSTA-Datura.pdf)

### Evaluation：怎么证明有效？

- 测试 5 个模型、4 个家族：Qwen-2.5-32B、Gemma-3-27B、GPT-4.1、GPT-4o-mini、Gemini-2.5-pro；任务来自 Agent-SafetyBench 与 SHADE-Arena，共 **740 个 safety-critical tasks**。[全文 §7.1、§7.4](https://chengcheng-wan.github.io/paper/26-ISSTA-Datura.pdf)
- 对比 Prompt Attack、Injected Attack、Jailbreak Function Attack 三类 baseline。无额外防御、只看模型自身 alignment 时，Datura 的 ASR 为 **94.86%–99.59%**，PHR 为 **72.70%–85.54%**；最强 baseline 在 Gemini 上为 70.00%，Datura 为 95.27%，差 25.27 个百分点。[全文 Table 5、§8.1]
- 加 Prompt Refuge system prompt 后，Datura 仍有 **78.78%–95.54% ASR**；例如 GPT-4.1 上 92.70%，而 Jailbreak Function Attack 从 96.22% 降到 29.86%。[全文 Table 5]
- 在复现的真实软件防御中：Dify 防御下 ASR **65.81%–96.76%（均值 79.89%）**，Khoj LLM-judge 防御下 **72.30%–92.30%（均值 79.86%）**，逐步人工审核下 **75.54%–82.70%**。作者的解释是审核者单独看每一步时忽略了长链的聚合意图。[全文 §8.2]
- 消融显示 Prompt Refuge 下移除 Tool Bridge 最多使 ASR 下降 **10.86pp**，移除 Bias Injection 最多下降 **4.94pp**；bridge 的影响约为 bias 的 2.0–2.8 倍，支持“语义连续性比入口选择 bias 更关键”。[全文 Table 6、§8.3]
- GPT-4o 自动评分器随机抽取 200 个案例做人类复核，报告 Cohen’s `κ = 0.99`。[全文 §7.5]

### Weakness：哪里还能改？

1. **威胁模型假设较强。** 攻击者必须能控制某些工具输出并修改首个工具 metadata；它很好地覆盖恶意第三方工具/MCP supply chain，但不能代表只有网页内容污染、memory poisoning 或用户权限不足的所有威胁。[全文 §3.1 + 我的判断]
2. **ASR 是“执行意图”，不一定是真实伤害。** 论文明确规定：agent 承诺转账/外泄，即使模拟 API 失败，也可计为 ASR 成功。因此它证明的是 policy compromise，不等于端到端 exploit success。[全文 §5.6]
3. **只覆盖文本工具交互。** 作者自己在 Threats to Validity 中承认尚未覆盖 vision/audio 等多模态工具；只测两个 benchmark、有限模型和若干金融/邮件/日历等域。[全文 §9]
4. **生成器和 evaluator 都依赖 GPT-4o。** 200 个样本的人工复核与 κ=0.99 是很好的缓解，但没有消除生成偏好、judge bias 和跨 740 任务整体误差。[我的判断，依据全文 §5.4、§5.6、§7.5]
5. **防御评估是机制的本地复现。** Dify、Khoj 和人工审核流程在受控环境重建，并非直接攻击完整线上部署；真实系统的权限边界、审计、事务回滚和工具签名可能改变结果。[全文 §7.3 + 我的判断]
6. **方法擅长一类安全缺陷，不是通用 agent tester。** 它不能替代功能正确性、性能、恢复性、隐私合规或长期 memory 测试；应理解为 tool-chain red teaming 专项工具。[我的判断]

### My Idea：如果让我继续做，我做什么？

我会把 Datura 发展成 **Temporal Provenance Testing + Defense Co-evolution**：

- 给每个 tool result 附带来源、签名、权限、freshness 和 trust level，把这些属性作为类型沿调用链传播；测试器系统地篡改其中一个 provenance 字段。
- 构建 temporal safety oracle：不是逐步判“这句话危险吗”，而是检查跨步骤的信息流、权限升级、目标漂移和 cumulative risk，例如 `read(secret) → transform → send(external)`。
- 让 Datura attacker 与 provenance-aware monitor 交替训练/搜索，报告的不只是 ASR，还包括真实 side-effect success、被哪条 policy 拦截、最短攻击链和 false-positive utility cost。
- 扩展到 GUI observation、网页内容、长期 memory 和 agent-to-agent message，在事务化 sandbox 中执行真实副作用后自动回滚。

这会把论文揭示的“逐步无害、整体有害”现象，转化为可部署的跨步骤防御与更严格的端到端安全测试标准。

---

## 三篇论文放在一起看

- **SpecOps** 解决“真实环境里端到端把 agent 测起来”，重点是 test orchestration 与环境 oracle。
- **AgentInspect** 解决“工具异常时 agent 怎样坏、怎样稳定检出”，重点是 fault injection、trajectory 和 behavioral oracle。
- **Datura** 解决“工具链怎样在每步看似合法时把 agent 渐进劫持”，重点是 adversarial tool output、跨步语义和安全 oracle。

它们正好组成一个可继续研究的三层栈：底层用 SpecOps 提供真实执行环境，中层用 AgentInspect 做系统故障与恢复覆盖，上层用 Datura 做对抗性工具链测试；共同缺口是**可重放状态、跨步骤因果覆盖、独立可执行 oracle，以及跨框架统一 trace schema**。
