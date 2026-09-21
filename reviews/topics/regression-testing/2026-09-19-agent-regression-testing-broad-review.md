# Agent 回归测试、持续评测与行为漂移：2023–2026 广泛检索

检索日期：2026-09-19（Asia/Shanghai）

## 1. 范围与判定标准

本轮只纳入**被测对象是 LLM agent / agentic system** 的工作。所谓回归问题至少涉及以下一项：

1. 在 model、prompt、tool、agent harness 或业务规则升级前后比较同一组 agent 行为；
2. 把固定测试集接入 nightly / CI/CD / continuous evaluation；
3. 用重复执行区分真实退化与随机 flakiness；
4. 对轨迹、工具调用、状态副作用、成本或时延做差分；
5. 控制外部 API/环境漂移，使跨版本结果可比；
6. 以行为 contract、时序断言或统计门限作为 release gate。

排除项：用 agent 生成或执行普通软件回归测试、agent-as-tester、只评测单轮 LLM 输出、以及没有测试 agent 本身的工作。

结论先行：**“agent regression testing” 已经出现了几篇直接命名和落地的工作，但截至 2026-09，大部分仍是预印本或系统论文。真正经过主流会议同行评审、又把跨版本回归当核心问题的研究仍很少。** 当前最直接的五项证据是 Sheffler 的时序断言、AgentEval、AgentLens、Agent Harness Evolution 纵向研究，以及 Agent Behavioral Contracts；其余工作主要解决随机性、环境漂移和 oracle 三个前置难题。

证据等级：`全文` = 已检查论文正文；`摘要` = 只用官方摘要支撑高层描述；`元数据` = 只用于题名、作者、venue 和版本状态。引用数为 Semantic Scholar 在检索日的快照，不作为质量分数。

## 2. 最直接的论文与系统

