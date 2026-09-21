# Agent-Testing Agent 阅读笔记

- 论文：*Agent-Testing Agent: A Meta-Agent for Automated Testing and Evaluation of Conversational AI Agents*
- 年份/版本：EACL 2026；DOI `10.18653/v1/2026.eacl-long.339`。
- 方法：结合静态代码分析、开发者询问、文献检索和 persona 驱动的对抗测试；依据 judge 反馈动态提升难度。
- 输出：量化评分与面向开发者的定性 bug report。
- 主要价值：从固定 benchmark 转向针对被测 agent 的自适应测试生成。
- 局限：只验证少量应用；LLM judge 与测试生成器可能共享偏差，web/code 证据也会漂移。
- 开源：https://github.com/KhalilMrini/Agent-Testing-Agent
- 证据：本地正式论文全文阅读，方法、实验、消融和局限已检查。
