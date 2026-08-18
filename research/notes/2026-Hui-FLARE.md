# FLARE 阅读笔记

- 论文：*FLARE: Agentic Coverage-Guided Fuzzing for LLM-Based Multi-Agent Systems*
- 年份/版本：2026，arXiv:2604.05289。
- 方法：读取 MAS 源码与 agent 定义，抽取任务规格、主体内行为和主体间执行路径；据此构造 oracle 并用覆盖反馈引导测试。
- 覆盖：inter-agent execution path coverage 与 intra-agent expected/boundary behavior coverage。
- 主要贡献：将 coverage-guided fuzzing 直接用于被测多智能体应用，而不是让 agent 去测试其他软件。
- 局限：自动抽取的规格可能不完整；语义 oracle 与生成模型相关；预印本尚待独立复现。
- 证据：arXiv 全文页面与方法/实验段落已检查；本地 PDF 下载受限，未使用摘要之外未核实数字。
