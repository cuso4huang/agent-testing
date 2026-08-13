# Tool Selection Prompt Injection：工具选择测试

**论文**：Jiawen Shi et al. *Prompt Injection Attack to Tool Selection in LLM Agents*. NDSS 2026. DOI: 10.14722/ndss.2026.230675.

**攻击名**：ToolHijacker。目标不是篡改一次工具调用的参数，而是在工具库中注入一份恶意工具文档，使 Agent 对攻击者指定的目标任务持续选择恶意工具。

## 被攻击的两阶段选择链

常见大工具库不会把所有 schema 都放进上下文，而是：

1. **Retrieval**：用任务描述从工具文档库召回 top-k。
2. **Selection**：LLM 在召回候选中决定调用哪个工具。

因此测试工具选择时不能只测最后的 LLM selection；恶意文档可能先通过语义优化挤进 top-k，再通过指令/描述操纵最终选择。

## ToolHijacker 的优化目标

恶意文档同时优化两类目标：

- **R（retrieval objective）**：与目标任务在嵌入空间足够接近，提高召回命中率。
- **S（selection objective）**：进入候选后，让目标 LLM 更倾向选择恶意工具。

论文实现两条路径：

- **Gradient-free**：由攻击者 LLM 在句子级生成/筛选变体，语义自然、对闭源模型迁移更好。
- **Gradient-based**：在可微 shadow 模型上做 token 级优化，并加入语义/困惑度约束。

使用 shadow retriever、shadow task descriptions 和 shadow LLM，体现的是现实的 no-box 场景：不知道目标 Agent 的模型、检索器和内部参数。

## 指标

- **AHR（Attack Hit Rate）**：恶意工具文档是否进入检索候选。
- **ASR（Attack Success Rate）**：Agent 最终是否为目标任务选择恶意工具。
- 还要测非目标任务上的命中/成功，以检查攻击是否具有目标特异性，而非无差别劫持。

## 主要结果

- 两种方法跨 8 个目标 LLM、MetaTool 与 ToolBench 均取得高成功率；在多种检索器实验中，gradient-free 达到 100% AHR、99% ASR，gradient-based 在开源检索器上 100% ASR、闭源 embedding 上约 95%。
- 非目标任务上的 ASR 接近零，说明恶意文档可针对特定任务。
- 手工 prompt injection、JudgeDeceiver、PoisonedRAG 等基线明显更弱，因为没有同时为 retrieval 与 selection 优化。
- StruQ、SecAlign、已知答案检测、DataSentinel 和困惑度检测仍漏掉大量攻击；句子级 gradient-free 文档尤其像正常工具说明。

## 应怎样测工具选择

建立一个三层 test oracle：

1. **检索正确性**：gold tool 是否进入 top-k；不可信工具是否因描述污染异常上升。
2. **选择正确性**：给定候选集合，最终选择是否满足任务和权限。
3. **执行安全性**：即使选错，能力系统是否阻止越权/敏感动作。

再做四类变异：

- 同义改写任务描述，检查选择稳定性。
- 注入语义高度相似但权限/来源不同的工具文档。
- 改变 k、工具池规模、检索器和候选顺序。
- 用目标任务与非目标任务做差分，识别定向后门式选择偏差。

## 局限与防御含义

- 论文证明自然语言层防御不够；工具文档应视为供应链代码，而非普通文本。
- 测试聚焦“选哪个工具”，尚未联合优化工具参数和多步调用链；应与 Les Dissonances 一起阅读。
- 最可靠的缓解不只是检测恶意描述，还包括可信来源、签名、权限隔离、allowlist、用户确认及执行时策略。