| 论文 / 系统 | 年份与版本 | 是否正式发表 | 核心方法 | 主要回归维度 | 证据 / 引用 |
|---|---|---|---|---|---|
| [An Approach to Checking Correctness for Agentic Systems](https://arxiv.org/abs/2509.20364) — Thomas J. Sheffler | 2025，arXiv:2509.20364 | 未发现正式版本；预印本 | 把 agent tool call、agent handoff、state transition 编译成事件流；用类似硬件 PSL 的 temporal expressions 检查动作顺序，而非脆弱的文本匹配 | **模型替换、prompt/logic 修改后的行为回归**；tool sequencing、handoff protocol、禁止/必需事件 | 全文；S2 引用 4 |
| [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](https://arxiv.org/abs/2604.23581) | 2026，arXiv:2604.23581 | DBLP 标为 CoRR；OpenReview 稿，未核实正式录用 | 把运行轨迹建成 evaluation DAG；节点上放类型化指标和 calibrated LLM judge；沿依赖边归因传播；用 paired bootstrap + 历史 `2σ` 双门限报警，并接入 GitHub Actions | **model/prompt/tool/config 版本差分**；step-quality、failure detection、root cause、CI/CD gate | 全文；S2 引用 6；代码：[bettyguo/AgentEval](https://github.com/bettyguo/AgentEval) |
| [AgentLens: Production-Assessed Trajectory Reviews for Coding Agent Evaluation](https://arxiv.org/abs/2607.06624) | 2026，arXiv:2607.06624 | 未发现正式版本；预印本 | 结合 formal verifier、五维 LLM trajectory review、确定性 telemetry 和同任务 side-by-side review；nightly/weekly 当前版对 anchor run | **产品版本回归**；end result、instruction compliance、pitfalls、tool use、交互质量、成本/时延、异常终止 | 全文；S2 引用 2；[项目与代码](https://agent-lens.github.io/agent-lens-bench/) |
| [Don't Blame the Large Language Model: How Agent Harness Evolution Shapes Coding Agent Quality](https://arxiv.org/abs/2607.03691) | 2026，arXiv:2607.03691v2；当前题名中的术语已由 v1 的 *scaffolding* 改为 *agent harness* | PDF 标注 “Manuscript submitted to ACM”；未核实正式录用 | 固定 underlying LLM，逐版运行 35 个 Qwen Code CLI release；每版 50 个 SWE-bench Verified 任务、每任务两次；将质量波动关联到 release change 和 harness architecture component | **harness 升级兼容性与非功能回归**；resolve rate、token、tool-call overhead、跨次一致性 | 全文；S2 引用 2 |
| [Agent Behavioral Contracts: Formal Specification and Runtime Enforcement for Reliable Autonomous AI Agents](https://arxiv.org/abs/2602.22302) / AgentAssert | 2026，arXiv:2602.22302 | 未发现正式版本；预印本 | Design-by-Contract 式 `C=(P,I,G,R)`：precondition、invariant、governance、recovery；定义概率 contract satisfaction 和 drift bound；运行时逐 action 检查 | **behavioral drift、policy regression、跨 run contract violation**；可作为升级前后的不变量 gate | 摘要 + 正文片段；需谨慎看待单团队理论假设与 benchmark 外部效度；[项目](https://agentassert.com/) |
| [Agent Gym: A Framework for Continuous Evaluation and Evolution of LLM Agents Through Human-in-the-Loop Feedback](https://arxiv.org/abs/2608.15591) | 2026，arXiv:2608.15591 | 未发现正式版本；预印本 | Act–Evaluate–Investigate–Correct–Learn–Observe 六模块；constitution artifacts、deterministic+LLM correction、SME 审批的 rule learning | **业务规则演化后的持续合规测试**；rule hit、correction outcome、spec-to-note gap | 全文；S2 引用 0；目前主要是 invoice-processing reference implementation，跨域和多版本趋势仪表盘仍属 future work |

### 对直接工作最值得注意的细节

- **Sheffler 2025 是最“像传统回归测试”的最小方案。** 同一三 agent 系统在强模型配置下运行 10 次均满足时序断言；将两个子 agent 换成小模型后，10 次中仅 7 次正确完成 handoff，断言抓到 tool 顺序与 coordination 错误。弱点是样例只有一个三 agent demo、两个配置、20 次执行，远不足以证明通用性。
- **AgentEval 是最完整的 CI/CD 方案。** 测试用 JSON 描述 expected DAG 和 tolerance；每次运行携带 model/prompt/tool 版本；paired bootstrap (`p<0.05`) 与历史 `2σ` 同时越界才报警；10-case smoke test 先 gate 100+ case full suite。论文报告 6 个模拟更新场景中 precision 88%、recall 94%，四个月试点产生 23 个告警，经团队分诊为 8 genuine、12 borderline、3 false positive。主要局限是核心生产数据来自单一组织、judge 依赖 GPT-4o、对非 DAG/高度动态多 agent 架构适用性降低。
- **AgentLens 已真正用于 nightly regression。** 候选版本与 anchor run 做同场景 side-by-side trajectory review，显著下降触发通知。它还专门测了 flakiness：同一 GLM-5.1 配置重复五次，质量指数均值 67.28、标准差约 0.9；32 个场景中 16 个 formal verification 结果在五次间波动。局限是当前公开 fold 仅 16 个 Java 场景 × 2 persona，且接近模型之间有明显 judge self-family preference。
- **Agent Harness Evolution 说明“为何必须做回归”。** 35 个 Qwen Code release × 50 任务 × 2 次 = 3,500 runs，在固定模型下没有显著的 resolve-rate 单调进步，后期版本却几乎消耗两倍计算 token/tool calls；作者把风险集中到 LLM provider 与 context management 等架构层。这是纵向实证研究，不是现成 regression framework。
- **Agent Gym 是 continuous correction，不等同成熟的版本回归系统。** 论文明确把 multi-run trend dashboard 和 CI/CD spec-to-note release gate 放在未来工作中；现阶段更适合视为“持续评测架构原型”。

## 3. 回归测试的关键基础论文

这些论文不一定直接叫 regression testing，但它们解决了 release gate 必须面对的统计、环境或 oracle 问题。

| 论文 | 正式版本 | 对回归测试的贡献 | 适合测的维度 | 证据 / 引用 |
|---|---|---|---|---|
| [Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666) | **ICML 2026，PMLR 306** | 给出 12 个指标，将 reliability 分成 consistency、robustness、predictability、safety；论文明确建议把这些维度的统计回归测试接入部署流水线 | outcome/trajectory/resource consistency，prompt/environment perturbation，calibration、failure severity | 全文；S2 引用 54 |
| [τ-bench](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b126cc38b8638e07bef37e7b2bb72bf-Abstract-Conference.html) | **ICLR 2025**；arXiv:2406.12045 | 引入 `pass^k`：同一任务连续 k 次都成功，直接暴露单次 pass 掩盖的 flaky 行为；以数据库 end-state 作可执行 oracle | 重复执行可靠性、policy compliance、状态副作用 | 全文；S2 对 arXiv 记录引用 1,172 |
| [ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions](https://arxiv.org/abs/2601.06112) | 预印本 | 统一可靠性曲面 `R(k, ε, λ)`：重复执行、语义等价输入扰动、tool/API fault injection；用 action metamorphic relation 比 end-state 等价而非文本 | flakiness、metamorphic regression、tool fault tolerance | 全文；S2 引用 30 |
| [Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents](https://arxiv.org/abs/2603.29231) | 预印本 | 以任务时长分层，引入 Reliability Decay Curve、Variance Amplification Factor、Graceful Degradation Score、Meltdown Onset Point | 长轨迹版本退化、meltdown rate、方差随 horizon 放大 | 全文；S2 引用 6 |
| [How Consistent Are LLM Agents? Measuring Behavioral Reproducibility in Multi-Step Tool-Calling Pipelines](https://arxiv.org/abs/2605.28840) | 预印本 | 对相同输入的多次 typed tool call trace 定义 Tool Sequence Similarity 与 Argument Consistency；1,140 traces 显示结构通常稳定、参数仍漂移 | tool sequence、tool arguments、first-divergence；区分结构性 regression 与随机参数差异 | 全文；S2 引用 4 |
| [When Agents Disagree With Themselves](https://arxiv.org/abs/2602.11619) | 预印本 | 3,000 个 ReAct runs；相同任务的 action-sequence 分歧可预测失败，69% divergence 从第 2 步首次搜索开始 | repeated-run path diversity、early-divergence alert | 全文；S2 引用 1 |
| [StableToolBench](https://aclanthology.org/2024.findings-acl.664/) | **Findings of ACL 2024**，DOI `10.18653/v1/2024.findings-acl.664` | 以 cache + API simulator 减少 RapidAPI 状态变化；提出更稳定的 solvable pass/win rate | **测试环境漂移控制**；避免把第三方 API 坏了误判成 agent regression | 全文；S2 引用 139 |
| [AI Agents That Matter](https://openreview.net/forum?id=Zy4uFzMviZ) | **TMLR 2025**；arXiv:2407.01502 | 强调成本控制、holdout、重复试验和标准化；证明只比 accuracy 会奖励昂贵 agent，也会混淆 agent/framework/model 的贡献 | accuracy–cost regression、overfitting、统计不确定性 | 全文；S2 引用 205 |
| [Agentic CLEAR](https://aclanthology.org/2026.acl-demo.74/) | **ACL 2026 System Demonstrations**，DOI `10.18653/v1/2026.acl-demo.74` | 在 observability traces 上做 system–trace–node 三层 LLM evaluation，并跨轨迹聚类 recurrent issues；可作为 regression triage 层 | node/trace quality、recurrent failure clusters、task-success prediction | 全文；S2 当前记录未单独批查；正式元数据已由 ACL 核验 |
| [Beyond Pass@k: Measuring Reliability and Security of Agentic Code Generation](https://arxiv.org/abs/2608.14711) | 预印本 | 指出把 unit-test 数误当独立 rollout 数会虚高 pass@k；提出按独立运行计算 `reliability@k` 与 security-adjusted 版本 | coding-agent repeated-run reliability、regression introduction rate、安全回归 | 全文；S2 引用 1；主要结果来自合成数据，真实 SWE-bench pilot 仅 5 tasks/1 agent/1 run，证据很弱 |
| [Beyond Pass@1: K-Sample Behavioral Equivalence for Code-Agent Evaluation](https://openreview.net/forum?id=qblhwh1eDn) | ACM CAIS 2026 RLEval workshop | 同一问题采样 K 次，用测试行为签名聚类，再以 conformal risk control 选择 abstention threshold；能暴露“稳定地错” | stochastic regression、behavioral concentration、silent failure | 全文片段；workshop；单个 1.5B model + HumanEval+，外推性有限 |

## 4. 方法维度：如何把它们拼成真正的 Agent 回归流水线

| 层 | 推荐证据 | 回归测试产物 |
|---|---|---|
| 环境冻结 | StableToolBench；τ-bench | versioned DB snapshot、tool schema、API simulator/cache、时间与身份固定 |
| 测试输入 | τ-bench；ReliabilityBench；AI Agents That Matter | 固定 holdout + 语义等价变体 + 失败注入；任务集本身也版本化 |
| 重复协议 | `pass^k`；ReliabilityBench；两篇 consistency work | 同任务多 seed/多次运行；估计 task-level flakiness 而非只看总体均值 |
| 行为 oracle | Sheffler temporal assertions；Agent Behavioral Contracts | 必须/禁止事件、偏序、handoff contract、权限与副作用 invariant |
| 轨迹差分 | AgentLens；AgentEval；Agentic CLEAR | first divergence、node score delta、failure propagation、side-by-side evidence |
| 非功能回归 | Agent Harness Evolution；AI Agents That Matter | tokens、cost、latency、tool calls、timeout/abort、recovery burden |
| 统计 release gate | AgentEval；Towards a Science of AI Agent Reliability | paired task deltas、bootstrap CI、multiple-run hierarchical estimates、severity-aware threshold |

最重要的设计原则是：**不要把“当前版成功率低于上一版”直接叫 regression。** 至少要同时控制 task、environment、model/harness/tool/judge 版本，并用 paired repeated runs 估计随机波动；否则可能只是 agent flakiness、外部 API 漂移或 judge 漂移。

## 5. 研究空白

1. **版本差分缺少因果隔离。** Agent Harness Evolution 固定模型只改变 harness，是少数真正隔离变量的研究；多数 benchmark 同时换 model、prompt、tool 和 provider，无法定位回归来源。
2. **没有统一的 agent regression coverage。** 现有覆盖零散分布在 task、tool、trajectory 和 fault injection。尚缺 `任务 × 状态 × tool × 权限 × failure × recovery` 的组合覆盖标准。
3. **随机性门限仍不成熟。** 多数论文用 5–10 次重复；AgentEval 虽引入 bootstrap，仍缺统一的 task-level hierarchical model、最小可检测退化和多重比较修正。
4. **judge 也会回归。** AgentLens 已观察到 model-family self-preference；当 evaluator model 更新时，分数变化可能来自 judge，而不是被测 agent。需要冻结 judge、gold anchor 和 judge-version diff。
5. **环境与数据漂移没有和产品回归清晰分离。** StableToolBench 主要处理 API availability，不处理真实动态业务环境中 policy/data/schema 的合理演化。
6. **跨版本轨迹“等价”定义不成熟。** 完全相同的 tool sequence 未必必要；真正需要的是 partial-order、end-state、副作用与资源预算上的语义等价。
7. **生产证据弱。** AgentEval 与 AgentLens 提供了少量生产/夜间流水线证据，但 AgentEval 是单组织数据，AgentLens 的公开 fold 很小；独立复制几乎不存在。

## 6. 值得继续做的具体题目

### 题目 A：Version-Paired Agent Regression Testing（优先）

对相同环境快照、相同任务和相同随机种子，成对运行 `old` 与 `new` agent。先用 temporal/contract oracle 检查硬约束，再用 trajectory alignment 找 first semantic divergence；最终输出 outcome、side effect、resource、recovery 四类 delta，并用 task-level paired bootstrap / hierarchical model 决定是否 gate release。

与现有工作的区别：AgentLens 有 side-by-side review 但没有明确的语义轨迹对齐；AgentEval 有 DAG 与统计报警但主要依赖 LLM node score；这里可以把**可执行 contract + 对齐差分 + 统计门限**结合起来。

### 题目 B：Regression Test Selection for Agents

维护 task-to-component 依赖图：prompt 段、tool schema、memory policy、planner、executor、permission rule 分别影响哪些 regression cases。升级时只选择可能受影响的 case，再用历史 flakiness 和风险加权。这直接回应 AgentEval/AgentLens 全量运行成本高的问题。

### 题目 C：Judge-Aware Regression Testing

同时维护 agent version 和 judge version 两条轴：`old-agent/old-judge`、`new-agent/old-judge`、`old-agent/new-judge`、`new-agent/new-judge` 四格实验，用 difference-in-differences 分离 agent regression 与 evaluator drift。

## 7. 可复现检索记录

### 数据源

- arXiv 官方摘要/PDF与版本历史；
- Semantic Scholar Graph API（一次 batch 查询元数据和 citationCount）；
- Crossref + OpenAlex（`verify_metadata.py`；预印本通常只由 OpenAlex 精确命中，Crossref 常返回相似题名，故不能把 arXiv DataCite DOI 当正式出版 DOI）；
- DBLP（AgentEval 被标为 CoRR）；
- ACL Anthology（StableToolBench、Agentic CLEAR 的正式元数据）；
- ICLR Proceedings（τ-bench 正式版本）；
- PMLR PDF（Towards a Science of AI Agent Reliability 的 ICML 2026 正式版本）；
- OpenReview/TMLR（AI Agents That Matter）；
- 论文官方项目/GitHub。

### 实际查询词

1. `"LLM agent" regression testing versions drift evaluation`
2. `"agentic system" "regression testing" LLM`
3. `"LLM agents" flakiness stability repeated runs evaluation`
4. `"coding agents" regression evaluation trajectories production`
5. `site:arxiv.org "agentic regression testing"`
6. `site:arxiv.org "behavioral regression" "LLM agent"`
7. `site:arxiv.org "version drift" agents evaluation`
8. `site:arxiv.org agent flakiness repeated runs tool agent`
9. `site:arxiv.org/abs "regression" "agentic systems"`
10. `site:arxiv.org/abs "continuous evaluation" "LLM agents"`
11. `site:arxiv.org/abs "differential testing" "LLM agents"`
12. `site:arxiv.org/abs "model upgrade" "LLM agents" evaluation`
13. `site:arxiv.org/abs agent benchmark "pass^k" consistency`
14. `site:arxiv.org/abs "agent reliability" consistency perturbation fault tolerance`
15. `site:arxiv.org/abs "agents" "behavioral consistency" repeated`
16. `site:arxiv.org/abs "agent evaluation" "CI/CD" regression`
17. 精确题名/ID 查询：`2509.20364`、`2604.23581`、`2607.03691`、`2607.06624`、`2608.15591`、`2601.06112`、`2603.29231`、`2602.16666`、`2605.28840`、`2602.11619`、`2403.07714`、`2406.12045`、`2407.01502`、`2608.14711`、`2602.22302`。

### 排除示例

- *ExploreAI: ... Observable-Regression Testing of Black-Box VR and 3D Applications*：agent 用来测试 VR/3D 软件，属于 agent-as-tester。
- *Human-AI Collaboration for Scaling Agile Regression Testing*：agent 生成普通系统回归脚本，被测对象不是 agent。
- *CodeARC*：虽然使用 differential oracle，但研究目标是 agent 完成 inductive program synthesis 的能力，不是 agent 版本回归。
- 通用 LLM 输出回归与 prompt regression 工具：若没有多步 tool/state/trajectory，被排除出核心表。

## 8. 核验说明

- 正式发表：StableToolBench、τ-bench、AI Agents That Matter、Towards a Science of AI Agent Reliability、Agentic CLEAR 已从官方 proceedings/Anthology/PMLR/OpenReview 核验。
- 预印本：Sheffler、AgentEval、AgentLens、Agent Harness Evolution、Agent Gym、ReliabilityBench、Beyond pass@1、两篇 consistency 论文、Beyond Pass@k、Agent Behavioral Contracts 均未找到可靠的正式出版记录；arXiv/Datacite DOI 不等同于会议或期刊 DOI。
- 版本冲突：`2607.03691` v1 搜索索引常显示 *Scaffolding Evolution*，当前 v2 官方题名为 *Agent Harness Evolution*；引用时应采用 v2 题名。
- `τ-bench` 的预印本年份为 2024，正式版本是 ICLR 2025；本报告按正式版本标 2025。

