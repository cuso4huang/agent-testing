# 从综述到原始论文：智能体测试与测评证据地图

> 检索截止：2026-08-13。本报告全文阅读核心综述后，抽取与“智能体测试和测评”直接相关的论点，再追踪到原始 benchmark、测试方法和评测器论文。综述用于建立地图；有关方法、实验结果和局限性的判断优先来自原始论文全文。

## 1. 本轮全文阅读范围

| 综述 | 阅读状态 | 重点阅读内容 |
|---|---|---|
| Yehudai et al., *A Survey on Evaluation of LLM-based Agents*, Findings ACL 2026 | 全文 25 页 | benchmark 构造、静态/动态环境、接口与 metric；评测框架；stepwise/trajectory；趋势和研究空白 |
| Mohammadi et al., *Evaluation and Benchmarking of LLM Agents: A Survey*, KDD 2025 | 全文 11 页 | evaluation objective/process 二维分类；任务、能力、可靠性、安全、交互模式、metric 计算和企业评测 |
| Zhu et al., *Evolutionary Perspectives on the Evaluation of LLM-Based AI Agents*, FCS 2026 | 全文 30 页 | chatbot→agent 的评测演化；环境、agent、evaluator、metric 四视角；各应用 benchmark 表格 |
| Ling et al., *Toward Secure LLM Agents*, arXiv:2606.10749 | 全文 42 页 | 系统检索与编码方法；247 篇安全语料；benchmark 重用、metric 分布和部署保障缺口 |
| Kim et al., *The Attack and Defense Landscape of Agentic AI*, USENIX Security 2026 | 本地正式稿全文 | agent 设计空间、攻击面、防御层与安全测试边界 |

没有把综述中的引用自动当作事实。对下列代表性原始论文，已利用本地全文及结构化笔记复核：AgentBoard、ToolSandbox、AgentRewardBench、τ-bench、AppWorld、AgentDojo、AI Agents That Matter、WebArena、OSWorld、SWE-bench、ToolEmu、AgentHarm、MultiAgentBench 等。

## 2. 综述共同指出的核心问题

### 2.1 任务成功率只是底线

ACL 综述把 task completion 视为最普遍的 metric，但指出其实现依任务而异：代码 agent 用执行测试，改变环境的 agent 用状态匹配，短答案任务用 answer match。二元结果无法说明中间进度和失败原因。

KDD 综述进一步把 agent behavior、capability、reliability、safety 分开，说明单个 success rate 不能表达重复一致性、扰动鲁棒性、政策合规和成本。

对应原始论文：

