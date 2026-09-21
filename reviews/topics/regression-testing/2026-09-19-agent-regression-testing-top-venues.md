# LLM Agent 回归测试：软件工程顶会与近邻工作检索

> 检索日期：2026-09-19（Asia/Shanghai）  
> 范围：2023–2026；优先 ICSE、FSE、ASE、ISSTA、ICST；严格排除“用 agent 测普通软件”。  
> 核心判据：被测对象必须是 LLM agent/agentic system；必须比较同一任务或场景下的旧/新 agent、prompt、model、tool、skill、memory 或配置，或把历史失败固化为可重复 CI 门禁。仅做一次性 benchmark、一般鲁棒性测试或重复运行，不自动算 regression testing。

## 结论先行

1. **在所查 2023–2026 软件工程旗舰会议主赛道中，我没有找到一篇已经完整提出并验证“LLM agent 版本 A→B 回归测试系统”的论文。** 这是实质性的研究空白，不是检索遗漏后可以随便用一般 benchmark 填补的空白。
2. 顶会主赛道中最接近的直接证据是 **Tangent（ASE 2026）**：它研究的就是 agent application 测试，并发现 10 位业界受访者中有 **50%** 在模型更新时做 continuous evaluation/regression testing，常见做法是 rerun、before–after comparison、downstream performance evaluation 和 trace inspection；但它是实践调查，**没有提出回归测试算法**。
3. **Regression Accumulation in Multi-Turn LLM Programming Conversations（ASE 2026）** 确实提出了逐轮保留旧测试、计算 regression pass rate、用 verification gate 阻止退化的协议；但其 SUT 是多轮 LLM 代码建议，不是带工具/状态/环境的 agent。严格口径下应列为“方法近邻”，不能冒充 agent regression paper。
4. 真正直接、可实现的 agent 回归测试方法集中在 2026 年预印本：**Chronicle、AgentLens、Layer-Isolated Evaluation、TDAD、The Regression Tax**。其中：
   - Chronicle 解决历史事故的确定性 replay；
   - AgentLens 做当前版本与 anchor run 的 nightly trajectory diff；
   - Layer-Isolated Evaluation 做每层 deterministic CI gate；
   - TDAD 测规格 v1→v2 后旧行为是否保持；
   - Regression Tax 用 paired task transitions 揭示平均分掩盖的“新增 skill 反而弄坏旧任务”。
5. 唯一已正式发表、且与“持续 agent 评测”高度相符的近邻是 **Continuous Benchmark Generation（ICSE 2026 的 LLM4Code workshop）**，但它不是 ICSE Research Track。

## 1. 检索与核验方法

### 数据源

- 会议一手来源：ICSE/FSE/ASE/ISSTA/ICST 的 `conf.researchr.org` 官方 program/track 页面。
- 学术元数据：Semantic Scholar、Crossref、OpenAlex、DBLP。
- 开放全文与版本：arXiv；有 DOI 时用 Crossref + OpenAlex 交叉核验。
- 引用数：Semantic Scholar，快照日期 2026-09-19；新论文的低引用数不作为排除条件。

### 查询族

- `LLM agent regression testing version upgrade degradation`
- `agentic system behavioral differential testing model versions`
- `LLM agent continuous evaluation CI regression`
- `LLM agent trajectory replay regression testing`
- 会议定向检索：`site:conf.researchr.org (ICSE|FSE|ASE|ISSTA|ICST) agent regression|continuous evaluation|version|behavioral differential`
- 补充概念：`nightly evaluation`、`anchor run`、`locked baseline`、`spec evolution`、`skill-induced regression`、`cut-point replay`。

### 纳入/排除规则

纳入至少满足一项：

- 同一任务上做 agent 旧/新版本的 paired comparison；
- 将 baseline/anchor run 固定后在 CI/nightly 中检测退化；
- 规格、prompt、model、skill、tool 或 agent scaffold 更新后，验证旧行为仍被保持；
- 把线上失败 trace 固化成可重复执行的 regression test。

排除：

- agent 只是测试普通 app/code 的 tester，例如 WebTestPilot、MuMuTestUp、WebCQ、TestAgent；
- 只评估普通 LLM/code generation，没有 agent loop、工具、环境或状态；
- 只重复运行来测稳定性/归因，没有旧版—新版比较或回归门禁；
- 一次性安全/鲁棒性测试，没有将结果固化为版本回归测试。

## 2. 软件工程顶会主赛道：严格结果

