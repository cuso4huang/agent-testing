# Gaia2 阅读笔记

- 论文：*Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments*
- 年份/版本：ICLR 2026 正式论文；arXiv:2602.11964。
- 研究问题：agent 能否在动态、异步、有噪声和其他 agent 参与的环境中持续执行。
- 方法：统一测试 execution、search、ambiguity、adaptability、time、noise 和 agent-to-agent 等能力；环境事件与 agent 动作异步发生。
- Oracle/指标：任务特定 verifier、pass@1、能力切片和 scaffold 对照。
- 主要结论：时间相关任务尤其困难；异步和动态状态揭示静态问答/同步工具环境遗漏的失败。
- 局限：模拟世界仍不能覆盖开放互联网和真实组织流程；verifier 与软检查需要持续校准。
- 开源：论文和项目材料开放。
- 证据：全文阅读，环境、任务、verifier、实验与附录已检查。
