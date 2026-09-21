# 智能体测试第 6、7 类方法：论文检索与阅读笔记

> 检索截止：2026-08-22（Asia/Shanghai）  
> 本文件是第一阶段交付物；尚未据此制作或修改 PPT。

## 0. 术语与阅读口径

- **Coverage Feedback（覆盖反馈）**：用本轮执行发现的新行为或新状态，决定下一轮优先测试哪些输入。
- **Grey-box Testing（灰盒测试）**：不要求完全理解系统内部实现，但利用部分运行信息引导测试生成。
- **Seed（种子）**：作为后续 Mutation（变异，即对输入进行修改）的起始测试输入。
- **Oracle（测试判定机制）**：判断一次执行是否正确、安全或符合约束的规则、模型或环境检查器。
- **Trajectory（执行轨迹）**：Agent 运行中的状态、动作、工具调用、观察和消息序列。
- **Failure Attribution（故障归因）**：定位哪个 Agent、哪个步骤对最终失败负主要责任。
- **Intervention（干预）**：主动替换某一步的动作、观察、上下文或策略，再检查结果是否变化。
- **Counterfactual Replay（反事实重放）**：修改历史步骤后重新执行后续过程，用“如果当时不同会怎样”检验归因。
- **Ablation Study（消融实验）**：移除一个模块，观察性能变化，以估计该模块的实际贡献。

## 1. 检索与筛选总表

| 项目 | 第 6 类：覆盖反馈 | 第 7 类：轨迹与因果 | 合计 |
|---|---:|---:|---:|
| 分类图或计划明确点名 | 5 | 11 | 16 |
| 联网补充的直接相关候选 | 1（MUZZLE） | 1（Automatic Failure Attribution） | 2 |
| 去重后的候选 | 6 | 12 | 18 |
| 已阅读全文 | 5 | 12 | 17 |
| 无法解析/排除 | 1 | 0 | 1 |
| 最终纳入阅读笔记 | 5 | 12 | 17 |

### 1.1 数据库与查询

- 数据库与权威页面：arXiv、ACL Anthology、PMLR、USENIX Security、OpenReview、Crossref、OpenAlex、DBLP/会议页面。
- 主要英文查询：`LLM agent coverage-guided fuzzing`、`tool sequence feedback agent testing`、`multi-agent behavior coverage`、`trajectory-guided red teaming web agent`、`LLM agent failure attribution`、`causal replay agent trace`、`counterfactual intervention agent failure`、`root cause multi-agent trajectory`。
- 中文辅助查询：`智能体 覆盖引导 模糊测试`、`多智能体 故障归因`、`智能体 轨迹 因果 重放`。
- 元数据核验：正式 DOI 优先；无 DOI 的预印本以 arXiv ID、精确题名和作者交叉核验。Crossref 返回的模糊近似项不视为匹配。

### 1.2 纳入、排除与版本合并

- 纳入：被测对象是 LLM Agent/MAS，且论文明确贡献覆盖反馈、轨迹评测、故障定位、干预验证或因果重放。
- 邻近纳入：MultiAgentBench 不执行覆盖引导搜索，但按用户给定分类保留，并明确标为“过程覆盖/里程碑指标型邻近工作”。
- 排除：让 Agent 去测试普通 Java/硬件程序、但不测试 Agent 本身的 coverage-guided 工作；纯训练 credit assignment；泛可解释性论文。
- `SafeVault/SafeFault`：在 arXiv、Crossref、OpenAlex 和网络检索中均未找到与 Agent 覆盖反馈测试相符的论文。它很可能是分类图中的笔误或低清晰度误读，故不纳入。
- 同一工作的 arXiv 与正式会议版合并为一条；引用优先采用 ACL、ICML/PMLR、KDD、USENIX 等正式版本。

## 2. 第 6 类：覆盖反馈驱动测试

### 2.1 VeriGrey: Greybox Agent Validation

1. **中文主题**：用工具调用序列反馈引导 Agent 安全测试。
2. **元数据**：Yuntong Zhang、Sungmin Kang、Ruijie Meng、Marcel Böhme、Abhik Roychoudhury；2026；arXiv:2603.17639v1；未核验正式会议版。
3. **证据状态**：已阅读全文；本地 PDF 与 arXiv/OpenAlex 身份一致。
4. **问题**：黑盒随机改写 prompt 很难到达低频但危险的工具组合，随机注入还常因语义不连贯而被 Agent 忽略。
5. **基本思路**：以调用过的工具序列作为行为签名；只有发现新序列的输入才被视为 interesting seed（有价值种子）。
6. **流程**：正常任务与攻击目标输入 → Context Bridging（上下文桥接）生成语义连贯的注入 → 执行 Agent → 提取工具序列 → 新覆盖则保留种子并继续变异 → Oracle 检查攻击是否成功。
7. **实现**：覆盖反馈模块维护已见工具序列；对话式攻击 Agent 按反馈动态生成变体；真实案例覆盖 AgentDojo、Gemini CLI 和 OpenClaw skills。
8. **反馈/指标**：工具调用序列新颖性；攻击发现有效率/成功率。覆盖只是搜索信号，不等同于正确性 Oracle。
9. **实验**：与黑盒 prompt 变异对比；在 AgentDojo 上比较多个后端，并做“去覆盖反馈”“去上下文桥接”消融。
10. **结果**：GPT-4.1 设置中完整 VeriGrey 为 70.7%，去掉覆盖反馈为 59.6%（下降 11.1 个百分点），去掉上下文桥接约 44.0%。论文摘要报告相对黑盒额外提升约 33%。
11. **局限**：相同工具序列可能对应不同参数和语义状态；新序列不必然更危险；预印本且真实系统案例数量有限。
12. **分类理由**：反馈直接决定种子是否保留和后续变异预算，是最典型的 Agent 灰盒覆盖闭环。
13. **PPT 可用图表**：Figure 2（上下文桥接与灰盒反馈框架）；Tables 1–2（主结果与消融）；真实系统案例表。
14. **一句话总结**：VeriGrey 将传统“代码边覆盖”替换为“工具序列覆盖”，把随机攻击生成变成受 Agent 行为反馈引导的搜索。

