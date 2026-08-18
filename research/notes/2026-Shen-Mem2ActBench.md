# Mem2ActBench 阅读笔记

- 论文：*Mem2ActBench: A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents*
- 年份/版本：ACL 2026；arXiv:2601.19935。
- 研究问题：agent 能否从历史中自行判断要检索哪些约束，并把它们落实为工具调用。
- 方法：从 memory chains 反向生成工具任务，刻意省略当前指令中的关键参数，迫使 agent 使用长期记忆。
- Oracle/指标：工具选择/参数的精确或 F1 类检查，区分检索与 action grounding。
- 主要结论：纯问答式记忆 benchmark 会高估真实任务能力；当前方法在从记忆到动作的转换上仍有明显缺口。
- 局限：工具和任务分布有限；反向生成的自然度与真实依赖由人工抽样确认而非完全保证。
- 开源：论文声明代码和数据开放。
- 证据：全文阅读，数据生成、实验、分析和局限已检查。
