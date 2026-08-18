# AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection

## 1. 基本信息

- 作者：Gou Tan 等
- 年份/版本：ASE 2026；arXiv:2608.06790；DOI: 10.1145/3832783.3837437
- 版本核验：论文首页给出 ASE 2026 与 DOI，OpenAlex 精确匹配；Crossref 于 2026-08-14 返回 404，故记为部分核验。
- 开放全文：https://arxiv.org/abs/2608.06790

## 2. 研究问题

如何在不修改不同 Agent 系统源码的情况下，对运行中的 LLM API 响应实施可控故障，并避免把未实际触发的注错任务计入鲁棒性结果（摘要、§1、§4）。

## 3. 被测试的智能体类型

覆盖问答、代码生成和软件工程 Agent 系统；论文比较多种系统、benchmark 与骨干模型（§5）。

## 4. 测试或评估方法

- 在共享 HTTP 客户端层安装运行时 wrapper，拦截并修改 LLM API 响应，不改 Agent 源码（§4.1–§4.3）。
- 故障分类为 crash、omission、value fault，并作用于 `content` 或 `tool_calls`；结合 single、persistent、intermittent、burst 策略、注入位置和复合场景形成 65 个配置（§3、§4.2）。
- 通过执行 trace 验证注错是否实际触发，只在已触发任务上计算影响（§4.4）。

## 5. 数据集、环境或基准

实验横跨多个 Agent 系统与问答、代码生成、软件工程 benchmark；完整组合见论文 §5 表格。注错对象是实际运行期间的 LLM API 调用，而非离线改写完成轨迹。

## 6. 评价指标

主要用注错前后 `pass@1` 差值衡量鲁棒性，并用 fault-type accuracy 和 fault-step accuracy 评价诊断（§5.1、§5.4）。

## 7. 实验设计

每个任务绑定独立注错状态；配置包含故障类型、目标字段、触发策略和起始调用位置。论文比较无故障基线与已验证触发的故障运行，并分析系统、模型和诊断器差异（§4–§5）。

## 8. 主要发现

- 所有被测系统在注错下均退化，最大 `pass@1` 降幅达到 50 个百分点（摘要、§5）。
- 系统相对鲁棒性排序跨骨干模型较稳定，作者据此认为实现结构比单纯模型能力更关键（摘要、§5.3）。
- 规则和 LLM 诊断在 fault type 上低于 53%，在 fault step 上低于 56%，说明定位 oracle 仍弱（摘要、§5.4）。

## 9. 局限性

HTTP 层方法主要覆盖 LLM API 响应故障，不能代表工具、环境、共享状态和内部并发故障；实验系统和公开 benchmark 也不能等同生产故障分布。诊断结果依赖论文选定的故障标签与触发位置（§6.2）。

## 10. 可复现性信息

- 代码：https://github.com/IntelligentDDS/AgentChaos
- 论文给出 Python 3.12、HTTP wrapper、注错配置和触发验证机制（§4.3–§4.4）。
- 闭源模型/API 的精确历史快照仍会限制数值级复现。

## 11. 与“智能体测试”研究的关系

这是把传统 chaos engineering 迁移到 Agent 系统的直接测试方法贡献，并把“注错是否实际触发”提升为实验有效性的必要条件。

## 12. 可借鉴的工程实现

统一 API 拦截层、per-task 注错上下文、故障策略 DSL、trigger coverage、基线/故障配对运行和自动最小失败 trace。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `research/papers/2026-Tan-AgentChaos.pdf`，13 页。详细结论来自摘要、§3–§6。

## 14. 可支持的综述结论

Agent 故障注入应同时报告故障模型、触发覆盖率、任务退化和诊断准确率；只发出注错请求而不验证触发会低估风险。
