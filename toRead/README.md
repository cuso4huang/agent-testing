# Agent 测试论文阅读包

检索与核对日期：2026-07-29。下列 8 篇均已下载 PDF，并基于全文生成中文阅读笔记。

| # | 论文 | 核心学习目标 | PDF | Notes |
|---|---|---|---|---|
| 1 | Agent-Testing Agent (ATA) | 自动化 Agent 测试框架 | [PDF](01-ATA-Agent-Testing-Agent.pdf) | [Notes](01-ATA-Agent-Testing-Agent-notes.md) · [全文翻译](01-ATA-Agent-Testing-Agent-全文翻译.md) |
| 2 | SIRAJ | 黑盒自动红队测试 | [PDF](02-SIRAJ.pdf) | [Notes](02-SIRAJ-notes.md) |
| 3 | AgentDoS | 程序分析 + 灰盒 Fuzzing | [PDF](03-AgentDoS.pdf) | [Notes](03-AgentDoS-notes.md) |
| 4 | Les Dissonances | 多工具控制流和数据流 | [PDF](04-Les-Dissonances.pdf) | [Notes](04-Les-Dissonances-notes.md) |
| 5 | Prompt Injection Attack to Tool Selection | 工具选择测试 | [PDF](05-Tool-Selection-Prompt-Injection.pdf) | [Notes](05-Tool-Selection-Prompt-Injection-notes.md) |
| 6 | MemoryAgentBench | 有状态、长期记忆测试 | [PDF](06-MemoryAgentBench.pdf) | [Notes](06-MemoryAgentBench-notes.md) |
| 7 | MobileSafetyBench | 真实交互环境中的安全预言机 | [PDF](07-MobileSafetyBench.pdf) | [Notes](07-MobileSafetyBench-notes.md) |
| 8 | Process Evaluation for Agentic Systems | 为什么必须测完整轨迹 | [PDF](08-Process-Evaluation.pdf) | [Notes](08-Process-Evaluation-notes.md) |

## 建议阅读顺序

先读 ATA 建立端到端测试框架，再读 Process Evaluation 明确“结果 + 过程”双重评价。随后按攻击面展开：SIRAJ（黑盒生成）→ AgentDoS（灰盒引导）→ Tool Selection（选择阶段）→ Les Dissonances（跨工具控制流/数据流）。最后读 MemoryAgentBench 与 MobileSafetyBench，补齐状态维度和真实环境预言机。

## 一张统一测试模型

这 8 篇可以归并为六个测试部件：

1. **被测系统建模**：ATA 的代码图/开发者访谈；SIRAJ 的黑盒 agent definition。
2. **测试输入生成**：ATA 的 persona；SIRAJ 的风险种子与迭代攻击；AgentDoS 的语义变异。
3. **覆盖反馈**：弱点、风险结果、工具轨迹、程序 sink、资源生命周期、记忆能力维度。
4. **执行环境**：对话沙箱、真实工具池、Android 模拟器、跨多轮持久状态。
5. **预言机**：LLM judge、资源监测、最终环境状态与动作历史、合规检查表。
6. **报告与回归**：不仅记录任务成败，还保存完整轨迹、首个偏离点、危害、严重度与可复现测试。

## 版本说明

- ATA、SIRAJ、MemoryAgentBench、Process Evaluation 使用 2026 会议版本或会议标注版本。
- AgentDoS 使用 USENIX Security 2026 预印本。
- Les Dissonances 与 Tool Selection Prompt Injection 使用 NDSS 2026 版本。
- MobileSafetyBench 使用 arXiv 最新扩展版（下载时为 arXiv:2410.17520 的当前版本）。