### 2.2 FLARE: Agentic Coverage-Guided Fuzzing for LLM-Based Multi-Agent Systems

1. **中文主题**：从 MAS 源码抽取行为规格，并用主体内/主体间覆盖引导测试。
2. **元数据**：Mingxuan Hui 等；2026；arXiv:2604.05289；OpenAlex 精确匹配，无正式 DOI。
3. **证据状态**：本轮已阅读全文（10 页 PDF，解析正文与附录共 21 个排版页）。
4. **问题**：MAS 的错误往往是无限循环、错误说话顺序、工具失败和依赖传播，普通代码覆盖很难描述这些语义行为。
5. **基本思路**：读取 MAS 源码和 Agent 定义，抽取规格、合法交互路径与主体内行为边界，再把运行轨迹映射到两类行为覆盖。
6. **流程**：软件分析 → 规格/行为空间/种子生成 → coverage-guided fuzzing → 执行与动态调度 → Failure Agent 检测 → Judge Agent 复核报告。
7. **实现**：RAC（inter-agent behavior coverage，主体间合法执行路径覆盖）与 AAC（intra-agent behavior coverage，主体内部期望/边界行为覆盖）共同更新种子和变异器权重。
8. **反馈/Oracle**：新 RAC/AAC 覆盖提高种子与变异策略权重；规格型 Oracle 检查任务、工具、关系和终止四类故障；双 Agent 复核降低幻觉报告。
9. **实验**：16 个开源 MAS 应用；与 LLM-Fuzzer、PythonFuzz、Frelatage 等比较；指标含语句、分支、RAC、AAC 和故障数。
10. **结果**：平均 96.9% RAC、91.1% AAC，较基线分别高 9.5 和 1.0 个百分点；94.2% 语句覆盖、81.7% 分支覆盖；发现 61 个 MAS 特有故障和 5 个 crash。
11. **局限**：规格和覆盖分母由 LLM/静态抽取生成，可能不完整；语义映射与 Oracle 可能共享模型偏差；部分应用环境冲突导致实验缺项。
12. **分类理由**：它明确用行为覆盖增量调度 fuzzing，是第 6 类中面向多智能体系统的核心方法。
13. **PPT 可用图表**：Figure 3（总体三阶段架构）；Figures 4–5（规格与行为抽取）；Table 1（覆盖结果）；Table 2（故障类型）。
14. **一句话总结**：FLARE 将“覆盖什么”从程序分支扩展为主体内行为和主体间协作路径。

### 2.3 Autonomy Comes with Costs: Detecting Denial-of-Service Vulnerabilities Caused by Resource Abusing in LLM-based Agents（AgentDoS）

1. **中文主题**：用资源生命周期和运行时消耗反馈发现 Agent 的拒绝服务漏洞。
2. **元数据**：Jiaqi Luo 等；USENIX Security 2026 正式论文；会议页面与正式 PDF 已核验，未发现 DOI。
3. **证据状态**：已阅读全文；本地正式稿。
4. **问题**：Agent 可自主下载、写文件或持续创建资源，功能任务可能成功但同时耗尽内存、磁盘等系统资源。
5. **基本思路**：先分析资源生命周期，再用 LLM 生成符合 Agent 功能语义的种子，以资源增长作为定向灰盒反馈。
6. **流程**：源码/资源生命周期分析 → 功能相关 prompt 种子 → Agent 执行 → 监测分配、累积和释放 → 优先变异高资源潜力种子 → 复现与报告 DoS。
7. **实现**：区分单任务、session 和永久性资源；组合静态分析、运行时监控和自然语言种子生成。
8. **反馈/Oracle**：资源增长、释放异常、崩溃或不可用状态；资源反馈既调度搜索，也参与漏洞判定。
9. **实验**：20 个广泛使用的开源 Agent；隔离环境中验证资源耗尽；记录披露和 CVE 状态。
10. **结果**：发现 36 个 zero-day，影响 16 个 Agent；论文/会议页报告其中 15 个获得 CVE。
11. **局限**：需要源码或足够资源可观测性；资源类型与样本有限；安全测试必须隔离，不能对真实服务直接运行。
12. **分类理由**：它把“新覆盖”具体化为资源生命周期和消耗潜力，是风险目标驱动的反馈式测试。
13. **PPT 可用图表**：总体工作流图、资源生命周期模式图、漏洞统计表和消融/效率表（以正式 PDF 图表编号为准）。
14. **一句话总结**：AgentDoS 证明智能体测试不仅要测任务结果，还要把资源副作用纳入反馈和 Oracle。

