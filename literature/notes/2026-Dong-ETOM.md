# ETOM 阅读笔记

- 论文：*ETOM: A Five-Level Benchmark for Evaluating Tool Orchestration within the MCP Ecosystem*
- 年份/版本：Findings of EACL 2026；DOI `10.18653/v1/2026.findings-eacl.75`。
- 方法：五级课程从单工具扩展到跨 server、多跳规划和 out-of-scope 拒绝；用 equal function sets 构造客观 ground truth。
- Oracle/指标：工具集合/编排 F1 等确定性指标，减少对 LLM-as-a-Judge 的依赖。
- 主要结论：单工具表现不能预测跨 server 编排；工具重叠、依赖和越界检测带来新的失败。
- 局限：模拟 MCP 生态和预定义等价函数集不能代表全部真实 server。
- 开源：https://github.com/snooow1029/ETOM
- 证据：全文阅读，benchmark、实验、错误分析和局限已检查。
