# Agent 回归测试：核心论文与阅读路线

检索日期：2026-09-19。

## 核心判断

截至检索日，软件工程旗舰会议主赛道尚未出现一套成熟、完整的“LLM agent 版本 A→B 回归测试系统”。ASE 2026 的 Tangent 提供了最直接的实践需求证据，但不是方法论文。真正直接的方法主要是 2026 年预印本、系统论文或 workshop 工作。

## 第一梯队：直接解决 Agent 回归测试

1. **Chronicle: Cut-Point Replay for Regression Testing of LLM Agents**
   - 把生产事故轨迹固化为 CI regression fixture。
   - 冻结大部分非确定边界，只让修改过的 cut point 执行新代码。
   - 最适合研究“历史故障如何稳定复现”。

2. **AgentLens: Production-Assessed Trajectory Reviews for Coding Agent Evaluation**
   - 对 current version 与 anchor run 做 nightly trajectory diff。
   - 同时检查最终结果、指令遵从、工具调用、异常终止和成本。
   - 最接近生产环境的版本回归流水线。

3. **Layer-Isolated Evaluation**
   - 把 agent 拆成 ontology、routing、memory、safety 等层。
   - 每层建立 deterministic、no-LLM、baseline-locked CI gate。
   - 适合低成本定位是哪个确定性层发生了退化。

4. **AgentAssay**
   - 将随机 agent 的回归判定建模为统计假设检验。
   - 输出 PASS / FAIL / INCONCLUSIVE，并用 SPRT 自适应减少重复次数。
   - 最适合研究随机性、统计功效与测试成本。

5. **Test-Driven AI Agent Definition (TDAD)**
   - 把 prompt 当作由行为规格和测试“编译”出来的 artifact。
   - 在 spec v1→v2 演化时显式检查旧 invariant 是否保持。
   - 最适合研究需求演化和 prompt regression。

6. **Automated Structural Testing of LLM-Based Agents**
   - 使用 OpenTelemetry trace、LLM mocking 与结构化 assertion。
   - 把 test pyramid、TDD 和 regression testing 引入 agent 工程。
   - 是传统软件测试技术迁移到 agent 的重要基础。

7. **The Regression Tax**
   - 对同一任务成对比较 no-skill 与 skill-enabled agent。
   - 将净提升分解为 gain 与 regression，避免平均分掩盖“修好一些、弄坏另一些”。
   - 最适合研究 skill 更新导致的行为退化。

## 顶会与正式发表的近邻证据

- **Tangent，ASE 2026 Research Papers**：证明工业界确实在模型更新时做 continuous/regression evaluation，但没有提出新算法。
- **Continuous Benchmark Generation，LLM4Code@ICSE 2026**：自动更新企业 agent benchmark，解决测试集随需求过时的问题；不是 ICSE Research Track。
- **τ-bench，ICLR 2025**：用 `pass^k` 测量多次运行可靠性，为回归门禁提供 flakiness 基线。
- **Towards a Science of AI Agent Reliability，ICML 2026**：提供 consistency、robustness、predictability、safety 指标体系。
- **StableToolBench，Findings ACL 2024**：通过 API cache/simulator 控制环境漂移，避免把外部工具变化误判为 agent regression。

## 推荐研究方向

最值得做的是 **Version-Paired Causal Agent Regression Testing**：

1. 在相同任务、环境快照和随机配置下，成对运行 old/new agent；
2. 同时检查最终状态、工具副作用、轨迹不变量、安全、成本和时延；
3. 用多次运行和 paired statistical test 区分回归与普通 flakiness；
4. 记录 model、prompt、tool、memory、skill、environment 和 judge 版本；
5. 发现回归后逐轴替换组件，做反事实定位；
6. 将结果分成 gain、regression、persistent pass、persistent fail，而不只报告平均分变化；
7. 明确区分 agent regression、environment drift 和 oracle/judge drift。

## 完整报告

- [软件工程顶会与严格纳排报告](./2026-09-19-agent-regression-testing-top-venues.md)
- [广泛检索、方法体系与研究选题](./2026-09-19-agent-regression-testing-broad-review.md)
- [结构化检索原始结果](../../../searches/runs/2026-live-agent-regression/results.json)
