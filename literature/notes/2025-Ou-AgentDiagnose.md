# AgentDiagnose：全文阅读笔记

## 基本信息

- 标题：AgentDiagnose: An Open Toolkit for Diagnosing LLM Agent Trajectories
- 作者：Tianyue Ou、Wanyao Guo、Apurva Gandhi、Graham Neubig、Xiang Yue
- 版本：EMNLP 2025 System Demonstrations
- DOI：10.18653/v1/2025.emnlp-demos.15
- 证据等级：已阅读全文；DOI/题名双源一致，OpenAlex 存在作者名变体

## 方法

工具包含可扩展的轨迹 evaluator 和可视化模块。示例 evaluator 覆盖回溯与探索、任务分解、观察读取、自我验证和目标质量；可视化包括动作语义嵌入、词云和状态转移时间线。

## 验证与指标

- 在 30 条人工标注轨迹上，以 Pearson、Spearman 和 Kendall 相关系数比较自动评分与人工评分。
- 不同维度相关性差异较大，任务分解最高，回溯与探索最低。
- 用评分筛选 NNetNav-Live 训练子集，并在 WebArena 上比较下游效果。

## 对 Agent 测试的价值

它提供了比最终 pass/fail 更细的诊断视图，也展示了如何把轨迹质量信号用于数据筛选。最合适的定位是可扩展的诊断工具，而非已经充分验证的通用 oracle。

## 局限

- 人工验证仅 30 条轨迹，不能支撑跨领域稳定性结论。
- 若系统不暴露推理文本，部分 evaluator 无法直接使用。
- LLM 评分提示、领域和轨迹格式变化可能造成测量漂移，需要独立回归集。

