# SIRAJ 阅读笔记

- 论文：*SIRAJ: Diverse and Efficient Red-Teaming for LLM Agents via Distilled Structured Reasoning*
- 年份/版本：Findings of EACL 2026；DOI `10.18653/v1/2026.findings-eacl.171`。
- 方法：从 agent 定义生成覆盖风险结果、工具轨迹和风险来源的 seed；根据历史执行轨迹迭代攻击；蒸馏教师的结构化推理降低成本。
- 主要价值：把安全测试从固定攻击模板推进到反馈驱动、面向任意黑盒 agent 的自动红队。
- 局限：风险 taxonomy 和 evaluator 决定可见覆盖；攻击成功不等于现实风险严重度。
- 证据：本地正式论文全文阅读，框架、实验、消融与讨论已检查。
