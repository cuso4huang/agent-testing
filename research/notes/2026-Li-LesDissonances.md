# Les Dissonances 阅读笔记

- 论文：*Les Dissonances: Cross-Tool Harvesting and Polluting in Pool-of-Tools Empowered LLM Agents*
- 年份/版本：NDSS 2026；DOI `10.14722/ndss.2026.240577`。
- 威胁：跨工具 harvesting/polluting 通过控制流劫持，在工具池中收集或污染敏感信息。
- 方法：Chord 动态扫描 LangChain/LlamaIndex 真实工具，组合工具依赖、输入输出和控制流进行测试。
- 主要价值：安全测试单元从单工具扩大到工具组合、数据流和任务控制流。
- 局限：框架和工具样本有限；动态扫描依赖可观测性，不能证明未发现路径安全。
- 开源：https://github.com/systemsecurity-uiuc/Chord/
- 证据：本地 NDSS 正式稿全文阅读，威胁模型、扫描器、实验和附录已检查。