### 2.4 MUZZLE: Adaptive Agentic Red-Teaming of Web Agents Against Indirect Prompt Injection Attacks

1. **中文主题**：根据 Web Agent 的轨迹和失败反馈，自适应寻找间接提示注入攻击。
2. **元数据**：Georgios Syros 等；35th USENIX Security Symposium，2026；arXiv:2602.09222；正式 PDF 和作者 artifact 已核验。
3. **证据状态**：本轮已阅读全文（USENIX 正式版）。
4. **问题**：固定 payload 和人工选择注入位置无法覆盖跨网页、跨应用和动态 Agent 轨迹中的巨大攻击空间。
5. **基本思路**：先观察受测 Agent 的实际轨迹，寻找高显著性 UI 注入面，再根据每次失败原因调整位置和恶意指令。
6. **流程**：执行正常用户任务 → Vessel Scout 识别/排序注入载体 → Payload Generator 生成上下文相关攻击 → Executor 重跑 → Judge 判断成功并归因失败 → 反馈更新下一轮策略。
7. **实现**：多 Agent 红队架构；沙箱 Web 环境支持后端状态复位；失败被区分为 payload 被忽略或注入载体未进入有效上下文。
8. **反馈/Oracle**：轨迹可见元素、失败类型、Partial Attack（部分攻击）与 E2E ASR（端到端攻击成功率）。
9. **实验**：4 个 Web 应用、10 个攻击目标、3 个 LLM、2 个 Agent scaffold；每种设置重复执行以处理随机性。
10. **结果**：发现 44 个新攻击，包括 3 个跨应用攻击和 1 个面向 Agent 的钓鱼场景；Table 6 给出 10 次重放下的端到端 ASR。
11. **局限**：使用本地可控 Web 环境；攻击目标与应用仍有限；Judge 与 payload 生成模型会影响结果；真实网页漂移和防御适应可能降低复现性。
12. **分类理由**：MUZZLE 不采用形式化覆盖率，但明确使用执行轨迹和失败反馈调度下一轮攻击，属于广义反馈驱动测试。
13. **PPT 可用图表**：总体多 Agent 红队框架图；Table 1（角色）；Table 2（应用/任务/目标）；Tables 4、6（案例与 ASR）。
14. **一句话总结**：MUZZLE 展示了“覆盖反馈”之外的另一条路线——用失败原因作为搜索反馈不断改进攻击。

### 2.5 MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents

1. **中文主题**：用里程碑和协作指标评价多智能体过程；属于分类图指定的邻近工作。
2. **元数据**：Kunlun Zhu 等；ACL 2025；DOI:10.18653/v1/2025.acl-long.421；arXiv:2503.01935。
3. **证据状态**：已阅读全文；ACL/DOI 双源核验。
4. **问题**：只看最终任务分数会掩盖沟通、规划、竞争和拓扑结构中的过程故障。
5. **基本思路**：在六类交互场景中同时评估任务结果、milestone（里程碑）、通信和规划质量。
6. **流程**：配置 Agent 图与角色 → 多轮协作/竞争 → 环境动作 → milestone 检测 → Task Score 与 Coordination Score 汇总。
7. **实现**：MARBLE 支持 star/tree/graph/chain 拓扑、共享/私有记忆、工具、planner 与 actors；LLM Judge 评价通信和规划。
8. **指标**：Task Score、milestone KPI、Communication/Planning/Coordination Score、消息与迭代过程。
9. **实验**：Research、Minecraft、Database、Coding、Werewolf、Bargaining；比较模型、拓扑、规划策略、Agent 数和迭代预算。
10. **结果**：高协调分不保证任务成功；graph 在 Research 场景最好；更多 Agent/通信不单调改善结果；cognitive planning 的里程碑提升约 3%。
11. **局限**：大量过程指标依赖 LLM Judge；不同场景的 Task Score 不同尺度；样本数/迭代描述存在局部不一致；无反馈式种子调度。
12. **分类理由**：它提供交互与里程碑“覆盖/过程测量”，但不以覆盖增量生成新测试，因此只能标为邻近 benchmark。
13. **PPT 可用图表**：Figure 2（MARBLE 框架）；拓扑、规划、迭代和 Agent 数消融图；Table 1（跨场景结果）。
14. **一句话总结**：MultiAgentBench 适合说明“该测哪些过程行为”，不应被写成 coverage-guided fuzzing 算法。

## 3. 第 7 类：轨迹与因果驱动测试

### 3.1 AgentRewardBench: Evaluating Automatic Evaluations of Web Agent Trajectories

