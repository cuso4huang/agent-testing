# 智能体轨迹（Agent Trajectory）表征调研

> 调研日期：2026-09-20（Asia/Shanghai）  
> 范围：LLM agents、tool-use agents、web/GUI agents、具身 agents；重点考察轨迹的存储、训练、记忆和评测表征。

## 结论先行

现在没有一个统一的“智能体轨迹标准格式”。研究与工程实践正在形成一个分层共识：

1. **底层保留可回放的时间序列**：任务/用户输入 → 观察 → 思考或决策上下文 → 动作/工具调用 → 工具结果或环境反馈，循环到结束。
2. **中层把每一步变成类型化事件**：工具名、参数、返回值、错误、状态变化、依赖关系、时间和执行元数据都单独记录，而不是只保存一段拼接文本。
3. **上层按用途做派生表征**：成功/失败标签、步骤级正确性、反思文本、经验规则、可执行技能、摘要、向量索引、搜索树或因果图。
4. **表示越来越面向“可验证过程”**：评测不再只问最终答案对不对，而是检查工具选得对不对、参数对不对、顺序和依赖对不对、哪一步首次出错、错误是否传播。

可以用下面这个统一抽象理解当前文献：

```text
τ = (goal, context_0, x_1, x_2, ..., x_T, outcome)

x_t = (
  observation_t,          # 环境/工具/用户提供给 agent 的信息
  reasoning_t?,           # 可选的显式 reasoning/thought/plan
  action_t,               # 工具调用、GUI 操作、代码、消息或 finish
  result_t,               # 返回值、页面变化、截图、错误、用户反馈
  reward_or_label_t?,     # 步骤级或轨迹级信号
  metadata_t               # 时间、成本、token、权限、agent_id、父步骤等
)
```

这里的 `reasoning_t` 是论文或日志中的“显式推理字段”，不等价于模型不可见的内部 hidden state；在生产系统中通常应允许省略、脱敏或只保存摘要。

## 1. 检索范围与方法

- 数据库/来源：arXiv、OpenReview/ICLR、NeurIPS Proceedings、ACL Anthology、AAAI、Crossref、OpenAlex，以及论文官方代码/数据页。
- 检索词：`LLM agent trajectory`、`language agent trajectory learning`、`agent trajectory compression memory`、`tool use trajectory language model`，并对关键论文做题名核验。
- 纳入标准：论文明确涉及轨迹的结构、采集、训练、压缩、记忆、搜索、步骤级评价或轨迹级奖励。
- 证据规则：优先阅读论文原文；仅依据摘要的工作标为“摘要级证据”。引用数仅作检索信号，不能作为论文质量分数。
- Semantic Scholar 本次 API 触发了速率限制，因此引用数主要采用 OpenAlex 的快照；不同数据库的数字会不同。

## 2. 轨迹表征的五个层次

| 层次 | 典型形式 | 代表工作 | 主要用途 |
|---|---|---|---|
| 线性事件序列 | `thought → action → observation` 或 message 列表 | ReAct、AgentTuning、AgentProcessBench | prompt/in-context、SFT、回放 |
| 类型化动作记录 | `(tool, arguments) → result/error`；`(target element, operation)` | Toolformer、ToolLLM、Mind2Web | 工具学习、执行、格式校验 |
| 环境状态/模态记录 | 文本、JSON、DOM、accessibility tree、截图、代码状态 | WebArena、Mind2Web、OS agents、Voyager | 状态建模与真实环境交互 |
| 分支结构 | 搜索树、工具依赖图、并行集合、因果图 | ToolLLM DFSDT、TRAJECT-Bench、AgentTrace | 多路径探索、依赖分析、根因定位 |
| 语义/记忆抽象 | 反思、经验规则、技能代码、摘要、向量 embedding | Reflexion、ExpeL、Voyager、ACON | 长期记忆、跨任务迁移、上下文压缩 |

关键变化是：**线性序列仍是原始事实层，但已经不再是唯一的研究对象**。

### 2.1 线性序列：最常见的“原始轨迹”

ReAct 把轨迹明确写成交替的 reasoning/action/observation 步骤：在每一步根据历史观察决定动作，动作得到环境反馈后再继续。它还把 thought 视为不改变环境、但会更新上下文的语言动作。这个格式适合 few-shot、SFT 和人工诊断。

Toolformer 将工具调用更严格地线性化为带特殊标记的序列：

```text
<API> api_name(input) → response </API>
```

模型学习何时调用、调用哪个 API、填什么参数，以及结果是否有助于后续 token 预测。它更像“语言模型中的可执行插槽”，而不是完整环境轨迹。

