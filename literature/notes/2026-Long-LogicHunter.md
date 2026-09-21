# LogicHunter 阅读笔记

- 论文：*LogicHunter: Testing LLM Agent Frameworks with an Agentic Oracle*
- 年份/版本：2026，arXiv:2607.06195。
- 被测对象：LangChain、LlamaIndex、CrewAI 等 agent framework。
- 方法：融合类型约束与真实仓库用法，生成“有效但语义极端”的输入；agentic oracle 主动查文档、源码和运行时状态以判定异常或静默语义错误。
- 主要贡献：同时解决传统 fuzzer 无效输入过多和普通 LLM oracle 被动、知识过时的问题。
- 局限：依赖真实用例质量；agentic oracle 有成本、非确定性和自身错误；框架快速演化。
- 开源：https://github.com/security-pride/LogicHunter
- 证据：全文阅读，架构、实验、消融、局限与 artifact 已检查。