1. **中文主题**：用专家标注轨迹测试自动评测器是否可信。
2. **元数据**：Xing Han Lù 等；COLM 2025；arXiv:2504.08942；正式 OpenReview 版本，无已核验 DOI。
3. **证据状态**：已阅读全文。
4. **问题**：规则 evaluator 和 LLM-as-a-Judge 是否会把失败轨迹误判为成功，从而扭曲 Agent 排名。
5. **基本思路**：把 evaluator 当成被测对象，以专家成功/副作用/重复标签作为 reference。
6. **流程**：收集真实 Web 轨迹 → 专家标注 → 多种规则/模型判定 → 计算 precision、recall、F1 → 分析对 Agent 成功率的偏差。
7. **实现**：1,302 条轨迹、351 个任务、5 个 Web benchmark、4 类 Agent、6 名专家。
8. **指标**：成功判断 precision/recall/F1、副作用与重复识别、成功率估计偏差。
9. **实验**：比较规则 evaluator、专用轨迹模型、不同 LLM Judge、截图与 A11Y 输入。
10. **结果**：所测 LLM Judge 的成功判断 precision 均未超过 70%；规则约 83.8% precision、55.9% recall；LLM Judge 容易相信 Agent 自述并高估成功。
11. **局限**：仅 Web 领域；专家标签也有噪声；动态网站和闭源模型漂移；未系统比较费用、延迟和重复调用方差。
12. **分类理由**：它直接读取完整轨迹并测试轨迹级 Oracle 的可靠性，是“轨迹评测”子类的代表。
13. **PPT 可用图表**：评测器比较主表、precision–recall 结果、不同 Agent/benchmark 偏差图、错误类型图。
14. **一句话总结**：AgentRewardBench 说明 Agent 测试首先要怀疑“分数是怎样判出来的”。

### 3.2 AJ-Bench: Benchmarking Agent-as-a-Judge for Environment-Aware Evaluation

1. **中文主题**：测试能够主动访问环境的 Judge Agent。
2. **元数据**：Wentao Shi 等；Findings of ACL 2026；DOI:10.18653/v1/2026.findings-acl.1269。
3. **证据状态**：已阅读全文；Crossref/OpenAlex 精确核验。
4. **问题**：Judge 只读文本轨迹是否足够；主动搜索、读取数据库或检查 GUI 状态能否改善判定。
5. **基本思路**：让 Judge 自己调用工具取得外部证据，分开测试信息获取、状态验证和过程验证能力。
6. **流程**：任务与候选轨迹 → Judge 决定是否调用工具 → 获取环境证据 → 给出判定 → 与人工/构造标签比较。
7. **实现**：155 个任务、516 条正负轨迹，覆盖三类环境验证模式。
8. **指标**：precision、recall、F1，并按领域与验证类型拆分。
9. **实验**：environment-aware Agent-as-a-Judge 与 text-only LLM-as-a-Judge 对比，分析工具能力的贡献。
10. **结果**：主动环境验证整体优于纯文本 Judge，但绝对性能仍不足以作为无需复核的最终 Oracle。
11. **局限**：Judge 的工具使用能力和评价推理耦合；三类领域与固定协议限制外推。
12. **分类理由**：它扩展了轨迹评价的证据边界，但仍主要是 evaluator 元测试而非因果归因。
13. **PPT 可用图表**：总体任务分类/框架图、主结果表、工具使用消融。
14. **一句话总结**：AJ-Bench 表明 Judge 需要“亲自查环境”，但会用工具不等于一定会正确判定。

### 3.3 Aligning Agents via Planning: A Benchmark for Trajectory-Level Reward Modeling（Plan-RewardBench）

1. **中文主题**：用长轨迹与 hard negative（难负例）压力测试 reward model。
2. **元数据**：Jiaxuan Wang 等；ACL 2026；DOI:10.18653/v1/2026.acl-long.1062。
3. **证据状态**：已阅读全文；正式版本双源核验。
4. **问题**：轨迹评测器是否真正理解规划、恢复、工具相关性和安全错误，还是只识别表面差异。
5. **基本思路**：固定任务与环境，构造自然 rollout、规则扰动和最小编辑的成对轨迹，让 evaluator 选择更好的一个。
6. **流程**：收集轨迹 → 构造/筛选难负例 → 多模型 panel 与人工审计 → 评测 reward model/LLM Judge → 检查长度、顺序和场景偏差。
7. **实现**：覆盖安全拒绝、无关/不可用工具、复杂规划和错误恢复四类场景。
8. **指标**：pairwise accuracy、macro accuracy、人类一致性、order-swap consistency。
9. **实验**：多类 evaluator 在长短轨迹、不同场景和顺序交换条件下比较。
10. **结果**：长轨迹使多数 evaluator 退化；不同模型在规划、恢复、工具和安全场景表现互补，没有统一赢家。
11. **局限**：文本工具轨迹为主；多数标签来自模型 panel；场景不均衡。
12. **分类理由**：它测试轨迹级 reward/判定机制，是轨迹质量评测子类。
13. **PPT 可用图表**：数据构造图、场景分类表、主结果与长度/顺序消融图。
14. **一句话总结**：Plan-RewardBench 用受控难负例检查 evaluator 是否真的理解“哪一步计划错了”。

### 3.4 Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems（Who&When）

