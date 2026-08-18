# Agent 测试方法与故障诊断增量调研：全文证据更新

## 1. 范围与检索策略

- 检索日期：2026-08-14；时间范围：2024–2026。
- 研究边界：直接测试 Agent、Agent 轨迹、harness 或多智能体基础设施的方法；排除“使用 Agent 测普通软件”、普通 LLM 故障诊断和没有测试方法贡献的能力榜单。
- 数据源：`conference_search.py` 汇合 Semantic Scholar、OpenAlex、Crossref、arXiv、DBLP 与开放获取解析；正式身份进一步用 Crossref/OpenAlex 和论文首页复核。
- 六个精确英文查询：
  1. `LLM agent fault injection chaos engineering reliability testing`
  2. `LLM agent coverage guided greybox fuzzing metamorphic testing`
  3. `AI agent test oracle state validation trajectory evaluation`
  4. `LLM multi agent failure localization attribution root cause diagnosis`
  5. `LLM agent runtime monitoring telemetry observability fault detection`
  6. `LLM multi agent cascading failure recovery testing fault propagation`
- 每组最多返回 100 条且不限定会议，共得到 600 条原始记录。跨查询合并并扣除原 85 条证据记录后有 502 个题名候选；人工筛选排除了大量传统系统 fuzzing、微服务诊断和“Agent 作为测试生成器”的论文。
- 数据源异常：Semantic Scholar 在四组查询中返回 HTTP 429；DBLP 五组出现 SSL EOF、一组 handshake timeout。OpenAlex、Crossref 与 arXiv 仍可工作；逐请求信息保存在 `tmp/literature-search-20260814-methods/*/results.json`。

## 2. 全文证据表

| 论文 | 版本与核验 | 主要测试对象/方法 | Oracle 与指标 | 关键局限 |
|---|---|---|---|---|
| AgentChaos | ASE 2026；arXiv:2608.06790；DOI 由论文/OpenAlex 支持，Crossref 待入库 | HTTP 层 65 个 API 故障配置；验证注错实际触发 | `pass@1` 差值、fault-type/step accuracy | 不覆盖工具、环境状态和内部并发故障 |
| OrchestraBench | arXiv:2608.05263 | orchestration 注错、恢复、级联和分解 | routing accuracy、分故障恢复率、cascade radius | 小型可验证依赖链，属于机制探针 |
| MAS-FIRE | arXiv:2602.19843 | 15 类语义/协调故障，跨三种 MAS 架构 | Robustness Score、分层 fault-tolerance occurrence | 人工故障分布、三种架构、两种模型 |
| Who Broke the System? | COLM 2026 论文稿；arXiv:2607.07989 | Judge 提案、多 Evaluator 复核、微调 Judge | Agent/step accuracy、容差、成本 | 同源 Evaluator、自报置信度、标签依赖 |
| VerifyMAS | arXiv:2605.17467 | error-first 全轨迹三值 hypothesis verification | Micro/Class F1、agent-error pair F1 | 依赖预定义 taxonomy，未知错误覆盖不足 |
| AgentDebugX | arXiv:2607.18754；开源软件 | 采集—归因—修复—重跑闭环 | 联合 Agent+Step accuracy、修复任务数、成本 | 固定失败子集，不能隔离归因单独贡献 |
| REFLECT | ICML FAGEN workshop；arXiv:2606.09071 | 定向 patch、保持前缀 replay、outcome flip 反哺定位 | exact/off-by-one、verified coverage、AUROC/F1 | 干预成功不证明原因唯一或最小 |
| StepFinder | KDD 2026；DOI 10.1145/3770855.3817991 | 轻量 agent-aware 时序异常排序 | Acc@K、MRR、容差、token、延迟 | 监督标签与单 benchmark 泛化风险 |
| Seeing the Whole Elephant | ACL 2026；DOI 10.18653/v1/2026.acl-long.912 | 完整 trace、输入/metadata 消融、局部重放 | Agent/step accuracy，三次运行平均 | 全 trace 隐私风险；动态验证只观察三步 |

观察项：AgentTelemetry 与 ICST 的 Observability/Fault Injection 论文有已核验 DOI，但未找到可确认的合法开放全文；AgentTrace、FALAT、Causal Agent Replay 本轮仅阅读摘要。它们不能支撑以下详细综合。

## 3. 方法综合

### 3.1 如何生成测试与注入故障

当前出现两条互补路线。AgentChaos 在共享 LLM HTTP 边界注入 crash、omission、value fault，优势是跨框架和非侵入；MAS-FIRE、OrchestraBench 则修改提示、消息、协调和任务依赖，能覆盖语义漂移、错误委派和级联，但更依赖具体 harness。测试平台应同时提供 transport/API fault 与 semantic/orchestration fault 两层，并显式记录某配置是否可注入、是否真正触发。

现有直接针对 Agent 的 coverage-guided、metamorphic 或 greybox 工作仍稀少。本轮高排名结果中，多数相关题名实际是让 Agent/LLM 去 fuzz REST API、协议或传统软件，不能作为“Agent 被测对象”的证据。因此覆盖概念目前更适合落在 Agent 状态、轨迹分支、工具 schema、权限边界和故障触发覆盖，而不是照搬代码覆盖率。

