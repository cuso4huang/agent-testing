# 九篇智能体测试论文：七问精读导航

检索与核查日期：2026-09-19。

本文是三份逐篇精读的导航。每篇均按以下结构分析：Problem、Gap、Insight、Technique、Evaluation、Weakness、My Idea。

## 分组精读

1. [SpecOps、AgentInspect、Datura](../paper-deep-dives/2026-09-19-paper-deep-dive-specops-agentinspect-datura.md)
   - 真实环境端到端测试
   - agent-specific coverage 与工具异常模拟
   - 工具调用链渐进式红队测试

2. [LogicHunter、AgentChaos、llmmas-otel](../paper-deep-dives/2026-09-19-paper-deep-dive-logichunter-agentchaos-llmmas-otel.md)
   - agent framework fuzzing 与 agentic oracle
   - LLM API 层混沌工程
   - 多智能体 trace observability 与定点故障注入

3. [FAMAS、AgentBreaker、ToolLeak](../paper-deep-dives/2026-09-19-paper-deep-dive-famas-agentbreaker-toolleak.md)
   - 多智能体失败 action 定位
   - context-aware Web 间接提示注入
   - coding-agent 工具调用的信息流与控制流攻击

## 一句话抓住九篇论文

| 论文 | 最核心的贡献 | 最值得继续做的方向 |
|---|---|---|
| SpecOps | 用四类 specialist 串起真实环境中的生成、布置、执行与判定 | 可重放的反事实环境测试与因果归因 |
| AgentInspect | 真实轨迹捕获加异常工具响应模拟，再用确定性规则找行为故障 | 跨框架 contract coverage 与语义故障模型 |
| Datura | 让每一步看似合法、整条工具链最终产生有害结果 | 状态化覆盖引导、攻击最小化与安全回归测试 |
| LogicHunter | 规格感知输入生成配合主动查文档、源码和状态的 oracle | 降低 LLM oracle 的相关偏差与不确定性 |
| AgentChaos | 在统一 LLM HTTP 边界非侵入注错，并先验证故障确实触发 | 扩展到工具、环境、并发及组合故障 |
| llmmas-otel | 将跨 agent trace 与可定位注错统一到 OpenTelemetry | 从初步工具验证扩展成标准化实验平台 |
| FAMAS | 把重复执行当作测试套件，用频谱可疑度定位失败 action | 用反事实重放从相关定位升级到因果定位 |
| AgentBreaker | 根据当前任务和 DOM 语境迭代生成网页注入文本 | 上下文覆盖、变形测试与真实副作用 oracle |
| ToolLeak | 揭示 schema 参数填充可泄密，tool description/return 可形成两阶段劫持 | 动态信息流、能力流覆盖与版本化安全回归 |

## 横向结论

这九篇可以拼成一条较完整的智能体测试流水线：

1. SpecOps、LogicHunter、AgentBreaker、Datura 负责生成有效或对抗性测试；
2. AgentInspect、AgentChaos、llmmas-otel 负责受控执行、注错与轨迹采集；
3. LogicHunter、SpecOps、ToolLeak 提供不同形式的 oracle；
4. FAMAS 在失败后定位最可疑的 agent action；
5. 当前共同短板是缺少跨框架覆盖标准、独立且低成本的 oracle、组合故障模型、确定性回放和真实副作用验证。

证据边界：SpecOps、Datura、LogicHunter、AgentChaos、llmmas-otel、FAMAS、ToolLeak 使用开放全文；AgentInspect 使用官方摘要与公开复现包；AgentBreaker 使用官方摘要与公开 artifact 源码。ISSTA/ASE 2026 在检索日尚未举行，相应官方 program 状态需会后复核。
