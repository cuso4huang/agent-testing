# MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems

## 1. 基本信息

- 作者：Jin Jia; Zhiling Deng; Zhuangbin Chen; Yingqi Wang; Zibin Zheng
- 年份/版本：2026，arXiv:2602.19843v1，预印本
- 身份核验：arXiv 与 OpenAlex 精确匹配；Crossref 返回 ICST 他文的模糊匹配，未采纳。

## 2. 研究问题

如何系统注入多智能体语义与协作故障，并以过程指标解释不同架构为什么能或不能容错（摘要、§1）。

## 3. 被测试的智能体类型

MetaGPT、Camel 与 Table-Critic 三种具有不同协调结构的 LLM 多智能体系统，骨干模型包括 GPT-5 与 DeepSeek-V3（§4.1）。

## 4. 测试或评估方法

- 构造 15 类 intra-agent 与 inter-agent 故障，覆盖 planning、memory、reasoning、action、配置、指令和协调机制。
- 在运行时对提示、消息、输出或路由实施故障，并记录故障容忍行为发生在哪个层次。
- 通过 LLM 自动标注过程行为，并用人工 held-out 集验证一致性（§3–§4）。

## 5. 数据集、环境或基准

在三套 MAS 的原生任务/工作流中执行注错；论文按系统架构限制明确标出无法注入的灰色组合（§4、图4）。

## 6. 评价指标

Robustness Score、fault-tolerance occurrence，以及 prompt、reasoning、mechanism、rule 等层级的检测/恢复行为；自动标注器与人工的 Cohen’s κ 为 0.94（§3.3、§4.2）。

## 7. 实验设计

在 3 个系统、2 个骨干模型和 15 类故障上比较鲁棒性与容错机制，围绕故障影响、架构机制和恢复策略组织研究问题（§4–§5）。

## 8. 主要发现

- 共享消息池、迭代批评和环境反馈等结构会分别缓冲记忆、规划与动作故障（§5.1）。
- 配置与指令故障可破坏协作语义契约；语法正确但语义错误的故障常绕过机制级过滤，更多依赖 reasoning-level 检测（§5.1–§5.2）。
- 线性单路径 pipeline 更容易让上游语义错误级联，闭环验证结构相对更有恢复机会（§6.2）。

## 9. 局限性

实验仅覆盖三种架构和两种模型；15 类人工故障未由生产 incident 分布校准。部分组合因架构或输出格式无法注入，比较矩阵并不完整；过程标签还依赖 LLM 自动标注（§4、§6）。

## 10. 可复现性信息

论文给出故障分类、系统、模型、注错逻辑与评价指标；正文引用 Agentscope OpenJudge，但未发现明确的 MAS-FIRE 官方代码仓库。预印本仍保留模板化会议占位信息。

## 11. 与“智能体测试”研究的关系

MAS-FIRE 是直接面向多智能体系统的语义故障注入与可靠性测评框架，补充 AgentChaos 偏 API/传输层的故障模型。

## 12. 可借鉴的工程实现

故障—架构可注入性矩阵、分层容错标签、共享内存/批评环/反馈环消融，以及按故障类别绘制 reliability surface。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `research/papers/2026-Jia-MASFIRE.pdf`，16 页。

## 14. 可支持的综述结论

Agent 测试需要同时覆盖低层 API 故障与高层语义/协调故障；鲁棒性不只由模型决定，还受到通信和验证拓扑显著影响。