AgentTuning 则把完整交互记录成多轮对话，并为每个动作附带 thought；最后给整条轨迹一个任务级 reward，用于过滤高质量轨迹。AgentProcessBench 延续了 message 序列，但把每个 assistant step 单独拿出来做步骤级标注。

### 2.2 类型化动作：从自然语言日志走向可执行记录

ToolLLM 的动作格式是：

```text
Thought: ...
API Name: ...
Parameters: {...}
Observation: {...}
```

每个 API 都有工具名、描述、参数 schema、响应示例；轨迹是带真实 API 返回值的多轮调用链。它还显式保留 `Finish with Final Answer` 和 `Finish by Giving Up` 两种终止动作。

Mind2Web 把网页轨迹中的每一步定义成 `(Target Element, Operation)`，其中 operation 包括 Click、Type、Select Option 等，另外保存网页快照、DOM、网络 HAR 和完整 trace。这样轨迹不是“点击了第几个按钮”的文字，而是“在当前页面状态下，对哪个元素执行什么操作”。

### 2.3 状态与观察：轨迹不只记录 agent 做了什么

WebArena 把环境形式化为 `E = <S, A, O, T>`，并明确区分隐藏状态 `S`、动作空间 `A` 和观察空间 `O`。网页观察可以是：

- URL、tab 和页面内容；
- 原始 HTML/DOM；
- screenshot/RGB array；
- accessibility tree（角色、文本和可交互属性）。

这说明一个重要问题：**同一个动作序列，在不同观察和初始状态下不是同一条轨迹**。因此做数据集或线上 trace 时，最好同时记录“agent 看到了什么”和“环境真实变成了什么”；只存模型输出会丢掉最关键的因果信息。

具身 agent 中，Voyager 进一步把 observation 结构化为 inventory、equipment、附近实体、biome、时间、生命值等，并把可复用行为表示成 executable code。代码在这里不是普通回答，而是一个可组合、可复用、带时间跨度的 action representation。

### 2.4 搜索树与图：轨迹不一定是一条链

ToolLLM 发现单条 ReAct 链容易因早期错误而陷入循环，于是用 depth-first search-based decision tree 保存多个 reasoning path；每个节点包含 thought、API 调用和真实响应，失败分支可以放弃后继续探索。

TRAJECT-Bench 把工具轨迹区分为两类：

- **parallel**：多个工具调用彼此独立，是无序的调用集合；
- **sequential**：后一个工具的参数依赖前一个工具的输出，并显式记录参数绑定。

它的顺序轨迹实际上已经接近一个带数据依赖的有向图，而不是普通字符串。2026 年的 AgentTrace 更进一步，尝试从执行日志重建多智能体工作流的因果图，用于从最终错误反向定位根因；这是新兴方向，尚未形成统一 schema。

### 2.5 记忆抽象：从“保存轨迹”到“保存经验”

当前文献中最清晰的演化路线是：

```text
raw trajectory  →  reflection/correction  →  experience/skill abstraction
```

- **Reflexion**：短期记忆保留当前 trial 的完整轨迹；长期记忆保存基于 reward 和失败原因生成的 verbal reflection。
- **ExpeL**：把成功/失败轨迹放入 experience pool，按任务相似度检索成功轨迹，并跨任务抽取可迁移 insights；其实现使用 embedding + kNN。
- **Voyager**：把成功行为抽象成带描述的 executable skill，使用向量数据库按任务和环境状态检索，并组合简单技能解决复杂任务。
- **ACON**：不再把完整 history 永久塞进 context，而是对 interaction history 与 latest observation 做选择性压缩；压缩器通过“成功未压缩轨迹 vs 压缩后失败轨迹”的差异学习保留哪些状态、变量、因果关系和决策线索。

2026 年的综述把这一演化概括为 Storage（轨迹保存）、Reflection（轨迹修正）和 Experience（跨轨迹抽象），这比简单区分 short-term/long-term memory 更能解释当前研究方向。

## 3. 训练和评测正在如何使用这些表征

### 3.1 训练：从 token imitation 到执行反馈

当前有四种常见训练对象：

1. **全轨迹 token imitation**：输入任务，模仿 thought/action/observation 序列；AgentTuning、ToolLLM 属于这一类。
2. **动作/工具调用监督**：只监督 tool name、参数、元素选择或下一步 action；Mind2Web 的动作预测是典型例子。
3. **轨迹级 reward/preference**：整条轨迹只有成功/失败或优劣标签，简单但 credit assignment 粗糙。
4. **步骤级 process supervision**：每一步标为正确、无效/探索、错误，或为候选动作提供 process reward。AgentProcessBench 使用 `+1/0/-1`；ToolPRMBench 将每个案例构造成“交互历史 + 正确动作 + plausible wrong action + tool metadata”；Plan-RewardBench 比较 preferred trajectory 与 hard negative trajectory。

