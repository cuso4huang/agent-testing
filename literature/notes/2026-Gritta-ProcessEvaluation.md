# Process Evaluation for Agentic Systems 阅读笔记

- 论文：*Process Evaluation for Agentic Systems*
- 年份/版本：Findings of EACL 2026；DOI `10.18653/v1/2026.findings-eacl.140`。
- 研究问题：正确答案是否通过合规、方法化且可审计的过程获得。
- 方法：为任务构造 process questions/rubrics，结合 partial accuracy、答案正确性和过程合规评测 deep-research/GAIA 类 agent。
- 主要结论：最终正确与过程正确并不等价；过程规则比具体答案更容易跨任务迁移，但 judge 仍需校准。
- 局限：任务与过程问题规模有限；LLM judge、人工规则与长轨迹成本限制泛化。
- 开源：https://github.com/deepsynth/process_eval
- 证据：全文阅读，构造、实验、整体评测框架和局限已检查。
