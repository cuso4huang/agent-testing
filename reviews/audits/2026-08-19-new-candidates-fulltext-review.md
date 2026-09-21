# 新增候选全文评审：harness、长期状态与技能差分失效

评审日期：2026-08-19

## 1. Agent Skills Can Be Harmful

### 身份与证据

- 题名：*Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents*
- 作者：Gen Dong 等
- 版本：arXiv `2608.11888v1`，2026-08-12
- 证据等级：已检查全文；预印本，未按同行评审论文处理

### 测试机制

该工作把技能加载视为一个可控变量，采用受差分测试启发的配对设计。目标运行与参考运行固定任务、verifier、Agent 框架、模型、仓库或容器状态和输入数据，只改变技能配置。参考运行可以是不加载技能，也可以加载语义相近的另一技能。

- 功能失效：目标运行失败、参考运行通过；
- 效率回归：两者都通过，但目标运行的 token 与时间均增加，且至少一项超过主要阈值 `T=2.0`；
- 参考运行是 pseudo-oracle，只说明相同任务在另一技能条件下可完成或可更便宜完成，不代表唯一正确解。

研究基于 SkillsBench 与 SWE-Skills-Bench，并从公开技能站点补充语义匹配技能，把潜在配对空间从 826 扩展到 20,664。执行使用 OpenCode 1.15.1 与 Claude Opus 4.6；经过自动筛选、去除证据不足/窄 verifier/重复案例及人工共识标注，形成 307 个确认案例：125 个功能失效和 182 个高置信效率回归。

### 可用于 PPT 的结论

- “可复用知识”本身也是回归变量；同一个任务可以通过有/无技能或不同技能的配对执行定位回归。
- 125 个功能失效中，Task-Implementation Fault 为 86 个；182 个效率回归中，Excessive Procedure 为 114 个，其中 excessive verification 为 67 个、heavy implementation pipeline 为 30 个。
- 自动归因工具 SkillTriage 对功能失效 exact root cause 与人工标签一致 111/125；对效率回归为 132/182。该数字是论文特定 taxonomy 和实验设置下的结果，不能泛化为通用根因定位精度。

### 局限

单一 Agent runtime 与单一前沿模型；任务集中在两个 benchmark；差分设计仍受 Agent 随机性影响；根因标签包含人工判断；参考运行只提供归因证据而非因果唯一性。适合作为“差分回归和可复用组件测试”的前沿案例，不宜作为成熟路线唯一锚点。

## 2. MEMPROBE

### 身份与证据

- 题名：*MEMPROBE: Probing Long-Term Agent Memory via Hidden User-State Recovery*
- 作者：Enze Ma 等
- 版本：arXiv `2606.24595v1`，2026
- 证据等级：已检查全文；预印本

### 测试机制

MEMPROBE 不再仅从未来回答间接判断记忆质量，而把交互结束后留下的 memory artifact 当成可审计对象。50 个模拟用户各有 31 个隐藏状态维度，共 1,550 个恢复目标；Agent 先完成一系列避免直接泄漏目标的帮助任务，再由恢复流程从最终记忆中重建隐藏用户状态。

它区分两种访问模式：

- `dump_all`：查看完整存储，测试证据是否被保留；
- `top-k`：只通过正常检索接口取得前 5 项，测试证据是否在运行预算内可访问。

失败归因进一步区分 Memory、Task、Agent 和 User simulator 环节，避免把所有缺失都归咎于记忆系统。

### 可用于 PPT 的结论

- 五种设置的即时任务完成率均接近饱和（99.87%–99.94%），但完整存储的类别平衡恢复分数只有 0.611–0.624，top-k 后进一步降至 0.473–0.540。
- 完整存储最强的系统不一定在正常检索模式最强，说明“保留了证据”和“运行时能取回证据”是不同测试性质。
- 该案例非常适合说明：终态成功之外，还要检查跨会话状态产物、写入、抽象、更新和可检索性。

### 局限

使用美国背景的合成用户、生成任务、受控对话 scaffold 和多个 LLM judge；任务本身较容易；judge 非人类金标且可能受槽位措辞影响。作者只进行小规模人工审计，失败归因人工一致为 90/120。适合作为长期状态测试的前沿补充案例，不宜在 PPT 中宣称已经解决真实用户记忆测试。

## 3. Understanding Agent-Reactive Bugs at the Model-Harness Boundary

### 身份与证据

- 题名：*Understanding Agent-Reactive Bugs at the Model-Harness Boundary: An Empirical Study of LLM Agent Issue Reports*
- 作者：论文首页作者信息见本地 PDF
- 版本：arXiv `2607.15684v1`，2026
- 证据等级：已检查全文；预印本

### 研究机制

论文定义 Agent-Reactive bug：失败表现依赖某种具体 LLM 行为以及 harness 对该行为的处理，两者缺一不可。研究抓取 Codex、Gemini CLI、LangChain 和 CrewAI 的 32,373 条 issue，经 bug、LLM 可达性和社区参与度筛选后，对 3,037 条进行人工分析，确认 255 个 AR bugs。两位标注者先共同开放编码 5%，再分工标注并讨论解决冲突。

研究从三个方面编码：用户看到的症状、触发失败的 LLM 行为、以及开发者讨论中的修复目标。共归纳 5 类症状和 8 类触发行为。

### 可用于 PPT 的结论

- Agent 的被测对象不是“模型输出”或“框架代码”二选一，而是模型—harness 交互边界。
- 症状包括 silent error、crash、error in output、retry loop 和 hang；只检查最终文本会漏掉伪造工具执行、状态错误和循环。
- 回归复现不应只重放用户 prompt，还应保存或 mock 特定模型行为、工具参数、模板破坏消息和长上下文状态。

### 局限

只覆盖四个公开项目；issue 记录可能不完整；症状、触发行为和修复目标均包含人工推断；闭源 Agent 缺少公开 issue 和 harness 代码。它更适合作为“测试对象为什么必须扩展到 harness”的实证动机，而不是一种完整自动化测试方法。

## 4. 对锚点选择的影响

- **Agent Skills Can Be Harmful**：进入补充案例矩阵，或作为“诊断与回归”页的小案例；其差分设计很强，但仍是新预印本。
- **MEMPROBE**：进入“跨会话状态测试”补充案例；如果 PPT 希望突出长期 Agent，可替换一个安全类案例成为锚点。
- **Agent-Reactive Bugs**：作为开场问题证据或“测试对象”页实证，不单独占用锚点页。

三篇论文共同说明：Agent Testing 不能只围绕 benchmark 排名。它还应控制可复用组件、检查持久化状态产物，并覆盖模型—harness 边界。