因此，轨迹表征的粒度正在从“整条 episode 一个 label”向“每个 assistant/tool step 一个 label”移动。

### 3.2 评测：最终答案之外的轨迹指标

TRAJECT-Bench 明确给出四类 trajectory-aware 指标：

- **Trajectory Exact Match**：工具名/调用序列是否完全一致；
- **Trajectory Inclusion**：所需工具是否被调用；
- **Tool Usage**：参数 schema、格式和值是否正确；
- **Trajectory Satisfy**：在没有唯一 gold path 时，用 judge 判断这条轨迹是否足以完成任务。

AgentProcessBench 则关注步骤质量和首错位置，特别引入 neutral/exploratory 标签，避免把必要的试探动作都当成错误；它还用 error-propagation rule 标记由首个错误导致的后续依赖步骤。

这两类工作共同说明：**复杂 agent 的“正确性”不是路径复现，而是约束满足 + 环境结果 + 过程质量**。WebArena 也因此优先用环境最终状态验证功能正确性，而不是简单比较 action string，因为同一个目标通常存在多条合法路径。

## 4. 当前比较稳妥的工程表征

如果你要为自己的 agent 设计轨迹数据，建议采用“原始事件层 + 派生视图层”，不要只存一条 prompt 字符串：

```json
{
  "trace_id": "run-20260920-001",
  "task": {"id": "...", "instruction": "..."},
  "environment": {"type": "api|web|gui|code|embodied", "version": "..."},
  "initial_state": "可序列化状态或快照引用",
  "steps": [
    {
      "t": 1,
      "actor": "agent|user|tool|environment",
      "observation": {"type": "text|json|dom|a11y|image|state", "payload": "..."},
      "reasoning_summary": "可选；建议保存摘要而非原始隐式 CoT",
      "action": {"type": "tool_call|gui|code|message|finish", "tool": "...", "arguments": {}},
      "result": {"status": "ok|error|timeout|blocked", "payload": "..."},
      "parent_step_ids": [],
      "cost": {"latency_ms": 0, "input_tokens": 0, "output_tokens": 0}
    }
  ],
  "outcome": {"success": true, "reward": 1.0, "final_state": "..."},
  "derived": {
    "first_error_step": null,
    "step_labels": [],
    "trajectory_summary": "...",
    "reflection": "...",
    "skill_ids": [],
    "embedding_id": "..."
  }
}
```

最低限应保证：

- 每一步有唯一 id/timestamp，能重放或定位；
- 明确区分 observation、action、result，不能把 tool response 和 agent text 混成一段；
- 保存 tool schema/version、参数和错误；
- 保存依赖关系或 parent step，支持链、并行和分支；
- 保存任务级 outcome 与步骤级标签；
- 对 reasoning 做可选、可脱敏设计；
- 原始事实与 LLM 派生摘要分层保存，避免摘要覆盖原始 trace。

## 5. 研究空白与判断

1. **还没有跨环境通用 schema**：API、网页、GUI、代码执行和具身环境的 observation/action 差异很大。
2. **状态不等于观察**：很多数据只记录模型看到的文本，没有记录真实环境状态、外部副作用和状态变化。
3. **“可行路径”不等于“gold path”**：WebArena 和 ToolLLM 都说明一个任务通常有多条合法轨迹；单纯 exact-match 会误罚合理解法。
4. **credit assignment 仍是瓶颈**：最终失败到底归因于哪一个早期 tool call、参数还是错误理解，仍缺少稳定的因果标注。
5. **压缩会损失状态与因果关系**：ACON 的结果说明长轨迹必须压缩，但“哪些信息绝不能丢”强依赖环境和任务。
6. **从单轨迹到跨轨迹泛化仍不充分**：反思可以修正一次失败，但经验、技能和参数化策略能否迁移到新任务，仍缺乏统一 benchmark。
7. **可观测性与隐私/安全存在张力**：完整 trace 可能包含用户数据、密钥、网页内容和敏感操作，实际系统需要原始日志、脱敏日志和训练数据分层。

我的判断是：近期最有前景的路线不是寻找一个“万能 embedding”，而是构建**可回放的结构化事件日志 + 依赖/因果视图 + 面向任务的语义压缩**。embedding 适合检索相似轨迹或技能，但不应替代可验证的原始 action/result 记录。

## 6. 代表性文献证据表