1. **中文主题**：首次系统定义“哪个 Agent、哪一步导致失败”的自动归因任务。
2. **元数据**：Shaokun Zhang 等；ICML 2025，PMLR 267；arXiv:2505.00212v3。
3. **证据状态**：已阅读全文；PMLR 正式身份与本地 PDF 核验。
4. **问题**：MAS 失败后，能否自动识别责任 Agent 和最早决定性错误步骤。
5. **基本思路**：构建带 Agent/step 标注的失败轨迹集，并测试一次性阅读、逐步检查和分段搜索等方法。
6. **流程**：收集 127 个 MAS 的失败日志 → 人工/规则标注责任 Agent 与步骤 → 输入归因模型 → 输出 Agent/step → 与真值比较。
7. **实现**：Who&When 包含 algorithm-generated 与 hand-crafted 系统，提供细粒度归因标签。
8. **指标**：Agent accuracy、严格 step accuracy 与容差 step accuracy。
9. **实验**：不同 LLM、历史长度、查询标签和三类自动归因协议。
10. **结果**：最佳方法 Agent accuracy 53.5%，step accuracy 仅 14.2%；手工系统的最佳步骤准确率更低，约 8.77%。
11. **局限**：output-heavy 轨迹缺输入和环境状态；标注“唯一决定步骤”可能简化多根因；数据规模有限。
12. **分类理由**：它奠定责任 Agent/关键步骤定位的任务定义和基准。
13. **PPT 可用图表**：Figure 1（问题定义）；数据构建/方法框架；主结果表。
14. **一句话总结**：Who&When 证明“找出哪个 Agent”尚可，但“精确定位哪一步”远未解决。

### 3.5 StepFinder: A Temporal Semantic Framework for Failure Attribution in Multi-Agent Systems

1. **中文主题**：用轻量时序模型低成本排序根因步骤。
2. **元数据**：Taiyu Zhu 等；KDD 2026；DOI:10.1145/3770855.3817991；arXiv:2606.03467。
3. **证据状态**：已阅读全文；正式 DOI 双源核验。
4. **问题**：逐步调用 LLM 检查长轨迹准确率低且 token/延迟高。
5. **基本思路**：缓存每步 embedding（向量表示），结合时间、Agent 身份和多尺度差分输出异常分数。
6. **流程**：轨迹编码 → agent-aware 时序交互 → 多尺度特征 → 每步异常分数 → top-k 候选。
7. **实现**：双向时序特征、位置偏置、temporal-consistency loss；推理阶段不生成文本。
8. **指标**：Acc@1/2/3、MRR@3、容差准确率、token 和延迟。
9. **实验**：Who&When 两个子集；与 all-at-once、step-by-step、binary search 和序列模型比较。
10. **结果**：在复杂 hand-crafted 子集更强；推理零生成 token，每样本约 0.61/3.56 秒；时序特征贡献最大。
11. **局限**：需要根因步骤标签；主要在一个 benchmark 家族验证；可能学习位置偏差。
12. **分类理由**：典型的轨迹相关性定位方法，不执行反事实干预。
13. **PPT 可用图表**：模型架构图、主结果表、效率表、组件消融。
14. **一句话总结**：StepFinder 提供可规模化的候选筛查，但“异常分高”仍不是因果证明。

### 3.6 Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems（TraceElephant）

1. **中文主题**：测试完整可观测性和可重放环境对故障归因的影响。
2. **元数据**：Mengzhuo Chen 等；ACL 2026；DOI:10.18653/v1/2026.acl-long.912。
3. **证据状态**：已阅读全文；ACL/Crossref/OpenAlex 核验。
4. **问题**：只记录 Agent 输出会不会使根因从证据上不可识别。
5. **基本思路**：同时提供输入、metadata、工具交互和可执行环境，并做静态字段移除与动态 replay 对比。
6. **流程**：middleware 采集全轨迹 → 专家标 Agent/步骤 → 不同可见度归因 → 局部重放 → 比较准确率。
7. **实现**：Captain-Agent、Magentic-One、SWE-Agent；380 条轨迹、220 条失败。
8. **指标**：Agent accuracy、exact step accuracy、容差 step accuracy。
9. **实验**：完整 trace、output-only、移除 input/metadata、动态重放；三次独立运行。
10. **结果**：完整轨迹使 Agent 归因平均提升约 22%，step 归因提升约 76%；可运行环境再提高约 10%。
11. **局限**：三个系统；完整轨迹含隐私、提示与密钥；局部重放只观察后续 3 步。
12. **分类理由**：它证明轨迹观测边界直接决定归因上限，并提供重放基准。
13. **PPT 可用图表**：TraceElephant 架构/数据流程图、可观测性消融主图和重放结果。
14. **一句话总结**：没有完整输入和状态时，归因失败可能不是模型不够强，而是证据根本不充分。

### 3.7 Towards Self-Improving Error Diagnosis in Multi-Agent Systems（ErrorProbe）

