# AgentLens 阅读笔记

- 论文：*AgentLens: Production-Assessed Trajectory Reviews for Coding Agent Evaluation*
- 年份/版本：2026，arXiv:2607.06624。
- 方法：将能程序化的正式检查与 LLM 生成的整轨迹 review、成对比较结合，并用于 nightly regression。
- 评测维度：指令遵循、工具使用、验证、错误恢复和用户沟通，而非只看测试是否通过。
- 主要价值：把 benchmark 作为产品诊断和版本回归工具，而不是单纯 leaderboard。
- 局限：单一 coding-agent 产品和任务分布；judge 与生产标注可能存在组织特定偏差。
- 开源：https://github.com/agent-lens/agent-lens-bench
- 证据：全文阅读，数据、评分、生产评估、案例和局限已检查。