引用数为 OpenAlex 在 2026-09-20 附近的快照，仅作发现信号；`—` 表示未使用可比的 OpenAlex 记录。

| 文献 | 年份/venue | ID | 轨迹表征贡献 | OpenAlex 引用 |
|---|---|---|---|---:|
| [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) | 2023 / ICLR | arXiv:2210.03629 | thought-action-observation 交错序列 | — |
| [Toolformer: Language Models Can Teach Themselves to Use Tools](https://proceedings.neurips.cc/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html) | 2023 / NeurIPS | DOI: 10.52202/075280-2997 | `<API> call → response </API>` 线性化 | 452 |
| [Reflexion: Language Agents with Verbal Reinforcement Learning](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) | 2023 / NeurIPS | DOI: 10.52202/075280-0377 | 轨迹 + verbal reflection episodic memory | 517 |
| [Mind2Web: Towards a Generalist Agent for the Web](https://arxiv.org/abs/2306.06070) | 2023 / NeurIPS | DOI: 10.52202/075280-1220 | `(target element, operation)` + DOM/trace | 65 |
| [ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs](https://arxiv.org/abs/2307.16789) | 2024 / ICLR | arXiv:2307.16789 | thought/API/parameters/observation；DFSDT 搜索树 | — |
| [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) | 2024 / ICLR | arXiv:2308.03688 | 多环境、多轮交互轨迹 benchmark | 55 |
| [ExpeL: LLM Agents Are Experiential Learners](https://doi.org/10.1609/aaai.v38i17.29936) | 2024 / AAAI | DOI: 10.1609/aaai.v38i17.29936 | experience pool + embedding/kNN + cross-task insights | 120 |
| [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://proceedings.iclr.cc/paper_files/paper/2024/file/4410c0711e9154a7a2d26f9b3816d1ef-Abstract-Conference.html) | 2024 / ICLR | arXiv:2307.13854 | `S,A,O,T`；DOM/screenshot/accessibility tree | — |
| [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | 2024 / TMLR | arXiv:2305.16291 | 状态快照 + executable skills + vector skill library | 204 |
| [AgentTuning: Enabling Generalized Agent Abilities for LLMs](https://aclanthology.org/2024.findings-acl.181/) | 2024 / Findings ACL | DOI: 10.18653/v1/2024.findings-acl.181 | 多轮 interaction trajectory + 任务级 reward | 33 |
| [Agent Trajectory Explorer](https://ojs.aaai.org/index.php/AAAI/article/view/35350) | 2025 / AAAI demo | DOI: 10.1609/aaai.v39i28.35350 | 把原始轨迹转换成可导航、可标注的可视化 | 0 |
| [ACON: Optimizing Context Compression for Long-horizon LLM Agents](https://arxiv.org/abs/2510.00615) | 2026 / ICML | arXiv:2510.00615 | history/observation 压缩；保留状态和决策线索 | 1 |
| [TRAJECT-Bench](https://arxiv.org/abs/2510.04550) | 2026 / ICLR | arXiv:2510.04550 | parallel set、sequential chain、依赖/顺序指标 | 0 |
| [AgentProcessBench](https://arxiv.org/abs/2603.14465) | 2026 / KDD | arXiv:2603.14465 | message trajectory + `+1/0/-1` 步骤标签 + 首错 | 0 |
| [ToolPRMBench](https://aclanthology.org/2026.findings-acl.602/) | 2026 / Findings ACL | DOI: 10.18653/v1/2026.findings-acl.602 | 历史 + 正确动作 + 错误候选 + tool metadata | 0 |
| [Plan-RewardBench](https://aclanthology.org/2026.acl-long.1062/) | 2026 / ACL | DOI: 10.18653/v1/2026.acl-long.1062 | trajectory-level preference pairs / hard negatives | 0 |
| [AgentTrace](https://arxiv.org/abs/2603.14688) | 2026 / arXiv | arXiv:2603.14688 | 从执行日志重建 causal graph 做根因分析 | 0 |
| [From Storage to Experience](https://arxiv.org/abs/2605.06716) | 2026 / arXiv survey | arXiv:2605.06716 | Storage → Reflection → Experience 演化框架 | 1 |

## 7. 参考阅读顺序

如果只读 6 篇，建议：

1. ReAct：理解最基础的 thought/action/observation 轨迹。
2. WebArena：理解状态、观察、动作和最终状态验证。
3. ToolLLM：理解工具调用链、真实响应和搜索树。
4. Reflexion：理解轨迹如何转成反思记忆。
5. TRAJECT-Bench：理解当前工具轨迹指标和依赖结构。
6. AgentProcessBench 或 ToolPRMBench：理解步骤级过程监督与 reward model。

