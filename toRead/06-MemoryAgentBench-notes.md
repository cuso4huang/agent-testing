# MemoryAgentBench：有状态、长期记忆测试

**论文**：Yuanzhe Hu, Yu Wang, Julian McAuley. *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*. ICLR 2026. arXiv:2507.05257v4.

**关键区分**：长上下文模型一次读完整材料，不等于有记忆的 Agent。记忆 Agent 会在交互中逐步吸收信息、压缩、更新、推断和检索；测试也必须按时间顺序增量注入，而不是把历史一次塞入 prompt。

## 四种核心记忆能力

1. **Accurate Retrieval（AR）**：给定查询，找回正确片段，包括单跳和多跳。
2. **Test-Time Learning（TTL）**：部署时从历史中学会新规则/技能，无需参数训练。
3. **Long-Range Understanding（LRU）**：整合分散在 100K+ token 历史中的信息，形成全局理解。
4. **Selective Forgetting（SF）**：遇到冲突或更新时修订、覆盖或删除旧事实。

这四类不能用一个“记忆问答准确率”替代：检索强不代表能学规则，保留多不代表会正确忘记。

## Benchmark 构造

- 共 2,071 个问题，历史深度约 103K–1.44M token。
- 将既有长上下文数据切分为多轮、按时间顺序逐块喂给 Agent。
- 新建 **EventQA**：从超长叙事中检索和组合角色事件，强调 AR。
- 新建 **FactConsolidation-SH/MH**：新旧事实冲突后做单跳/多跳判断，强调 SF。
- TTL 包含多类分类与推荐任务；LRU 包含摘要和侦探式全局推理。
- 统一比较三类系统：完整长上下文（LCA）、RAG、带外部记忆/工具的 agentic memory。

## 实验结论

- 没有一种方法同时掌握四项能力。
- 长上下文 Agent 在 TTL 和 LRU 上最好，因为这些任务需要吸收大量分散证据或规则。
- RAG 在直接检索类任务上有优势，但 top-k 机制会丢失全局信息，对模糊查询、多跳和长期理解较弱。
- 更强 backbone 对简单 RAG 的边际收益有限，瓶颈常在记忆机制；对复杂 agentic memory，强推理模型仍能带来提升。
- FactConsolidation 的低分并非数据不可解：强推理模型在短/完整证据条件下可获得高分，说明长期状态更新与多跳整合才是难点。

## 如何设计有状态测试

- 每个测试明确事件时间、注入轮次、查询轮次、允许保留的信息和必须遗忘的信息。
- 记录 memory write、update、delete、retrieve 的可观测事件，而不只看最后答案。
- 同一事实设计 `建立 -> 强化 -> 冲突 -> 撤销/覆盖 -> 再查询` 生命周期。
- 做 reset 隔离测试，区分任务内、会话内、用户级和全局记忆，防止跨用户泄漏。
- 同时记录准确率、陈旧信息命中率、冲突解析率、压缩率、存取成本和随历史长度的退化曲线。

## 局限

- 主要是文本记忆，未充分覆盖图像、文件、工具状态等多模态/环境记忆。
- 基于既有数据重构的对话不完全等同真实用户长期互动。
- 最终问答分数仍不能完整揭示写入、压缩和检索过程中的错误；需要结合 process evaluation。

