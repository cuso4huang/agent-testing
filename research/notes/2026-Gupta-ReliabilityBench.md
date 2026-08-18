# ReliabilityBench 阅读笔记

- 论文：*ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions*
- 年份/版本：2026，arXiv:2601.06112；未核验正式出版版本。
- 研究问题：如何把一次任务成功扩展为生产式可靠性测量。
- 方法：定义 `R(k, ε, λ)`，分别控制重复运行次数、语义等价扰动强度和工具/API 故障强度；比较 ReAct 与 Reflexion 等 agent。
- Oracle/指标：`pass^k`、扰动后任务成功、故障下成功与综合可靠性表面。
- 主要结论：单次成功会高估可靠性；扰动与故障产生的退化不等价，复杂 scaffold 不必然更可靠。
- 局限：预印本；领域和 agent 架构有限，故障模型无法穷尽生产基础设施问题。
- 与主题关系：是重复、变形和故障注入组合测试的直接范例。
- 开源：论文身份开放；代码状态需继续核验。
- 证据：全文阅读，方法、实验、讨论和局限已检查。
