# LLM-Coordination 阅读笔记

- 论文：*LLM-Coordination: Evaluating and Analyzing Multi-agent Coordination Abilities in Large Language Models*
- 年份/版本：Findings of NAACL 2025；DOI `10.18653/v1/2025.findings-naacl.448`。
- 方法：结合 agentic coordination games 与 CoordQA，分解环境理解、Theory of Mind 和联合规划。
- 主要结论：基于环境变量的协调较好，但涉及伙伴信念与意图时明显困难；零样本新伙伴提供独立的泛化测试。
- 测试启示：把团队成功拆成 partner modeling、joint planning 和 unseen-partner robustness。
- 局限：纯协调游戏和离散动作限制现实外推。
- 开源：论文提供实现入口。
- 证据：全文阅读，任务、指标、实验和局限已检查。