### 3.2 使用什么 oracle

证据显示 oracle 正从终态向多层诊断发展：

1. AgentChaos 用可执行 benchmark 的任务结果衡量故障影响，并用注错 trace 确认触发。
2. OrchestraBench 与 MAS-FIRE加入恢复率、传播范围和容错行为层级。
3. Who Broke、VerifyMAS、StepFinder 把轨迹 oracle 表述为责任 Agent、决定步骤或错误类型。
4. REFLECT 和 TraceElephant 进一步用保持前缀的重放/干预检查归因假设。

最强 oracle 不是一个更大的 Judge，而是“可执行终态 + 结构化轨迹规则 + 校准归因器 + 必要时 counterfactual replay”的组合。Judge 仍适合生成候选和处理开放语义，但不应独自声明因果真值。

### 3.3 怎样定位根因

- `AgentLocate` 通过多视角复核减少单次 Judge 脆弱性，但 Evaluator 同源和自报置信度仍可能形成相关偏差。
- `VerifyMAS` 先问错误类型是否被全轨迹支持，再找责任组件，减少 agent-first 对局部症状的偏好，但 taxonomy 之外的错误难以识别。
- `StepFinder` 将定位转化为时序异常排序，适合大规模低延迟筛查；它需要监督数据且未证明跨 benchmark 泛化。
- `REFLECT` 用实际干预把候选归因变成可测试假设，但 outcome flip 只表明某次修复足以改变结果，不证明根因唯一。
- `TraceElephant` 说明观察条件会决定诊断上限：缺少输入与状态时，根因可能从证据上不可辨识。

因此报告根因时应区分 source、first decisive step、symptom manifestation 和 recovery opportunity；晚期 verifier 看见错误不等于它制造了错误。

### 3.4 如何评价检测效果与成本

最小指标集应包含：任务成功差值、注错触发覆盖率、fault detection precision/recall、责任 Agent accuracy、exact/±1 step accuracy、cascade radius、按故障类型恢复率、误报/误阻断、token、延迟和每修复任务成本。随机 Agent 执行还应多 seed 重复并报告置信区间。

AgentDebugX 证明归因指标还应与一次受控重跑连接，检查诊断能否改善结果；但应设置组件消融，避免把更强提示、额外搜索和归因贡献混在一个 recipe 中。StepFinder 则展示在线场景可用轻量模型做第一层筛查，把昂贵的 replay 或多 Judge 复核留给不确定案例。

### 3.5 可观测性与隐私

TraceElephant 的完整输入/metadata 显著改善归因，AgentDebugX 也需要统一事件 schema；但完整 trace 会包含提示、工具参数、文件、截图、PII 和凭据。工程实现应默认本地存储、字段级采集、已知凭据/PII 脱敏、访问控制和人工审查；后续研究需要测量“删除哪些字段后诊断能力下降多少”，形成 privacy–diagnosability 曲线。

## 4. 冲突、局限与研究空白

1. **出版身份变化快。** StepFinder 与 TraceElephant 的 DOI 已双源核验；AgentChaos 的 DOI 由论文和 OpenAlex 支持但 Crossref 尚未解析。其余预印本的 Crossref 模糊匹配均未采纳。
2. **故障模型缺少生产校准。** API、语义、路由和消息故障多由研究者设计，尚未与真实 incident/telemetry 分布建立频率与严重度映射。
3. **归因真值仍不稳。** “最早错误”“决定性错误”“应负责的 verifier”和“可修复点”不是同一个概念；不同 benchmark 定义会改变标签。
4. **相关 Judge 偏差。** Judge、Evaluator、被测 Agent 和自动标注器经常来自同类模型，独立性和校准不足。
5. **反事实重放受随机性污染。** 新轨迹的提示、工具和协调会随干预变化，需配对 seed、冻结环境并区分局部充分性与唯一因果。
6. **直接 Agent 灰盒/变形测试仍是空白。** 目前大量工作是 Agent 生成传统软件测试，真正以 Agent 状态和轨迹覆盖为反馈的研究很少。
7. **隐私—可诊断性没有共同指标。** 完整 trace 提升定位，但现有工作几乎不报告脱敏后的诊断损失。
8. **修复闭环缺少安全约束。** 自动 rerun 可能放大副作用；诊断置信度、权限、预算和人工审批应进入测试协议。

## 5. 可复现成果

- 9 份开放 PDF：`research/papers/2026-*.pdf` 中对应本轮文件，均通过 PDF 签名和 `pdfinfo` 检查。
- 9 份结构化全文笔记：`research/notes/2026-*-*.md`。
- 证据与筛选：`research/evidence/evidence-table.csv`、`screening-log.csv`。
- 核验引用：`research/references.bib`。
- 原始检索 manifest：`tmp/literature-search-20260814-methods/`；临时结果不作为正式证据文件。