| 论文 | Venue / 身份 | 元数据与开放全文 | 为什么与 agent regression 有关 | 严格判定 | 证据层级 |
|---|---|---|---|---|---|
| **Tangent: An Empirical Study of Testing Practices for LLM-Based Agent Applications** — Pan et al. | ASE 2026 Research Papers，CCF-A；会议 2026-10-12 至 16，当前尚未举行 | DOI `10.1145/3832783.3837414`；[arXiv:2608.08413](https://arxiv.org/abs/2608.08413)；[ASE 官方 track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track)；S2 引用 1 | 全文 §6：50% 的 10 位资深从业者在模型更新时做 continuous evaluation/regression testing，采用 reruns、before–after comparison、downstream performance evaluation、trace inspection。论文还指出当前 agent tests 多为窄范围 unit test、heavy mocking、shallow assertions。 | **直接相关，但不是方法论文**。它证明需求真实存在并给出现状/缺口，不能用来声称已有成熟 regression framework。 | 全文已检查；会议官方页面确认；DOI 尚未在 Crossref/OpenAlex 生效，故为**部分核验**。 |
| **Regression Accumulation in Multi-Turn LLM Programming Conversations** — Yonghui (Andie) Huang et al. | ASE 2026 Research Papers，CCF-A；当前尚未举行 | [arXiv:2607.01855](https://arxiv.org/abs/2607.01855)；[ASE 官方 track](https://conf.researchr.org/track/ase-2026/ase-2026-research-track)；S2 引用 2 | 542 个任务被扩展成 8-turn requirement-evolution chains；每轮重跑此前测试，定义 regression pass rate；六个模型中 40%–73% 的任务丢失过往正确行为；Verification Gate 将 DeepSeek-V3 final-turn quality 从 75.8% 提到 87.9%，Llama-3.1-8B 从 31.6% 提到 47.3%。 | **边界论文，严格排除出 agent 核心集**：SUT 是多轮 LLM 编程对话/代码建议，不是 tool-using agentic system。但“历史测试保留 + 逐轮回归率 + rollback/retry gate”非常适合作为 agent regression protocol 的基线。 | 全文已检查；官方 program + arXiv 确认；正式 ACM DOI 尚未发现，arXiv 元数据已核验。 |

### 为什么其他已找到的顶会 agent-testing 论文不应被误标为回归测试

| 论文 | Venue | 能提供什么 | 为什么还不是 regression testing |
|---|---|---|---|
| **SpecOps** | ICSE 2026 Research | 可自动生成、布置、执行和判断真实 GUI/CLI/Web agent 测试；适合把固定 suite 重跑到新版本 | 原论文评估不同 agent 的一次性 bug detection，没有 paired old/new build、baseline diff 或 regression alert。 |
| **AgentInspect** | ISSTA 2026 Research（program tentative） | 确定性轨迹规则、异常工具响应模拟，适合成为 regression oracle | 实验比较真实/模拟 tool responses，不比较 agent 版本，也没有 CI baseline。 |
| **LogicHunter** | ISSTA 2026 Research（program tentative） | specification-aware fuzzing + agentic oracle，可发现 agent framework 的静默错误 | 目标是 fuzzing/bug discovery，不是跨版本行为保持。 |
| **FAMAS / Spectrum-based Failure Attribution** | FSE 2026 Research | 多次 replay 后从 passing/failing spectra 定位 MAS 的致错 action | replay 用于 fault localization；没有“修改前/修改后”回归判定。 |
| **AgentChaos** | ASE 2026 Research | 65 种 LLM API fault configurations 下测 agent 退化，适合生成 resilience regression suite | 对比的是无故障/有故障或架构间差异，不是同一 agent 变更前后的 regression gate。 |
| **llmmas-otel** | ICST 2026 Tool Showcase | 统一 trace 与 fault injection 坐标，可保存 baseline/faulty traces | 是 observability/fault-injection 基础设施；论文未实现版本基线与回归决策。 |

## 3. 直接命中 agent regression 的核心近邻工作

这些论文不是目标顶会主赛道，但在技术上比大多数顶会 agent-testing 论文更直接回答“如何对 agent 做回归测试”。

### 3.1 Chronicle: Cut-Point Replay for Regression Testing of LLM Agents

- **身份**：2026-09-17 发布的 arXiv 预印本；[arXiv:2609.20625](https://arxiv.org/abs/2609.20625)，目前尚未被 S2 收录。
- **直接性**：标题与方法都明确是 agent regression testing。它在 model/tool 等非确定边界记录 immutable envelopes；回归时选择 cut point，一部分边界重放旧记录，另一部分用新代码 live execution。这样可以把一次 production incident 变成每次 commit 都运行的测试；full replay 不需要模型调用，而 cut-point replay 是否调用模型取决于哪些边界被设为 live。论文的 CI benchmark 使用模拟模型边界，因此不产生 provider 调用。
- **评价**：6 个人工整理的历史事故；full replay 在 20 次重复中 0 divergence；cut-point tests 对 6/6 场景均能 fail faulty code、pass guarded fix 与 benign edit；192 个一阶 mutants 中杀死 51 个，而 full-stub baseline 为 0；每 boundary 记录开销 23 μs；全套一次约 3.6 ms。
- **弱点**：只有 6 个 curated incidents，incident、guard、assertion 共同设计；不支持 streaming、并行 tool calls，也不能重放 stubbed exception；192 mutants 中 141 存活，单事故 fixture 的覆盖面窄。
- **为何属于 regression**：输入不是重新生成的 benchmark，而是“旧失败 trace + 新代码”；判定目标正是 guard/fix 是否保持，且明确部署在 CI。

### 3.2 AgentLens: Production-Assessed Trajectory Reviews for Coding Agent Evaluation

- **身份**：arXiv 预印本；[arXiv:2607.06624](https://arxiv.org/abs/2607.06624)；S2 引用 2；开放代码由 arXiv 页面链接。
- **直接性**：candidate agent version 在固定 benchmark 上生成完整 trajectories，与 anchor run 做 side-by-side comparison；pipeline 支持 manual/nightly/weekly，检测 statistically significant degradation 后通知 maintainer。
- **Technique**：formal verifiers + LLM-written trajectory reviews；度量 end result、instruction compliance、pitfalls、tool-call quality、pleasantness；同时保存 trace、termination reason、judge evidence 与 experiment tracking。
- **重要案例**：nightly run 通过 trajectory degradation 与 abnormal termination 定位到了 parallel tool calling 的 `ConcurrentModificationException`；这是 final answer 指标容易漏掉的 harness regression。
- **弱点**：当前公开 fold 只有 16 scenarios × 2 personas = 32 trajectories，重点是 Java/IDE coding agents；LLM judge 存在自偏好——GPT-5.5 与 Sonnet-4.6 互换 judge 时，23% task–metric comparisons 改变 winner；尚缺系统的人类一致性研究。
- **为何属于 regression**：它实际运行 successive versions，对 current 与 anchor 做 paired trajectory diff，并形成 nightly product regression pipeline。

### 3.3 Layer-Isolated Evaluation: ... Regression-Locked Test Harness

- **身份**：arXiv 预印本；[arXiv:2606.11686](https://arxiv.org/abs/2606.11686)；S2 引用 0。
- **直接性**：把生产 ordering agent 拆成 ontology、intent、routing、decomposition、escalation、safety、memory、envelope/defense 等层；每层在 no-LLM pure mode 中有独立 assertion slice，并与 locked baseline 比较。
- **评价**：238 baseline cases / 23 slices，其中 pure suite 225 cases 约 2.39 秒；注入 7 种单层 regression。总体 pass rate 只下降 1.7–5.9 个百分点，容易被噪声掩盖；对应 slice 下降 25–91 个百分点，7/7 对应 slice 均在 top-3，平均 rank 1.29。第二个结构不同的 tenant 上也复现 7 种注入的对应 slice crater。
- **弱点**：单一 F&B ordering domain、PydanticAI；研究主要依赖人为注入，尚不能证明能定位自然演化中出现的 organic regressions；四个 slice 无覆盖；只覆盖 deterministic scaffold，生成式层仍需 nightly live lane。论文明确承认 locked baseline 是 drift detector，不是 correctness oracle，错误基线会被忠实锁死。
- **为何属于 regression**：每个 PR 对固定每层 baseline 做硬门禁；实验直接注入层级退化并验证是否检测、定位。

### 3.4 Test-Driven AI Agent Definition (TDAD)

- **身份**：arXiv 预印本；[arXiv:2603.08806](https://arxiv.org/abs/2603.08806)；S2 引用 6。
- **直接性**：将 agent prompt 看成 compiled artifact；behavioral specification → executable tests → iterative prompt compilation。它专门设计 spec v1→v2 evolution scenarios，并定义 Spec-Update Regression Score（SURS）检查旧 invariant 是否保持。
- **防止“只对可见测试过拟合”**：visible/hidden split；MutationSmith 生成 plausible faulty prompt variants；hidden tests 只在 compilation 后评估。
- **评价**：4 个深规格 agent（SupportOps、DataInsights、IncidentRunbook、ExpenseGuard），每个 v1/v2 各 3 次，共 24 trials；v1 compile success 92%、mean hidden pass rate 97%；v2 compile success 58%、hidden pass rate 78%；mutation score 86–100%；mean regression safety 97.2%。
- **弱点**：仅 4 个 mini-products；所有角色与 AUT 都使用 Claude Sonnet 4.5，存在 shared-model bias；成功 compile 的 v2 比例仅 58%；“测试由 agent 生成、prompt 也由 agent 优化”仍可能共同盲区。
- **为何属于 regression**：不仅测试新规格，还显式度量 v1 invariants 在 v2 agent 中是否保持。

### 3.5 The Regression Tax: Decomposing Why Skills Help and Hurt LLM Agents

- **身份**：arXiv 预印本；[arXiv:2607.22520](https://arxiv.org/abs/2607.22520)；S2 引用 0。
- **直接性**：对同一任务 paired 运行 no-skill baseline 与 skill-enabled agent；把总分变化分解为 gain（原失败→通过）和 regression（原通过→失败），而不是只看净平均分。
- **评价**：近 6,000 runs、2 个 office automation benchmarks、3 个 model–harness stacks；观察到 324 个 regression transitions，抵消了 59% 的 gross gains。识别 skill-description osmosis、grounding displacement、verification displacement 三类退化机制。
- **弱点**：研究的是“加 skill”这一种变更；paired outcome 仍可能受 agent sampling 噪声影响；office automation 外部有效性有限；它是差分测量/机制研究，不是 CI 工具。
- **为何属于 regression**：它给出了最清晰的 task-level paired definition：同一任务在 baseline 成功、更新后失败才记为 regression，能揭穿平均分持平时的 gain/regression 抵消。

## 4. 正式发表但非旗舰主赛道的持续评测近邻

### Continuous Benchmark Generation for Evaluating Enterprise-scale LLM Agents

- **身份**：ICSE 2026 联办的 **LLM4Code 2026 workshop**，不是 ICSE Research Track；DOI [`10.1145/3786181.3788708`](https://doi.org/10.1145/3786181.3788708)；[官方页面](https://conf.researchr.org/details/icse-2026/llm4code-2026-papers/8/Continuous-Benchmark-Generation-for-Evaluating-Enterprise-scale-LLM-Agents)；[arXiv:2511.10049](https://arxiv.org/abs/2511.10049)；S2 引用 3。Crossref/OpenAlex 对 DOI、题名与年份一致，**Verified**。
- **想法**：企业服务、需求和平台持续演化，固定 benchmark 会陈旧；从半结构化高层意图文档、已迁移服务和参考 commits 自动生成、更新 benchmark，分离“测什么”（requirements）和“怎么生成实例”。
- **评价**：大型企业的平台迁移 case study；对 4 个 repository，生成 benchmark 相对人工 benchmark 的 precision 都为 1，recall 为 0.25–0.667，F1 为 0.4–0.8；还能排除人工 benchmark 中已经 obsolete 的文件。
- **边界**：它支持 evolving agent 的 longitudinal evaluation，但没有像 AgentLens 那样给出 paired regression decision、显著性门槛或 trajectory-level root cause；5 页 workshop 论文，证据规模有限。

### Evaluation-Driven Development and Operations of LLM Agents (EDDOps)

- **身份**：仍为 under-review preprint；[arXiv:2411.13768](https://arxiv.org/abs/2411.13768)；S2 引用 10。
- **贡献**：基于 multivocal literature review，提出把 offline development-time evaluation 与 online runtime evaluation 组成闭环，让评测证据治理 agent 的适应与再开发。
- **边界**：是 process model/reference architecture，不是一个可直接比较两个版本、输出 regression verdict 的实现；Layer-Isolated Evaluation 正是把它的 component-level baseline 思想具体化。

## 5. 研究空白：从这些论文还能做什么

当前工作只覆盖了回归测试空间的不同切片：

| 变化轴 | 当前最好证据 | 尚缺什么 |
|---|---|---|
| agent code / deterministic scaffold | Chronicle、Layer-Isolated | streaming、parallel tools、distributed MAS；真实 organic regression corpus |
| model / prompt / harness version | AgentLens | 多次随机运行的置信区间、judge drift 校准、跨 provider 可复现性 |
| specification evolution | TDAD | 大规模真实规格演化、人工 oracle、跨模型生成/测试隔离 |
| skill addition/removal | Regression Tax | 自动定位是哪条 skill 规则导致回归；skill 组合与顺序交互 |
| evolving environment/requirements | Continuous Benchmark Generation | benchmark change 与 agent change 解耦，否则无法判断退化来自 SUT 还是 oracle 漂移 |
| full agent stack | Tangent 指出的现实需求 | 一个统一的 `model × prompt × tool × memory × skill × environment` change matrix 和 regression adequacy 标准 |

最值得做的新工作是 **Causal Agent Regression Testing**：

1. 从生产 trace 与已有测试建立版本化 scenario corpus；
2. 记录 model/tool/environment/memory 边界，支持 Chronicle 式 selective replay；
3. 同一 scenario 对 old/new version 做 matched repeated runs，而不是比较两个独立均值；
4. oracle 同时检查 final state、tool side effects、trajectory invariants、latency/cost 与安全策略；
5. 把任务转移拆成 `gain / regression / persistent pass / persistent fail`，并报告 McNemar test、effect size 和置信区间；
6. 对检测到的 regression 逐轴替换 model、prompt、tool、memory 或 skill，做 counterfactual localization；
7. benchmark/spec 自身也版本化，明确区分 **agent regression**、**environment drift** 和 **oracle drift**。

## 6. 明确排除的高混淆结果

| 论文/方向 | 排除理由 |
|---|---|
| Testora、RippleGUItester、MuMuTestUp、WebTestPilot、WebCQ | agent/LLM 是 tester 或生成器，SUT 是普通程序、GUI 或测试代码。 |
| Evaluation of the Choice of LLM in a Multi-Agent Solution for GUI-Test Generation（ICST 2025） | 虽比较 multi-agent tester 内的模型选择，但系统目标仍是 GUI test generation；不满足“直接测试 agent 产品”的用户边界。 |
| How well LLM-based test generation techniques perform with newer LLM versions?（ICST 2026） | 测的是 LLM test-generation technique 的版本效果，不是 agentic system。 |
| Regression Accumulation in Multi-Turn LLM Programming Conversations（ASE 2026） | 方法有价值，但 SUT 是多轮代码生成对话，故只作邻近基线，不进入严格 agent 核心集。 |
| FAMAS、REFLECT、Causal Agent Replay | replay 主要用于 failure attribution；如果没有版本 baseline 与 regression verdict，不应直接标为 regression testing。 |

## 7. 推荐阅读顺序

1. **Chronicle**：最纯粹的“把历史事故变成 CI 回归测试”。
2. **AgentLens**：最接近生产 nightly agent regression pipeline。
3. **Layer-Isolated Evaluation**：最适合学习便宜、确定、可定位的 per-PR gate。
4. **TDAD**：最系统地处理需求/规格演化中的旧行为保持。
5. **Regression Tax**：最重要的指标思想——不要只报 net average，要报 task-level gains 与 regressions。
6. **Tangent**：用顶会证据说明现实实践与研究缺口。
7. **Continuous Benchmark Generation**：理解 benchmark 本身如何随需求演化。

## 证据与核验说明

- 上述 Chronicle、AgentLens、Layer-Isolated、TDAD、Regression Tax、Continuous Benchmark Generation、EDDOps 与 ASE Regression Accumulation 均下载并检查了开放全文；Tangent 也已检查 arXiv 全文。
- S2 引用数是 2026-09-19 快照：Tangent 1、ASE Regression Accumulation 2、AgentLens 2、Layer-Isolated 0、TDAD 6、Regression Tax 0、Continuous Benchmark Generation 3、EDDOps 10；Chronicle 发布仅两天，S2 尚未收录。
- ASE 2026 与 ISSTA 2026 在检索日尚未举行；program/元数据可能继续更新。Tangent 的 DOI 在 S2 与既有会议记录中出现，但 Crossref/OpenAlex 当日 404，因此不把它标成完全核验。
- 结构化会议检索的 DBLP 与 arXiv 子源分别出现 JSON 解析失败和 HTTP 406；已使用官方会议 program、Crossref、OpenAlex、Semantic Scholar 与 arXiv 页面/全文交叉补偿，未把源失败误作“论文不存在”。
