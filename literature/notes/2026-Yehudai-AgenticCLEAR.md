# Agentic CLEAR：全文阅读笔记

## 基本信息

- 标题：Agentic CLEAR: Automating Multi-Level Evaluation of LLM Agents
- 作者：Asaf Yehudai、Lilach Eden、Michal Shmueli-Scheuer
- 版本：ACL 2026 System Demonstrations
- DOI：10.18653/v1/2026.acl-demo.74
- 证据等级：已阅读全文；Crossref 与 OpenAlex DOI/题名一致

## 研究问题与方法

Agentic CLEAR 位于可观测性层之上，自动为轨迹生成任务相关 rubric，并在 node、trace、system 三个层级生成诊断和聚合问题。它试图减少逐条人工读 trace 的成本，并避免只用单一全轨迹提示打分。

## 测试对象、Oracle 与指标

- 对象：AppWorld、GAIA、SWE-bench Verified Mini、τ-bench 等环境中的多种 Agent/模型组合。
- 判定：LLM 生成 rubric、节点/轨迹评分、跨轨迹问题聚合。
- 元评测：与人工标注错误对齐，报告 macro/micro F1；以 AUC 检查分数预测任务成功的能力。

## 主要贡献

方法把“哪一步发生了什么问题”和“系统反复出现什么问题”连接起来，适合作为回归分析与失败聚类的上层评测组件。论文也显示不同 benchmark、Agent 架构与 Judge 上的效果不一致，因此不能把聚合诊断当作统一金标准。

## 局限

- 依赖 LLM Judge，可能继承同源模型偏差与 rubric 漂移。
- 某些 benchmark 内部状态和原生判定信息不可见，影响生成 rubric 的完整性。
- 更适合作为诊断与候选问题发现层；可执行状态、安全不变量仍应由确定性 oracle 判定。

