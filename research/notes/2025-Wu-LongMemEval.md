# LongMemEval 阅读笔记

- 论文：*LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*
- 年份/版本：ICLR 2025；arXiv:2410.10813。
- 方法：覆盖信息提取、多 session 推理、时间推理、知识更新与拒答，使用长对话历史评测长期记忆。
- 主要贡献：提供可控长历史与问题，并系统分析检索、索引、扩展和阅读策略。
- 测试启示：需要分别测“是否写入”“是否取回”“是否正确更新”“无证据时是否拒答”，不能把最终 QA 准确率全部归因于 memory。
- 局限：更接近对话助手记忆，工具动作和真实副作用较少；合成历史与真实用户历史存在差距。
- 开源：https://github.com/xiaowu0162/LongMemEval
- 证据：全文与附录已阅读。
