# AgentDoS 阅读笔记

- 论文：*Autonomy Comes with Costs: Detecting Denial-of-Service Vulnerabilities Caused by Resource Abusing in LLM-based Agents*
- 年份/版本：USENIX Security 2026 正式论文。
- 方法：分析单任务、session 和永久性资源生命周期；用 LLM 生成与功能相关的自然语言种子，以资源消耗反馈实施定向灰盒 fuzzing。
- Oracle：资源增长、释放行为、崩溃/不可用状态与 SARIF 式报告。
- 主要价值：将非功能测试和资源治理引入 agent testing，发现普通功能 benchmark 看不到的 DoS。
- 局限：开源 agent 样本与资源类型有限；安全实验必须在隔离环境中进行。
- 证据：本地正式稿全文阅读，设计、实现、实验、披露和局限已检查。
