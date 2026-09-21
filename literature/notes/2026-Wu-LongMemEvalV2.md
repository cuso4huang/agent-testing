# LongMemEval-V2 阅读笔记

- 论文：*LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues*
- 年份/版本：2026，arXiv:2605.12493。
- 方法：把长期 memory 建立在多模态 Web agent 轨迹和工作经验上，测 agent 是否能像熟悉组织环境的同事一样利用经验。
- 主要价值：从个人事实回忆推进到工作流知识、轨迹证据和经验复用；引入 memory controller 与 downstream reader 的分解。
- 测试启示：保存轨迹来源、模态、时间和工作流规则；分别评估 memory construction、retrieval、reasoning 与最终回答。
- 局限：依赖 WebArena/AgentLab/Codex 等特定生态；轨迹成本高，视觉和文本表示会混入额外变量。
- 开放资源：https://xiaowu0162.github.io/longmemeval-v2/
- 证据：全文、主实验、消融与局限已检查。