1. **中文主题**：用结构化回溯、多 Agent 验证和已验证记忆改进错误定位。
2. **元数据**：Jiazheng Li、Emine Yilmaz、Bei Chen、Thu Le；Findings of ACL 2026；DOI:10.18653/v1/2026.findings-acl.98。
3. **证据状态**：本轮已阅读全文；Crossref/ACL Anthology 正式身份核验。
4. **问题**：长轨迹、延迟显现和分布变化使一次性 LLM Judge 难以定位最早错误。
5. **基本思路**：先用 MAST taxonomy（多智能体失败分类）标局部异常，再从症状反向裁剪依赖，最后由 Strategist/Investigator/Arbiter 验证假设。
6. **流程**：失败症状 → 结构分解/反向追踪 → 多 Agent 调查 → 工具证据验证 → 归因 → 仅将已验证模式写入 memory。
7. **实现**：verified episodic memory（已验证情景记忆）避免把幻觉诊断永久写入；支持 cold start 到持续积累。
8. **指标**：Agent accuracy、step accuracy、随记忆增长的学习曲线与跨域迁移。
9. **实验**：TracerTraj 与 Who&When 等三个基准；与 LLM-as-a-Judge 和 Agent-as-a-Judge 协议比较。
10. **结果**：论文报告 step accuracy 相对基线显著提升；验证记忆带来约 +13.4 个百分点的持续增益，Agent accuracy 增益较小。
11. **局限**：显式失败信号更适合该流程，silent failure 较难；多 Agent 调查成本高；记忆仍可能受验证 Oracle 错误污染。
12. **分类理由**：它属于“责任 Agent/关键步骤定位”，并以可执行证据验证和记忆增强诊断。
13. **PPT 可用图表**：Figure 2（框架）；Table 1（主结果）；Figure 3（记忆学习曲线）。
14. **一句话总结**：ErrorProbe 的关键不是“记住更多解释”，而是只记住被工具证据验证过的失败模式。

### 3.8 REFLECT: Intervention-Supported Error Attribution for Silent Failures in LLM Agent Traces

1. **中文主题**：通过定向修复和前缀保持重放验证 silent failure（静默失败）的归因。
2. **元数据**：Xiaofeng Lin 等；ICML 2026 FAGEN Workshop；arXiv:2606.09071；无正式 DOI。
3. **证据状态**：已阅读全文；arXiv/OpenAlex 精确身份。
4. **问题**：没有异常或崩溃的错误轨迹中，LLM Judge 的“看起来像根因”不能证明因果。
5. **基本思路**：生成候选根因与诊断特定 patch，固定此前轨迹并重放；结果翻转后再用对比证据修正归因。
6. **流程**：初步定位 → repair plan → 前缀保持干预 → replay → outcome flip → 最终 attribution record。
7. **实现**：同时支持有 ground truth 的 outcome Oracle 与无答案 proxy；记录 verified/fallback 状态。
8. **指标**：Exact/Off-by-1 step、覆盖率、verified 比例、outcome verifier AUROC/F1。
9. **实验**：WTQ、GAIA、SWE 相关轨迹和推理 benchmark；same-auditor 条件下比较多类基线。
10. **结果**：论文报告四个 benchmark 均取得最高定位准确率，结构化工具轨迹提升最大；干预成功时证据最强。
11. **局限**：成功修复只证明充分性，不证明原因唯一或最小；需要可重放环境；patch 质量会影响归因。
12. **分类理由**：它从相关性候选迈向“干预支持的归因验证”。
13. **PPT 可用图表**：方法总体框架、主结果表、verified/fallback 与 outcome verifier 消融。
14. **一句话总结**：REFLECT 不把“修好一次”直接当成真相，而是把重放结果作为更新归因的证据。

### 3.9 AgentTrace: Causal Graph Tracing for Root Cause Analysis in Deployed Multi-Agent Systems

1. **中文主题**：从执行日志构建依赖图并快速反向定位根因。
2. **元数据**：Zhaohui Geoffrey Wang；ICLR 2026 Workshop on Agents in the Wild；arXiv:2603.14688v2。
3. **证据状态**：本轮已阅读全文；论文首页与 OpenAlex/arXiv 身份一致。
4. **问题**：多 Agent 错误会沿消息和数据依赖级联，最终错误节点常不是最早根因。
5. **基本思路**：把动作建成有向图，用同 Agent 顺序、通信和数据依赖三类边连接；从错误节点反向 BFS，再按可解释特征排名。
6. **流程**：采集日志 → 构图 → 反向遍历候选 → 位置/结构/内容/流/置信度打分 → 输出根因排序。
7. **实现**：17 个特征；位置权重 0.70、结构 0.20，其余较小；调试时无需 LLM 推理。
8. **指标**：Hit@1/3/5、MRR（平均倒数排名）、运行时间。
9. **实验**：550 个合成失败场景、10 个领域、8–15 个动作；与启发式和 LLM 基线比较。
10. **结果**：不同故障类型/长度/位置的 Hit@1 约 92.7%–96.1%，亚秒级；消融显示位置特征主导。
11. **局限**：合成、单根因场景；高性能可能主要来自注入位置规则；论文所谓“causal graph”是日志依赖图，不是 do-intervention 因果识别。
12. **分类理由**：属于因果图式轨迹定位，但因果强度弱于执行式反事实重放。
13. **PPT 可用图表**：Figure 1（总体框架）；Tables 3–5（准确率、消融、鲁棒性）。
14. **一句话总结**：AgentTrace 很快、可解释，但更准确的称呼是“依赖图根因排序”，不能等同于因果干预证明。

