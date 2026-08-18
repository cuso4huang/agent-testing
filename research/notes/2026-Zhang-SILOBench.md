# SILO-BENCH 阅读笔记

- 论文：*SILO-BENCH: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems*
- 年份/版本：ACL 2026；DOI `10.18653/v1/2026.acl-long.1354`。
- 方法：让每个 agent 只持有全局问题的一部分；按 aggregation、mesh、global shuffle 三种通信复杂度设计 30 个精确答案任务，并变化协议、agent 数和模型。
- 指标：成功率、token 消耗、communication density。
- 主要结论：高通信活跃度不等于有效分布式推理；规模和通信复杂度提高时性能急剧下降。
- 局限：算法题与精确 oracle 有利于可重复性，但不覆盖开放语义协作。
- 开源：https://github.com/jwyjohn/acl26-silo-bench
- 证据：全文和 ACL 元数据已检查。
