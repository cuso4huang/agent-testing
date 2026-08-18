# Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems

## 1. 基本信息

- 作者：Mengzhuo Chen; Junjie Wang; Fangwen Mu; Yawen Wang; Zhe Liu; Huanxiang Feng; Qing Wang
- 年份/版本：ACL 2026 Long Paper
- DOI：10.18653/v1/2026.acl-long.912（Crossref/OpenAlex 一致核验）
- 代码/数据：https://github.com/TraceElephant/TraceElephant

## 2. 研究问题

部分可观测的 output-only trace 是否足以评价故障归因，以及完整输入、工具状态和可重放环境能带来多少诊断收益（摘要、§1）。

## 3. 被测试的智能体类型

Captain-Agent、Magentic-One 和 SWE-Agent，覆盖动态团队、固定多 Agent orchestration 与具有多个功能组件的单 Agent scaffold（§3.1）。

## 4. 测试或评估方法

TraceElephant 通过 LLM API middleware 捕获请求、响应、工具交互、输入上下文、Agent 配置和架构；比较完整 trace、移除 metadata/input 的静态设置，以及带局部 counterfactual replay 的动态设置（§3、附录 A.6）。

## 5. 数据集、环境或基准

从 GAIA、AssistantBench、SWE-Bench 收集 380 条轨迹，其中 220 条失败；每条失败轨迹标注责任组件和决定性步骤，并附可复现执行环境（§3.1、表1）。

## 6. 评价指标

Agent-level accuracy、exact step accuracy、固定容差 step accuracy；结果在三次独立运行上平均（附录 A.6.1）。

## 7. 实验设计

三名有 MAS 开发经验的标注者先独立标注，再对不确定案例协商一致；首轮 Krippendorff’s alpha 为 Agent 0.72、Step 0.64。比较 all-at-once、step-by-step、binary search、静态 agentic 与动态重放方法（§3.4、附录 A.5–A.6）。

## 8. 主要发现

- 完整 trace 相比 output-only 设置，Agent 归因平均提高 22%，Step 归因提高 76%；可运行环境使 Step accuracy 进一步提高约 10%（§1、§4）。
- 对 Who&When 的复查显示至少 21% 案例因缺少输入而无法可靠归因（§1）。
- Step-level 归因比 Agent-level 对缺失信息更敏感，且结果会随架构、Agent 类型和步骤位置变化（§4）。

## 9. 局限性

只覆盖三个系统和三类公开任务；完整 trace 在真实系统可能涉及隐私、专有提示和密钥。动态 replay 仅观察后续 3 步，验证的是局部责任而非全局因果充分性；若无 reference answer，oracle 仍更困难（附录 A.6、A.8）。

## 10. 可复现性信息

ACL 正式开放全文；仓库提供 trace、标注与执行材料。论文给出统一 JSON schema、采集 middleware、标注协议、模型设置和许可证（§3、附录 A.5–A.10）。

## 11. 与“智能体测试”研究的关系

直接证明 observability 是评测有效性的一部分：不同 trace 可见度会改变归因结果，benchmark 必须报告观察边界。

## 12. 可借鉴的工程实现

developer-facing full trace、输入/metadata 消融、可重放环境、专家共识标注、隐私过滤和局部 counterfactual debugger。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `research/papers/2026-Chen-SeeingWholeElephant.pdf`，ACL 页码 19888–19905，共 18 页。

## 14. 可支持的综述结论

故障归因 benchmark 的结果不能脱离可观测性解释；output-only trace 会系统性隐藏根因，而全量 trace 又引出隐私和最小必要记录问题。