### 3.10 Automatic Failure Attribution and Critical Step Prediction Method for Multi-Agent Systems Based on Causal Inference

1. **中文主题**：用多粒度因果图、Shapley 值和反事实模拟定位 MAS 的责任 Agent 与步骤。
2. **元数据**：Guoqing Ma 等；论文标注 AAAI 2026；arXiv:2509.08682；正式 DOI/会议索引仍待核验。
3. **证据状态**：已阅读全文（本地 PDF）；出版身份部分核验。
4. **问题**：相关性方法容易把下游症状当作上游根因。
5. **基本思路**：Agent 层做 performance causal inversion（性能因果反演），用 Shapley 分配责任；步骤层用 CDC-MAS 学习时序因果结构。
6. **流程**：轨迹特征 → Agent 层因果图与 Shapley → 步骤层因果发现 → 关键步骤 → 生成优化建议 → 反事实模拟验证。
7. **实现**：同时建模 Agent 与步骤粒度，强调非平稳多 Agent 交互中的因果发现。
8. **指标**：Agent/step accuracy、联合归因、优化后的任务成功率。
9. **实验**：Who&When 与 TRAIL；与 LLM Judge、统计与定位方法比较。
10. **结果**：论文报告最高 step accuracy 36.2%，归因指导的优化使任务成功率平均提高 22.4%。
11. **局限**：因果图来自观测数据与建模假设；反事实模拟不是完全真实环境重放；出版身份需继续确认。
12. **分类理由**：直接使用因果建模和反事实验证，属于因果归因子类。
13. **PPT 可用图表**：Figure 1（整体因果框架）；方法流程图；主结果和优化验证表。
14. **一句话总结**：该工作把 Agent 级责任和步骤级定位统一到因果建模中，但证据仍受结构学习假设限制。

### 3.11 CausalFlow: Causal Attribution and Counterfactual Repair for LLM Agent Failures

1. **中文主题**：通过最小反事实修复，把失败轨迹转化为可验证监督。
2. **元数据**：Akash Bonagiri 等；2026；arXiv:2605.25338v1；OpenAlex 精确匹配，无正式会议版。
3. **证据状态**：本轮已阅读全文（13 页主文及附录）。
4. **问题**：整段重写虽可能修复任务，却不能说明哪一步真正负责，也难形成干净的训练对。
5. **基本思路**：逐步替换候选步骤并重执行，计算 CRS（Causal Responsibility Score，因果责任分数）；只保留能翻转结果且修改最小的 repair。
6. **流程**：失败轨迹 → 候选步骤干预 → CRS → 生成多个最小修复 → 重执行/Outcome Predictor 验证 → 多 Agent 共识 → 输出错误/修复对。
7. **实现**：最小性由语义/编辑变化衡量；既支持 test-time repair，也支持训练数据生成。
8. **指标**：repair rate、minimality、causal consensus、修复前后 accuracy、CRS precision。
9. **实验**：GSM8K、MBPP、HotpotQA、MedBrowseComp；比较 Direct、Self-Refine、Self-Reflection 等。
10. **结果**：四个 benchmark 均提升；平均 minimality 约 0.79–0.87；检索型任务上相对启发式修复更有优势；结构化 trace 会降低初始准确率，但修复后可恢复。
11. **局限**：依赖 LLM 生成有效干预；重执行成本高；检索错误未必能靠局部改写修复；部分任务依赖 LLM Judge；结构化日志本身有准确率开销。
12. **分类理由**：它明确以反事实干预和结果翻转定义步骤责任，并把归因连到修复。
13. **PPT 可用图表**：Figure 1（总体管线）；Tables 1–2（修复、最小性与准确率）；Table 5（归因可靠性）。
14. **一句话总结**：CausalFlow 的贡献不仅是“修好”，而是寻找能以最小改动改变结局的步骤。

### 3.12 Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures（CAR）

