# SIRAJ：黑盒自动红队测试

**论文**：Kaiwen Zhou, Ahmed Elgohary, A S M Iftekhar, Amin Saied. *SIRAJ: Diverse and Efficient Red-Teaming for LLM Agents via Distilled Structured Reasoning*. Findings of EACL 2026, pp. 3269–3292. arXiv:2510.26037.

**全称**：Structured Iterative Reasoning for Agents safety Judgement。它面向任意黑盒 Agent，不要求源码或模型权重，只依赖 Agent 定义以及每次尝试产生的执行轨迹。

## 两阶段红队闭环

1. **多样化种子生成**
   - 从 Agent definition 出发，不只枚举粗粒度风险类别。
   - 将风险空间拆成三轴：细粒度 **risk outcome**、导致风险的 **tool-use trajectory**、风险来源（恶意用户或恶意环境）。
   - 由此生成覆盖不同危害结果和到达路径的 seed test cases。
2. **迭代攻击构造**
   - 执行种子并观察黑盒轨迹。
   - 根据前一次失败/接近成功的证据选择红队策略、改写测试，再次执行。
   - 轨迹因此既是待评价对象，也是下一轮攻击的反馈。

## Structured Reasoning Distillation

直接用大型推理模型做迭代红队成本很高。SIRAJ 把教师模型的红队推理组织成结构化字段，让较小模型学习“观察轨迹—诊断阻塞—选策略—生成下一次攻击”的过程，而非只蒸馏最终 prompt。论文报告蒸馏后的 8B red-teamer 比 671B DeepSeek-R1 更有效。

## 覆盖与预言机

- 覆盖不能只数安全类别；应同时测 **危害结果覆盖、工具调用轨迹覆盖、风险源覆盖**。
- 攻击成功要落到 Agent 的实际行为/工具轨迹，而非仅检查它是否输出了不安全文本。
- 黑盒并不意味着无反馈：完整的动作、工具调用和观察序列是高价值的灰度反馈，只是不读取内部实现。

## 主要结果

- 种子生成使风险结果和工具调用轨迹覆盖提升约 2–2.5 倍。
- 结构化蒸馏的 8B red-teamer 的攻击成功率提升 100%，并超过 DeepSeek-R1 671B。
- 消融实验支持三个组件的作用：多维种子空间、基于历史轨迹的迭代、结构化推理蒸馏。

## 与 ATA 的区别

- ATA 追求广义质量测试，利用源码、开发者访谈和文献；SIRAJ 专注安全红队，强调黑盒通用性。
- ATA 以弱点和难度闭环；SIRAJ 以危害结果、到达轨迹和风险源闭环。
- 可组合方式：ATA 负责系统建模和测试编排，SIRAJ 作为其中的安全测试生成器。

## 局限与实践建议

- 黑盒结果受轨迹可观测性影响；若工具输出或环境状态被隐藏，攻击诊断会变弱。
- LLM 生成的攻击与 Judge 可能带来模型家族偏差，必须保留规则/环境型安全预言机。
- 覆盖提升不等于真实风险分布；应按资产、权限和危害严重度给测试加权。
- 测试平台应保存每次攻击的父子关系、策略、轨迹差异和成功条件，才能复现迭代搜索过程。

