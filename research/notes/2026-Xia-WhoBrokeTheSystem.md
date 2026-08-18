# Who Broke the System? Failure Localization in LLM-Based Multi-Agent Systems

## 1. 基本信息

- 作者：Yufei Xia; Anjun Gao; Yueyang Quan; Zhuqing Liu; Minghong Fang
- 年份/版本：COLM 2026 论文稿；arXiv:2607.07989v1；未发现正式 DOI
- 身份核验：论文首页标注“Published as a conference paper at COLM 2026”；arXiv 身份明确。Crossref 模糊结果为他文，未采纳。

## 2. 研究问题

如何在长程、多工具和交织的多智能体轨迹中同时定位责任 Agent 与最早决定性失败步骤（§1、§3）。

## 3. 被测试的智能体类型

轮流行动的 LLM 多智能体系统，轨迹包含状态、动作、调度角色和工具交互（§2.1）。

## 4. 测试或评估方法

AgentLocate 先由 Judge 提出 `(agent, step)` 假设，再由三个采用不同提示风格的 Evaluator 独立复核，以自报置信度加权投票；最后把 Judge、Evaluator 理由和聚合结果转换为 LoRA 微调样本（§3.1–§3.3）。支持 full-trajectory 与 step-by-step 两种检查方式。

## 5. 数据集、环境或基准

Who&When 的 Algorithm-Generated、Hand-Crafted 子集，以及 Aegis-Bench。训练、验证和测试拆分见 §4.1。

## 6. 评价指标

责任 Agent accuracy、决定步骤 accuracy；Aegis-Bench 另用 agent accuracy 与 agent-error pair accuracy。附录还报告容差窗口、token、费用和运行时间（§4.1–§4.2）。

## 7. 实验设计

比较 WhichAgent、AgenTracer、ECHO、AEGIS 及两种 poisoning-forensics 方法；测试 Qwen、Llama、Mistral、GPT-4o，做 Evaluator 数量、模型、refinement round 和组件消融（§4–§5）。

## 8. 主要发现

- AgentLocate 在论文所测模型与设置中整体优于对照；Who&When Algorithm-Generated 上多数配置的 Agent 准确率超过 50%（§4.2、表1）。
- 三个 Evaluator 较一个明显提升，继续增加到五或七个没有稳定收益；一个 refinement round 基本形成主要收益（§4.2）。
- 晚期 verifier/retriever 容易因“症状更可见”被误判为根因，作者称之为 visibility bias（§5）。

## 9. 局限性

Evaluator 与 Judge 使用同一底层模型，置信度是模型自报；方法需要失败标签和微调数据。决定性步骤标签本身具有因果歧义，且基准规模、Agent 配置和错误分布限制外推（§3–§5）。

## 10. 可复现性信息

论文提供完整提示与超参数；文中写明代码将在接收后发布，但正文未给出可访问仓库地址。闭源 GPT-4o 微调会限制完全复现。

## 11. 与“智能体测试”研究的关系

把二元 pass/fail oracle 深化为“责任组件 + 最早决定步骤”的诊断 oracle，并显示根因和症状必须分离。

## 12. 可借鉴的工程实现

结构化 `(agent, step, evidence, confidence)` 输出、多视角复核、±1 step 容差、晚期症状偏差检查和成本感知升级路径。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `research/papers/2026-Xia-WhoBrokeTheSystem.pdf`，25 页。正文证据主要来自 §1、§3–§5。

## 14. 可支持的综述结论

多智能体归因不能只问“谁错了”，还应定位何时变得不可恢复，并校准 Judge 的同源偏差和症状偏差。