1. **中文主题**：在随机 Agent 中用重复反事实重放估计步骤的因果效应。
2. **元数据**：Jaineet Shah；2026；arXiv:2606.08275v1；OpenAlex/arXiv 身份核验，无正式会议版。
3. **证据状态**：本轮已阅读全文（8 页）；已确定为第 7 类 PPT 深入案例。
4. **问题**：有害动作的执行步通常只是结果，真正决定可能发生在更早一步；单次重放又会被 LLM 随机性误导。
5. **基本思路**：把轨迹建模为 Structural Causal Model（结构因果模型），对步骤执行 do-operation（主动设置变量的因果操作），从同一前缀重复向后运行并比较结果分布。
6. **流程**：记录可重放状态 → 选择步骤 → do_resample/do_action/do_observation/do_context/do_policy → K 次向后重放 → 估计效应与置信区间 → Point of Commitment（结果锁定点）/Shapley 归因。
7. **实现**：五类干预；action-match rate 衡量重放忠实度；single-step contrastive estimator 定位单步；预算受限 Monte-Carlo Shapley 处理多步交互。
8. **指标**：坏结果概率变化、Wilson/bootstrap Confidence Interval（置信区间）、Shapley efficiency、replay action-match rate。
9. **实验**：带已知因果结构的三步 synthetic SCM；另用 support-agent injection 展示交互报告。
10. **结果**：单关键步骤实验恢复真正决策步；两步 AND 失败中 Shapley 为约 0.44、0.45、0，责任和 0.909，接近解析真值 0.91。
11. **局限**：主要定量验证是合成 SCM；真实案例没有大规模人工因果真值；重放成本随步骤和样本数增长；环境漂移会破坏可重放性。
12. **分类理由**：CAR 用实际干预、重复执行和结果分布回答“哪一步造成失败”，最符合“轨迹与因果驱动”。
13. **PPT 可用图表**：Figure 1（support-agent 归因报告）；Section 5 的 pivotal-step 与 two-step interaction 数值；干预代数说明。
14. **一句话总结**：CAR 的核心不是让 Judge 猜根因，而是把每个归因假设变成可以重复执行的反事实测试。

## 4. 跨论文综合

### 4.1 第 6 类共同流程

`测试目标 → 初始种子 → Agent 执行 → 收集工具/状态/资源/轨迹反馈 → 判断是否产生新行为或更高风险 → 更新种子与变异策略 → Oracle 确认失败`

- VeriGrey：反馈是工具序列。
- FLARE：反馈是主体内与主体间行为覆盖。
- AgentDoS：反馈是资源生命周期和消耗。
- MUZZLE：反馈是轨迹中的注入面与失败原因。
- MultiAgentBench：提供里程碑和过程指标，但不执行反馈式搜索。

**综合判断**：第 6 类还没有统一的 Agent coverage 定义。工具序列可计算但语义粗糙；语义行为覆盖更贴近 Agent，但依赖规格抽取与 LLM 映射；风险反馈能直接找漏洞，却只覆盖特定风险。

### 4.2 第 7 类共同流程

`完整轨迹 → 轨迹质量/评测器检查 → 候选 Agent/步骤定位 → 定义干预 → 固定前缀并重复重放 → 比较结果分布 → 单步或多步责任分配`

- AgentRewardBench、AJ-Bench、Plan-RewardBench：检查轨迹与 evaluator 是否可信。
- Who&When、StepFinder、TraceElephant、ErrorProbe：定位责任 Agent/步骤并研究可观测性与效率。
- REFLECT：用修复重放为归因提供干预证据。
- AgentTrace：基于日志依赖图快速排序，但没有执行式因果识别。
- Automatic Failure Attribution、CausalFlow、CAR：分别通过因果结构学习、最小结果翻转和随机反事实重放增强因果证据。

**综合判断**：第 7 类应明确区分“轨迹相关性定位”和“因果验证”。前者成本低，适合筛候选；后者证据更强，但依赖可重放环境、可靠 outcome Oracle 和更多执行预算。

## 5. 后续 PPT 的证据选择

- 第 6 类深入案例：**VeriGrey**。首选 Figure 2；实验使用 70.7%、59.6%、约 44.0% 的主/消融结果，并明确使用“百分点”。
- 第 7 类深入案例：**CAR**。首选 Figure 1；实验使用 pivotal-step 与 `0.44/0.45/≈0，sum=0.909 vs 0.91`，同时醒目标注“主要定量验证为合成 SCM”。
- 文献地图中以实心标记上述 17 篇已阅读全文论文；`SafeVault/SafeFault` 不作为论文展示，可在备注中解释为未解析条目。
- MultiAgentBench 标注“邻近工作”；AgentTrace 标注“依赖图定位，非执行式干预”；所有预印本标注“arXiv preprint”。

## 6. 主要来源

- [VeriGrey](https://arxiv.org/abs/2603.17639)
- [FLARE](https://arxiv.org/abs/2604.05289)
- [AgentDoS / USENIX Security 2026](https://www.usenix.org/conference/usenixsecurity26/presentation/luo)
- [MUZZLE / USENIX Security 2026](https://www.usenix.org/conference/usenixsecurity26/technical-sessions)
- [MultiAgentBench / ACL 2025](https://aclanthology.org/2025.acl-long.421/)
- [AgentRewardBench](https://arxiv.org/abs/2504.08942)
- [AJ-Bench / Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1269/)
- [Plan-RewardBench / ACL 2026](https://aclanthology.org/2026.acl-long.1062/)
- [Who&When](https://arxiv.org/abs/2505.00212)
- [StepFinder](https://arxiv.org/abs/2606.03467)
- [TraceElephant / ACL 2026](https://aclanthology.org/2026.acl-long.912/)
- [ErrorProbe / Findings ACL 2026](https://aclanthology.org/2026.findings-acl.98/)
- [REFLECT](https://arxiv.org/abs/2606.09071)
- [AgentTrace](https://arxiv.org/abs/2603.14688)
- [Automatic Failure Attribution](https://arxiv.org/abs/2509.08682)
- [CausalFlow](https://arxiv.org/abs/2605.25338)
- [Causal Agent Replay](https://arxiv.org/abs/2606.08275)