| 原始工作 | 可借鉴内容 | 开源 |
|---|---|---|
| [SWE-bench](https://github.com/SWE-bench/SWE-bench) | 用 fail-to-pass 与 pass-to-pass 测试检查补丁是否修复问题且不破坏旧功能，是代码 agent 的执行型 oracle。 | benchmark、Docker/环境和 evaluator 开源 |
| [AppWorld](https://github.com/stonybrooknlp/appworld) | 比较 `expected changes` 与 `allowed changes`，把未允许的数据库差分视为 collateral damage；contrast-set 测相近场景稳定性。 | Engine、任务、验证器和环境开源 |
| [τ-bench](https://github.com/sierra-research/tau-bench) | 同时检查数据库终态和必须返回给用户的信息；提出 `pass^k` 测连续多次全部成功。 | 任务、政策、工具、数据库和用户模拟器开源 |
| [WebArena](https://github.com/web-arena-x/webarena) | 在自托管网站中执行任务，以 URL、页面内容和后台状态等任务特定 evaluator 判断成功。 | 网站环境、任务和 evaluator 开源 |

### 2.2 测试对象必须包括完整轨迹

ACL 综述把工程评测分成：final-response、stepwise、trajectory-based 三层。轨迹评测又分为：

- reference-based：精确、部分、无序或子集匹配预期动作；可复现，但可能拒绝合法替代路径；
- reference-free：用 LLM judge 判断连贯、效率和目标导向；灵活，但可靠性较低；
- graph-based：检查预期节点和转移，而不是要求一条扁平且唯一的工具序列。

对应原始论文：

| 原始工作 | 方法 | 主要价值与边界 | 开源 |
|---|---|---|---|
| [AgentBoard](https://github.com/hkust-nlp/AgentBoard) | 人工定义子目标，计算 Progress Rate | 能定位长链任务在哪一阶段停滞；不是副作用或安全 oracle。 | 是 |
| [ToolSandbox](https://github.com/apple/ToolSandbox) | milestone DAG + minefield DAG + 每步世界状态快照 | 允许多条等价正确路径，同时检查必要前置条件和禁止状态，是较强的轨迹 oracle 模板。 | 是 |
| [AgentRewardBench](https://github.com/McGill-NLP/agent-reward-bench) | 用专家标注轨迹元评估规则和 LLM judge | 证明规则通常精确但召回不足，LLM judge 容易相信 agent 自述；评测器本身必须回归测试。 | 是 |
| [Agent-as-a-Judge](https://github.com/metauto-ai/agent-as-a-judge) | evaluator agent 主动检查工作区及层级需求 | 比一次性文本 judge 更能收集证据，但 evaluator 自己也会规划或记忆失败。 | 是 |

### 2.3 可靠性需要重复、扰动和故障注入

KDD 综述明确区分：

- consistency：同一任务反复运行是否稳定；
- robustness：输入释义、错别字、无关上下文、页面变化或环境变化下是否仍成功；
- adaptive resilience：API 错误、null、异常输出后能否恢复。

对应原始论文：

| 原始工作 | 测什么 | 建议采用的指标/做法 | 开源 |
|---|---|---|---|
| [τ-bench](https://github.com/sierra-research/tau-bench) | 重复一致性 | success rate + `pass^k` + 多次独立执行；不要只报 pass@k。 | 是 |
| [OSWorld](https://github.com/xlang-ai/OSWorld) | GUI/桌面 agent 对窗口、布局和真实 OS 状态的鲁棒性 | 任务成功、动作轨迹、环境初始化/重置和扰动对比。 | 是 |
| [BrowserGym](https://github.com/ServiceNow/BrowserGym) | 跨 Web benchmark 与 harness 的统一执行 | 锁定浏览器、时区、语言、地理位置、网站和 agent harness 版本。 | 是 |
| [ToolEmu](https://github.com/ryoungj/ToolEmu) | 风险环境和工具失败模拟 | 在低成本模拟中注入异常，再对高风险失败做人工或真实环境确认。 | 是 |
| [AI Agents That Matter](https://github.com/benediktstroebl/agent-evals) | benchmark 方法学、成本、holdout 与复现 | 报告成本—准确率 Pareto、简单基线、独立 holdout、重复运行和精确模型/脚手架版本。 | 是 |

### 2.4 安全测试必须同时测效用

安全 SoK 对 247 篇文献的编码显示：Attack Success Rate 的使用远多于 utility、latency 和 cost。它据此指出安全评测往往更像漏洞发现，而不是部署保障。一个拒绝所有任务的 agent 会得到低 ASR，却没有实际效用。

对应原始论文：

| 原始工作 | 测试模型 | 应联合报告 | 开源 |
|---|---|---|---|
| [AgentDojo](https://github.com/ethz-spylab/agentdojo) | 正常用户任务 + 间接提示注入 + 工具环境 | utility、security/ASR、攻击者目标是否达成；以环境状态而非文本风格作 oracle。 | MIT 开源 |
| [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) | 工具输出中的间接 prompt injection | 攻击成功与正常工具任务性能；需明确攻击面、工具权限和攻击位置。 | 是 |
| [Agent Security Bench](https://github.com/agiresearch/ASB) | 多攻击、多防御的统一 agent 安全 benchmark | ASR、正常效用、防御效果和不同威胁类别。 | 是 |
| [AgentHarm](https://github.com/centerforaisafety/agentharm) | 多步有害工具任务与 jailbreak | 实际有害任务完成、拒绝/正常效用和 jailbreak transfer，而非只判文本有害。 | 是 |
| [SafeAgentBench](https://github.com/shengyin1224/SafeAgentBench) | 具身 agent 的危险/安全任务规划 | 任务成功与安全违规分开；文本拒绝不能替代动作安全。 | 项目资源公开；版本需锁定 |

### 2.5 评测器也必须被测试

ACL 综述认为 reference-based 精确但难覆盖多条合法路径，reference-free 灵活但可靠性较弱。它还指出当前平台很难对大量轨迹做根因分析，且昂贵 judge 带来的评测成本经常没有被计入。

可直接形成以下 evaluator 测试方案：

```text
专家标注 golden trajectories
  ├─ 成功但路径不同
  ├─ 看似合理但未真正执行
  ├─ 终态正确但过程违规
  ├─ 局部成功但最终失败
  ├─ 重复/循环/超预算
  └─ 环境或工具故障，不应归咎 agent

对每个 evaluator 报告：precision、recall、F1、分类型错误、成本、延迟、重复一致性。
```

首选原始证据是 AgentRewardBench；如果工作区可供 evaluator 主动检查，再参考 Agent-as-a-Judge。能程序化判定的状态、权限和副作用不应首先交给 LLM judge。

### 2.6 应分离模型能力和 agent harness

ACL 综述明确指出多数 benchmark 混淆了 backbone LLM 与 harness/scaffold 的贡献。模型、系统提示、历史压缩、planner、memory、tool schema、重试策略和环境版本共同决定结果。

对应方法与资源：

- [BrowserGym/AgentLab](https://github.com/ServiceNow/BrowserGym)：统一 Web agent 的 observation/action 接口与实验管理；
- [Harbor](https://github.com/laude-institute/harbor)：统一 agent harness/环境执行的近期方向，引用时需核验所用版本；
- AI Agents That Matter：要求报告 agent + model + benchmark 的完整组合，而不是只按模型名归因；
- AgentRewardBench：不同 agent family 会改变 evaluator 的错误分布。

推荐使用受控因子实验：固定任务和环境，一次只替换 model、prompt、planner、memory 或 tool layer；报告交互效应，不把所有提升归因于模型。

## 3. 按“测试方法”重新组织的原始论文清单

| 测试方法 | 代表论文/资源 | 适用范围 | 成熟度判断 |
|---|---|---|---|
| 环境化系统测试 | WebArena、OSWorld、AppWorld、SWE-bench、τ-bench | Web、OS、跨应用、代码、企业工作流 | 主流；生产验收基础 |
| 状态差分与副作用 oracle | AppWorld、τ-bench、AgentDojo | 有可查询终态/数据库的工具 agent | 证据较强 |
| 轨迹里程碑/禁止事件 | AgentBoard、ToolSandbox | 长任务、工具调用、过程合规 | 快速成为主流 |
| evaluator 元测试 | AgentRewardBench、Agent-as-a-Judge | Web/code agent 的自动评分 | 必需但仍不成熟 |
| 重复与统计可靠性 | τ-bench、AI Agents That Matter | 所有概率 agent | 应成为默认做法 |
| 扰动与变形测试 | OSWorld、BrowserGym；通用做法仍分散 | GUI/Web、输入和环境变化 | 缺统一 metamorphic relation |
| 模拟与故障注入 | ToolEmu、ToolSandbox | 工具异常、危险长尾 | 有用，但需真实复现率 |
| 自动测试生成 | PDoctor、ATA | 规划约束、对话 agent | 新兴；受 oracle 质量约束 |
| 灰盒/覆盖引导 fuzzing | AgentDoS、VeriGrey、FLARE | 资源、工具序列、多智能体行为 | 2026 前沿；覆盖语义未标准化 |
| 自适应安全红队 | AgentDojo Adaptive Attacks、SIRAJ、MUZZLE | 间接注入、黑盒/网页 agent | 比固定攻击模板更可信 |
| 运行时策略验证 | AgentSpec、MATE、NEXUS | 生产动作阻断和轨迹审计 | 新兴；需测误阻断和延迟 |

## 4. 综述没有充分覆盖、但与你主题高度相关的新增论文

综述存在天然时间滞后。依据 2026 年新增原始论文，应补入：

1. **ATA — Agent-Testing Agent（EACL 2026）**：结合代码分析、开发者询问、文献证据和 persona 生成，依据 judge 反馈提升测试难度。适合“自动测试生成”。
2. **SIRAJ（Findings EACL 2026）**：从 agent 定义产生风险种子，并用前次攻击轨迹迭代改进；适合“自适应红队”。
3. **AgentDoS（USENIX Security 2026）**：将资源生命周期作为灰盒反馈，定向发现资源耗尽；适合“非功能/DoS 测试”。
4. **VeriGrey（arXiv:2603.17639）**：把工具调用序列作为反馈函数；适合“行为覆盖引导 fuzzing”。
5. **FLARE（arXiv:2604.05289）**：抽取多智能体规格及主体内/主体间行为空间；适合“多智能体覆盖测试”。
6. **LogicHunter（arXiv:2607.06195）**：规格感知输入生成 + 主动查文档、源码和状态的 agentic oracle；适合“agent framework 测试”。

这些工作中的预印本应标记为前沿证据，不能与已同行评审的方法等权引用。

## 5. 可直接采用的智能体测试框架

综合综述与原始论文，建议把一个测试用例表示为：

```text
TestCase = {
  goal,
  initial_state,
  policy_and_permissions,
  tools_and_schemas,
  user_or_peer_behavior,
  perturbation_or_attack,
  execution_budget,
  required_milestones,
  forbidden_events,
  expected_changes,
  allowed_changes
}
```

每次执行至少保存：

- agent/model/harness/evaluator 的精确版本；
- 初态和终态快照；
- 完整 observation/action/tool trace；
- 工具副作用和错误；
- 成功、progress、违规、恢复、成本和延迟；
- 多次运行的分布、置信区间和失败簇。

推荐的 oracle 优先级：

1. 确定性环境状态与单元测试；
2. 权限、顺序、里程碑和禁止事件断言；
3. 规则/程序无法覆盖的局部语义 judge；
4. 人工抽检与 evaluator golden-set 回归。

## 6. 最值得作为研究选题的空白

1. **跨 benchmark 的统一轨迹语义**：目前 tool sequence、DAG、subgoal 和 span 各自为政。
2. **agent 测试覆盖率**：代码覆盖不等于语义/状态/风险覆盖；VeriGrey、FLARE 只是早期方案。
3. **变形测试**：缺少经过验证的释义、实体重命名、可交换工具顺序、环境布局和权限变化关系。
4. **长期状态测试**：跨 session 记忆污染、权限变化、延迟触发和资源泄漏仍覆盖不足。
5. **evaluator 独立性**：生成测试、被测 agent 和 judge 使用同一家族模型会产生相关偏差。
6. **安全—效用—成本联合指标**：安全 SoK 显示 latency/cost 报告尤其稀缺。
7. **故障归因**：需要区分模型错误、harness 错误、工具错误、环境漂移和 evaluator 错误。
8. **失败归约与回归**：把长轨迹事故自动缩减为可稳定重放的最小测试仍缺成熟方法。

## 7. 证据限制

- 已全文阅读的综述可以支持其分类、检索方法和作者结论，但原始论文的具体数字不由综述二手引用支撑。
- 本报告对代表性原始论文采用本地全文/结构化笔记复核；对 Harbor、MUZZLE、MATE 等近期资源只作方向定位，不在此使用详细实验结论。
- 不同论文中的 success rate、ASR、utility 和 cost 定义不同，不能直接拼成排行榜。
- GitHub 开源不保证复现：闭源模型快照、网站/API 漂移、许可证和环境镜像仍会限制数值级复现。
