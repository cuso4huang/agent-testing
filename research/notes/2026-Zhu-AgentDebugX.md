# AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents

## 1. 基本信息

- 作者：Kunlun Zhu 等
- 年份/版本：2026，arXiv:2607.18754v1，预印本
- 身份核验：arXiv 与 OpenAlex 精确匹配；Crossref 模糊结果为他文，未采纳。
- 代码：https://github.com/AgentDebugX/AgentDebugX

## 2. 研究问题

如何把 trace 采集、异常检测、根因归因、修复建议、受控重跑和历史失败记忆连成可部署的闭环调试工具（§1–§3）。

## 3. 被测试的智能体类型

单 Agent 和多智能体、ReAct/工具使用、LangChain/LangGraph、CrewAI、OpenAI Agents SDK、OpenTelemetry GenAI 等多种运行时（§2、附录 D）。

## 4. 测试或评估方法

统一事件 schema 后，DeepDebug 先结构化读取轨迹、形成多个候选，再对分歧候选做局部窗口 cross-examination；输出责任 Agent、步骤、failure mode、置信度、证据和修复建议。失败可在人工/策略批准后重跑（§3–§4）。

## 5. 数据集、环境或基准

Who&When 全集 184 条用于归因；GAIA validation 165 题用于端到端恢复，其中基线失败 73 题（附录 C）。

## 6. 评价指标

Agent accuracy、exact/±1 step accuracy、联合 Agent+Step accuracy、恢复任务数、分难度成功率、token 与运行成本（§4、附录 C）。

## 7. 实验设计

归因比较规则、all-at-once、step-by-step、binary search 与 DeepDebug；恢复比较 DeepDebug 指令、Reflexion、CRITIC、AutoManual，并固定同一失败子集和一次重跑（§4）。

## 8. 主要发现

- Who&When 上 DeepDebug 的 Agent accuracy 为 56.0%，严格联合准确率 28.8%，高于论文中的单次读取对照 47.8% 和 21.7%（§4、表2）。
- GAIA 中 DeepDebug 修复 13/73 个失败任务，高于对照的 4–6 个；完整成功率由 55.8% 提升至 63.6%（§4、表3）。
- 收益主要集中在超过 40 个事件的长 trace，但该组仅 26 条，作者明确视为描述性证据（§4）。

## 9. 局限性

没有评价开发者调试时间和 UI；Who&When 提供参考答案；额外多次调用并非对所有模型有益。GAIA 只测一个 policy model 和固定失败子集，比较的是完整重试 recipe，不能隔离归因单独贡献。Error Hub 与 taxonomy induction 尚未实证（附录 E）。

## 10. 可复现性信息

MIT 许可 Python 包，可通过 `pip install agentdebugx`；支持 JSONL/SQLite、runtime adapter、offline importer 和 OpenTelemetry。论文给出提示、解码参数与评测协议（附录 B–D）。

## 11. 与“智能体测试”研究的关系

补足从离线 benchmark 到 CI/incident debugging 的工程接口，并用重跑结果检查诊断是否能真正改善任务结果。

## 12. 可借鉴的工程实现

统一 trace schema、成本分级诊断、本地优先存储、证据化归因、人工批准恢复、失败语料库与 CI regression fixture。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `research/papers/2026-Zhu-AgentDebugX.pdf`，10 页。

## 14. 可支持的综述结论

生产级 Agent 测试需要把 observability、diagnosis 和 recovery 连成闭环，同时将诊断输出呈现为带证据与置信度的假设而非确定真值。
