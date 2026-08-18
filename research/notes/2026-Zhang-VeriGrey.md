# VeriGrey 阅读笔记

- 论文：*VeriGrey: Greybox Agent Validation*
- 年份/版本：2026，arXiv:2603.17639。
- 方法：用工具调用序列作为灰盒反馈，变异间接注入 prompt，并把正常任务与注入任务联结以探索低频危险行为。
- 场景：AgentDojo、Gemini CLI、OpenClaw/skills。
- 主要价值：提出 agent 行为覆盖的具体代理信号，优于完全黑盒的随机 prompt 变异。
- 局限：不同语义状态可能共享工具序列；新序列不必然代表新风险；当前为预印本。
- 开放性：全文开放；artifact 状态需继续跟踪。
- 证据：本地全文阅读，方法、实验、case studies 和讨论已检查。
