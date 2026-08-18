# MemoryAgentBench 阅读笔记

- 论文：*Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*
- 年份/版本：ICLR 2026；arXiv:2507.05257。
- 研究问题：如何在增量交互而非一次性长上下文中评测 memory agent。
- 方法：按记忆科学划分准确检索、test-time learning、长程理解和选择性遗忘，统一比较 memory architectures。
- 主要结论：现有 memory agent 在部分检索任务有效，但面对动态更新、长程推理和遗忘要求仍有明显缺口；更强 backbone 不能消除机制性问题。
- 测试启示：记忆写入、更新、检索和使用应分阶段记录；必须设置 no-memory/long-context 对照。
- 局限：任务与实现选择有限；不同 memory 系统的预算和索引策略难完全等价。
- 开源：论文提供数据与源码入口。
- 证据：全文阅读，数据构造、协议、实验和附录已检查。
