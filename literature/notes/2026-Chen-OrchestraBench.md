# OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality

## 1. 基本信息

- 作者：Yidian Chen; Yingzi Gu; Natan Vidra; Spurthi Setty; Sharon Zheng
- 年份/版本：2026，arXiv:2608.05263v1，预印本，无正式 DOI
- 身份核验：arXiv 与 OpenAlex 精确匹配；Crossref 返回的是无关论文，未采纳。

## 2. 研究问题

怎样超越团队总正确率，分别测量多智能体 orchestration 的路由、故障恢复、级联传播和任务分解质量（摘要、§1）。

## 3. 被测试的智能体类型

模板化企业工作流中的多智能体 orchestration pipeline，并辅以真实 Claude Agent 的可验证算术依赖链机制实验（§3–§5）。

## 4. 测试或评估方法

- 使用 seed 可复现的故障注入 harness，对 MAST 故障模式实施受控注错。
- 比较 surface flag router、intent-reasoning router 与 oracle，并测试 blind retry 和 trusted-state repair。
- 按 pipeline depth 扩展依赖链，观察故障传播半径（§4–§5）。

## 5. 数据集、环境或基准

26 条带金标的路由诊断案例，以及深度 3–7 的可验证算术链；部分机制结果还换成 loan-approval 叙事并比较 Claude Sonnet、Opus、Haiku（§5.1–§5.4）。

## 6. 评价指标

路由准确率、按故障类型恢复率、cascade radius、time to detection、分解质量，以及配对检验和 bootstrap 置信区间（§4、§5）。

## 7. 实验设计

四组实验分别比较路由策略、故障注入与恢复、传播深度和分解质量；对关键结论进行模型与叙事改写检查，并用 trusted-state 消融区分自主检测与外部提示贡献（§5）。

## 8. 主要发现

- 误导或缺失 surface flag 时，关键词路由器在 26 条诊断集的 adversarial 案例为 0%，intent router 为 100% 并匹配 oracle（§5.1）。
- 工具故障完全恢复，模糊委派部分恢复，若干潜伏或语义故障不恢复；blind retry 会重现潜伏故障（§5.2）。
- pipeline 深度从 3 增至 7 时，平均 cascade radius 从 0.9 增至 4.7（§5.3）。
- trusted-state 消融表明部分“遏制”收益来自可信状态信号，而非 Agent 自主检测（§5.4）。

## 9. 局限性

主要结果是小规模、可验证依赖链上的机制探针，不应外推为真实企业 workload 结论；工作流规模、领域复杂度和真实生产故障分布仍有限（§7 Limitations）。

## 10. 可复现性信息

论文描述 seed 控制、模板化 workflow、注错 harness、配对统计与模型配置；未在正文中发现明确公开代码地址。

## 11. 与“智能体测试”研究的关系

把 recovery、cascade 和 decomposition 从附属分析提升为一等测试目标，适合作为多智能体回归与故障传播测试的指标模板。

## 12. 可借鉴的工程实现

确定性依赖链 oracle、故障模式分层、cascade radius、trusted-state 消融、失败重试策略对照和 seed 固定。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `literature/papers/2026-Chen-OrchestraBench.pdf`，8 页。

## 14. 可支持的综述结论

多智能体测试需要区分“发现、归因、恢复和遏制”；团队最终成功率不能说明故障从哪里开始、传播多远以及恢复是否依赖外部真值。
