# Plan-RewardBench：全文阅读笔记

## 基本信息

- 标题：Aligning Agents via Planning: A Benchmark for Trajectory-Level Reward Modeling
- 作者：Jiaxuan Wang 等
- 版本：ACL 2026 Long Paper
- DOI：10.18653/v1/2026.acl-long.1062
- 证据等级：已阅读全文；Crossref 与 OpenAlex DOI/题名一致

## 研究问题与方法

论文元评测 reward model 和 LLM Judge 能否在长轨迹中区分较优与干扰轨迹。Plan-RewardBench 覆盖安全拒绝、工具无关/不可用、复杂规划和错误恢复，并结合自然 rollout、规则扰动和最小编辑扰动构造 hard negative。

## Oracle 与指标

- 输入包含工具 registry、多轮对话和完整交错轨迹，环境状态与用户意图在轨迹对内固定。
- 采用 pairwise accuracy 和 macro average；检查轨迹长度、任务难度及顺序交换带来的偏差。
- 标签使用多模型 panel、meta-review 与分层人工审计；人工一致性按场景报告 Cohen's kappa。

## 对 Agent 测试的价值

该工作不是普通规划能力榜单，而是对轨迹评测器进行压力测试，并提供可复用的 hard-negative 构造方法。它补足了长轨迹、工具错误恢复和表面线索偏差等 evaluator 测试维度。

## 局限

- 当前数据为文本工具轨迹，尚不能代表 GUI、具身或隐式状态环境。
- 多数标签来自模型 panel，人工审计不是全量标签。
- 四类场景分布不均，整体 macro 指标仍受任务构成影响。

