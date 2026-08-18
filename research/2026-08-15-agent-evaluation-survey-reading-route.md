# Agent 测评与测试综述：7 篇全景入门精读路线

> 检索日期：2026-08-15。目标不是罗列所有 Agent 综述，而是为初学者选择一条从“Agent 是什么”到“如何评价、测试和验证 Agent 系统”的最短完整路径。

## 1. 检索范围与方法

### 1.1 研究问题

本轮回答三个问题：

1. 初学者需要哪几篇综述，才能建立 Agent 测评与测试的完整概念地图？
2. 哪些综述分别补足通用评测、泛化可靠性、安全、Evaluator 与系统验证？
3. 这些综述的正式版本、开放全文与证据状态是否可信？

时间范围默认设为 2023–2026，英文论文为主。纳入对象必须是综述、系统化知识研究（SoK）或系统验证型文献回顾；只提供单个 benchmark、单一模型对比或特定行业应用综述的论文不进入最终清单。

### 1.2 数据源与检索式

使用 literature-research 技能的 `conference_search.py`，从 Semantic Scholar、OpenAlex、Crossref、arXiv 与 DBLP 合并检索以下六组查询，每组最多保留 40 条：

```text
LLM agent evaluation survey
agentic AI testing validation survey
LLM agent benchmark survey
LLM agent security systematic review
AI agent reliability robustness evaluation survey
agent trajectory evaluation survey
```

检索 manifest 保存在 `tmp/agent-survey-route-20260815/q*/results.json`。第一轮中 q1、q2、q3、q4、q6 各返回 40 条；q5 因所有来源同时超时而重试，重试后返回 40 条且无来源错误。第一轮 DBLP 多次出现 SSL EOF/握手超时，q6 的 Semantic Scholar 返回 HTTP 429，q6 的 OpenAlex 超时；这些异常不能解释为“数据库中没有相关论文”。

2026-08-15 随后对 DBLP 做了专项重试。诊断结果为：DNS 正常；默认 `HTTPS_PROXY=http://127.0.0.1:7891` 在建立 CONNECT 隧道后发生 TLS `SSL_ERROR_SYSCALL`；把 `dblp.org` 加入 `NO_PROXY` 后，DBLP API 曾成功返回 `status=200` JSON，但连续请求又出现远端关闭和零字节超时。因此，本轮另用相同六组查询对 `dblp.org` 索引做低频、域名限定补检，并核对命中的 DBLP publication/author records。专项补检确认了最终清单中的 Yehudai 等和 Kim 等的 DBLP 记录，也发现以下高相关扩展候选：

- Feng He et al., *The Emerged Security and Privacy of LLM Agent: A Survey with Case Studies*, ACM Computing Surveys；
- Miao Yu et al., *A Survey on Trustworthy LLM Agents: Threats and Countermeasures*, KDD 2025/CoRR；
- Kun Wang et al., *A Comprehensive Survey in LLM(-Agent) Full Stack Safety*, CoRR；
- Yuchen Ling et al., *Toward Secure LLM Agents: Threat Surfaces, Attacks, Defenses, and Evaluation*, CoRR；
- Junyu Luo et al., *Large Language Model Agent: A Survey on Methodology, Applications and Challenges*, CoRR。

这些工作没有改变核心 7 篇：前四篇与 Kim 等的系统安全 SoK 高度重叠，最后一篇偏通用 Agent 方法和应用，均未补足主路线中缺失的独立维度。它们适合作为安全或架构专题的第二层扩展阅读。

合并后有约 94 个标题包含 survey、review、SoK、taxonomy 或 validation 的候选。人工筛选排除了：

- 特定行业应用综述，如医疗、教育、IoT；
- 普通 LLM 测评而非 Agent 测评；
- “使用 Agent 测传统软件”或“使用 Agent 生成综述”；
- 与入选论文高度重复且没有新增视角的宽泛综述；
- 只有元数据、来源可疑或身份冲突且无法进一步核验的记录。

### 1.3 核验与去重规则

按 DOI、arXiv ID、规范化标题与作者顺序去重。正式会议/期刊版优先，开放 arXiv 版本只作为全文入口。DOI 使用 `verify_metadata.py` 对 Crossref 与 OpenAlex 交叉核验；没有 DOI 的 USENIX 论文以官方会议页核验；最新预印本以 arXiv 身份核验。

证据等级：

- **全文已检查**：本地 PDF 已读取，可用于章节推荐和方法综合；
- **已核验**：Crossref 与 OpenAlex 一致，或权威出版方记录确认；
- **部分核验**：只有 arXiv 等单一权威记录，且尚无正式发表版本。

## 2. 最终推荐与证据表

| 顺序 | 论文 | 年份与版本 | 标识符 | 核验/证据 | 在路线中的作用 |
|---|---|---|---|---|---|
| 1 | *A Survey on Large Language Model based Autonomous Agents* | Frontiers of Computer Science, 2024 | DOI `10.1007/s11704-024-40231-1`；arXiv `2308.11432` | 已核验；全文已检查 | 先理解 Agent 架构，避免把模型、Agent 和 Harness 混为一谈 |
| 2 | *Evaluation and Benchmarking of LLM Agents: A Survey* | KDD 2025 | DOI `10.1145/3711896.3736570`；arXiv `2507.21504` | 已核验；全文已检查 | 用简洁的二维 taxonomy 建立评测全景 |
| 3 | *A Survey on Evaluation of LLM-based Agents* | Findings of ACL 2026 | DOI `10.18653/v1/2026.findings-acl.1330`；arXiv `2503.16416` | 已核验；全文已检查 | 深入 benchmark、轨迹评价与评测框架 |
| 4 | *Generalizability of Large Language Model-Based Agents: A Comprehensive Survey* | ACM Computing Surveys, 2026 | DOI `10.1145/3794858`；arXiv `2509.16330` | 已核验；全文已检查 | 把单次能力提升到跨任务、环境和组件的泛化可靠性 |
| 5 | *SoK: Attack and Defense Landscape of Agentic AI Systems* | USENIX Security 2026 | 官方会议记录；扩展版 arXiv `2603.11088` | USENIX 官方页核验；会议预出版全文已检查 | 建立系统安全攻击面与分层防御图 |
| 6 | *A Survey on LLM-as-a-Judge* | The Innovation, 2026 | DOI `10.1016/j.xinn.2025.101253`；arXiv `2411.15594` | 已核验；全文已检查 | 理解自动 Evaluator 为什么必须被测试 |
| 7 | *Beyond Component Testing: Validating Agentic AI Systems* | arXiv 预印本, 2026 | arXiv `2607.29405` | 部分核验；全文已检查 | 把前六篇合并为面向生命周期的系统验证议程 |

最终清单只有第 7 篇仍是纯预印本；第 6 篇虽然最初以 2024 arXiv 版本传播，但已经正式发表于 2026 年 *The Innovation*，不应继续标作预印本。

## 3. 三篇入门必读

### 3.1 Wang et al.：先建立 Agent 架构地图

开放全文：[本地 PDF](./papers/2024-Wang-AutonomousAgentSurvey.pdf) · [DOI](https://doi.org/10.1007/s11704-024-40231-1) · [arXiv](https://arxiv.org/abs/2308.11432)

**为什么关键**

这篇的主要价值不是最新 benchmark，而是把 Autonomous Agent 拆成 profiling、memory、planning 和 action 等模块。只有先理解这些部件，后面才能判断失败来自模型、记忆、规划、工具还是执行层。

**重点读**

- Section 2：Agent 架构与各模块；
- Section 4：主观/客观 Agent 评价；
- Section 6：角色能力、对齐、提示鲁棒性、幻觉与知识边界。

**它覆盖了什么**：Agent 的基本结构、应用、早期评价方式和能力边界。

**它遗漏了什么**：对状态差分、完整轨迹、故障注入、Judge 元评测和生产回归覆盖不足；不要把它当作最新测试方法综述。

**阅读问题**

1. 一个 Agent 的失败可以落在哪些模块？
2. 模型能力和 Agent 系统能力为什么不能直接等同？
3. 哪些评价对象可以精确判定，哪些只能语义评价？

### 3.2 Mohammadi et al.：用二维 taxonomy 看全景

开放全文：[本地 PDF](./papers/2025-Mohammadi-AgentEvaluationSurvey.pdf) · [DOI](https://doi.org/10.1145/3711896.3736570) · [arXiv](https://arxiv.org/abs/2507.21504)

**为什么关键**

篇幅较短，适合第一次系统理解 Agent evaluation。它将“评价什么”和“怎样评价”分开：前者包含行为、能力、可靠性和安全，后者包含静态/动态交互、数据集与指标计算。

**重点读**

- Section 2：整体 taxonomy；
- Sections 3.1–3.4：行为、能力、可靠性、安全；
- Sections 4.1–4.3：静态/动态评测、交互方式与指标；
- Section 6：未来方向。

**它覆盖了什么**：评测目标、动态环境、可靠性、安全、成本与企业场景。

**它遗漏了什么**：对具体轨迹 Oracle、评测器失效模式和软件测试式缺陷发现讲得不够深。

**阅读问题**

1. Evaluation objective 和 evaluation process 为什么要分开？
2. Success、robustness、safety 和 cost 为什么不能压成一个分数？
3. 静态离线评测何时会错误代表真实 Agent 能力？

### 3.3 Yehudai et al.：进入 Agent 专属评测方法

开放全文：[本地 PDF](./papers/2026-Yehudai-AgentEvaluationSurvey.pdf) · [ACL Anthology](https://aclanthology.org/2026.findings-acl.1330/)

**为什么关键**

这是三篇中与“Agent evaluation”最直接、分类最细的一篇。它区分核心能力、应用型 Agent、通用 Agent、benchmark 设计维度和开发者评测框架，并专门讨论 final-response、stepwise 和 trajectory-based evaluation。

**重点读**

- Section 2：核心 Agent 能力评价；
- Sections 3–4：应用型与通用 Agent；
- Section 5：benchmark 维度与 final/step/trajectory 评价；
- Section 6：评测框架；
- Section 7.2：未来方向；
- Appendix A：文献检索方法。

**它覆盖了什么**：任务类型、环境、轨迹、指标、框架和 benchmark 选择。

**它遗漏了什么**：它仍主要是一篇 evaluation survey，而不是故障注入、Fuzzing、失败最小化和 CI 回归的系统综述。

**阅读问题**

1. Final-response、stepwise 和 trajectory-based evaluation 各自漏掉什么？
2. Reference-based 与 reference-free 轨迹评价有什么结构性权衡？
3. Benchmark、Agent 框架和 Evaluator 怎样共同影响最后的分数？

## 4. 三篇专题必读

### 4.1 Zhang et al.：泛化与可靠性

开放全文：[本地 PDF](./papers/2026-Zhang-AgentGeneralizabilitySurvey.pdf) · [DOI](https://doi.org/10.1145/3794858) · [arXiv](https://arxiv.org/abs/2509.16330)

**为什么关键**

一般 benchmark 测“在已给任务上能不能成功”；这篇追问 Agent 是否能跨指令、任务、环境、领域和组件配置保持表现。它还区分 generalizable framework 与 generalizable agent，能帮助理解 Harness 与模型之间的交互。

**重点读**

- Sections 1.1–1.2：问题边界及与其他综述区别；
- Section 2：Agent 生态、组件与多方利益相关者；
- Sections 3.2–3.4：评价维度、指标及局限；
- Sections 7.5、7.8：不确定性和从框架泛化到 Agent 泛化；
- Section 8：结论与未来方向。

**它覆盖了什么**：跨域泛化、方差、成本、组件异质性和架构协调。

**它遗漏了什么**：泛化不是完整可靠性；故障恢复、非幂等副作用、持续状态漂移和安全事件仍需单独测试。

**阅读问题**

1. “平均成功率高”和“跨环境泛化好”有什么区别？
2. 怎样区分模型泛化、组件泛化与 Harness 泛化？
3. 为什么方差和泛化成本应成为指标？

### 4.2 Kim et al.：Agent 系统安全

开放全文：[本地 PDF](../自己找的论文/sec26_prepub_kim-juhee-agentic.pdf) · [USENIX 官方页](https://www.usenix.org/conference/usenixsecurity26/presentation/kim-juhee-agentic)

**为什么关键**

与只讨论 jailbreak 的综述不同，这篇从系统安全角度分析由 LLM、RAG、长期存储、工具、凭据和编排层组成的 Agent。它把攻击面与 input/output guardrail、信息流控制、监控、人在回路、权限隔离、形式化方法、身份和凭据管理等防御对应起来。

**重点读**

- Sections 2–3：Agent 设计空间；
- Section 4：攻击面与安全风险；
- Sections 5.1–5.6：安全目标、防御机制及设计原则；
- 每个防御小节末尾的 `Limitations and Open Challenges`；
- Section 6：结论。

**它覆盖了什么**：输入、工具、数据流、权限、身份、凭据、监控和 secure-by-design。

**它遗漏了什么**：SoK 给出攻击/防御地图，但不会替你设计可执行安全 Oracle、正常效用基线和生产事件频率模型。

**阅读问题**

1. Agent 安全为什么不能简化为 Prompt Injection 检测？
2. 哪些问题应由模型 guardrail 处理，哪些必须由权限和信息流机制处理？
3. 每种防御会牺牲多少正常任务效用，论文是否真的测量了它？

### 4.3 Gu et al.：Evaluator 也需要被测试

开放全文：[本地 PDF](./papers/2026-Gu-LLMJudgeSurvey.pdf) · [正式全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13237853/) · [DOI](https://doi.org/10.1016/j.xinn.2025.101253)

**为什么关键**

开放式 Agent 任务经常依赖 LLM Judge。这篇系统整理 Judge 的构建、改进、可靠性评价、偏差和对抗鲁棒性，并包含 Agent 场景。它能防止把“有一个 Judge”误当成“已经有可靠 Oracle”。

**重点读**

- Sections 2.4–2.5：评价流程和快速实践；
- Section 4：Judge 的人工一致性、偏差、对抗鲁棒性与元评测；
- Section 5 中的 Agent 应用；
- Section 6：可靠性、鲁棒性、透明性和时间一致性；
- Section 7：未来工作。

**它覆盖了什么**：Judge 设计、偏差、可靠性、对抗攻击和 meta-evaluation。

**它遗漏了什么**：这不是 Agent 专属综述；对环境终态、工具副作用和长轨迹 grounding 的处理仍需要结合 AgentRewardBench 等原始论文。

**阅读问题**

1. Judge 与人工一致是否足以证明 Judge 正确？
2. 位置偏差、冗长偏差、自偏好和轨迹内注入如何影响 Agent 评价？
3. 哪些断言应交给程序化 Oracle，而不是 LLM Judge？

## 5. 前沿补充：从 Evaluation 走向 Validation

### 5.1 Mirto et al.：生命周期系统验证

开放全文：[本地 PDF](./papers/2026-Mirto-AgenticValidationSurvey.pdf) · [arXiv](https://arxiv.org/abs/2607.29405)

**为什么关键**

这是最终清单中唯一尚未正式发表的预印本，也是最直接讨论“testing/validation”而非排行榜的一篇。它综合 257 篇文献，用 behavioral、safety、temporal、regulatory 和 multi-agent 五个维度描述 Agent 验证，并把离线评测延伸到运行时监控和审计证据。

**重点读**

- Sections 1.2–1.3：五个 testing mismatch；
- Section 2：系统综述方法，尤其 2.3–2.8；
- Sections 4–5：扩大后的 assurance target 及传统软件测试假设为何失效；
- Section 6：五维 taxonomy；
- Section 7：现有方法；
- Sections 9–10：研究议程与开放问题。

**它覆盖了什么**：轨迹上下文、时间有效性、运行时保障、监管可读性、多智能体和生命周期证据。

**它遗漏了什么**：它很新，taxonomy 和 257 篇编码尚缺独立复现；跨领域综合较宽，不能替代具体测试技术的原始论文。

**阅读问题**

1. Agent 使传统软件测试的哪些假设失效，哪些仍然成立？
2. 离线 benchmark、预发布测试、运行时监控和审计怎样形成闭环？
3. “验证轨迹处于上下文中”怎样转化为可执行测试用例和 Oracle？

## 6. 推荐阅读顺序

建议分四轮，而不是七篇连续从头读到尾：

1. **架构轮**：Wang Section 2 → 明确 Agent 由哪些组件组成。
2. **评测轮**：Mohammadi 全文 → Yehudai Sections 5–7 → 建立 objective/process 与 trajectory/oracle 地图。
3. **专项轮**：Zhang Sections 3、7–8 → Kim Sections 4–5 → Gu Sections 4、6 → 分别理解泛化、安全和 Evaluator 风险。
4. **研究轮**：Mirto Sections 5–10 → 把前面知识重新组织为软件测试和生命周期验证问题。

如果时间非常有限，先读 Mohammadi、Yehudai 和 Mirto；如果准备做实验，再补 Kim、Gu 和 Zhang；Wang 用于补齐 Agent 架构基础。

## 7. 七篇综述的共同结论

七篇论文的共同判断可以压缩为以下五点：

1. **Agent 的评价对象是系统，不只是 backbone LLM。** 模型、记忆、规划器、工具、Harness、环境和 Evaluator 共同决定结果。
2. **任务成功率只是底线。** 还需要过程、状态副作用、稳定性、安全、成本和延迟。
3. **轨迹是核心证据。** 但轨迹评价不能要求唯一参考路径，也不能只相信 Agent 的自然语言自述。
4. **Evaluator 本身必须接受元评测。** LLM Judge 的一致性、偏差、鲁棒性、校准和成本都需要测试。
5. **研究正从 benchmark 转向 lifecycle validation。** 离线测评需要与故障注入、对抗测试、运行时监控、版本回归和审计证据连接。

## 8. 关键分歧与研究空白

### 8.1 Evaluation 与 Testing 的边界

通用评测综述主要回答“Agent 能力有多强”；系统验证综述回答“什么条件下失败、为什么失败、修复后是否复现”。现有文献常把两者混称 evaluation，导致 benchmark 数量很多，而测试生成、覆盖反馈、失败最小化和回归闭环较少。

### 8.2 Oracle 没有统一答案

精确规则可复现，但可能拒绝合法替代路径；LLM Judge 灵活，但会受到自述、位置、冗长、模型家族和攻击内容影响。更可信的方向是环境状态断言、轨迹约束、局部语义 Judge 与人工校准的混合 Oracle。

### 8.3 泛化、可靠性与安全尚未统一

泛化综述关注跨任务/环境表现，安全 SoK 关注攻击与防御，系统验证综述关注时间和生命周期。真实系统需要把重复运行、环境扰动、故障恢复、权限、安全和成本放在同一实验设计中，当前仍缺统一协议。

### 8.4 最值得继续研究的空白

- Agent 状态、工具序列和风险结果的统一覆盖定义；
- 语义变形测试、灰盒 Fuzzing 和跨框架故障注入；
- 多条正确路径下的混合轨迹 Oracle；
- 长期记忆与多智能体错误的传播和因果定位；
- 长轨迹失败的自动缩减与稳定回归；
- 隐私保护的生产 trace 回放；
- MCP/Skill/工具供应链的版本、权限和组合测试。

## 9. 证据冲突与限制

- DBLP 第一轮因本地 HTTPS 代理的 TLS 隧道失败而缺失；绕过代理后 API 可间歇连通，但连续访问仍被远端关闭或超时。专项域名补检补回了关键 DBLP 记录，但不等价于一次完全稳定的 DBLP API 批量导出。Semantic Scholar 另有一次 429，OpenAlex 和若干来源有超时，因此不能声称检索绝对穷尽。
- *Evolutionary Perspectives on the Evaluation of LLM-Based AI Agents* 与入选通用综述高度重叠；本地证据表所记正式 DOI 在本轮 Crossref/OpenAlex 查询中未解析，因此不进入核心 7 篇。它仍可作为 benchmark 表格型备查资料。
- Kim 等的 USENIX 会议版为三作者预出版稿；arXiv `2603.11088` 是作者扩展版且作者列表扩大。两者属于版本关系，不应当作两篇独立工作。
- Mirto 等仅有 arXiv 版本；其 257 篇编码和 taxonomy 在正式评审或独立复现前应降低证据权重。
- 综述适合建立地图，但具体实验数字、攻击成功率和 Judge 准确性必须回到原始论文核验。

## 10. 经核验的参考文献

1. Wang, L., Ma, C., Feng, X., et al. (2024). A survey on large language model based autonomous agents. *Frontiers of Computer Science*. https://doi.org/10.1007/s11704-024-40231-1
2. Mohammadi, M., Li, Y., Lo, J. C., & Yip, W. (2025). Evaluation and Benchmarking of LLM Agents: A Survey. *Proceedings of KDD 2025*. https://doi.org/10.1145/3711896.3736570
3. Yehudai, A., Eden, L., Li, A., et al. (2026). A Survey on Evaluation of LLM-based Agents. *Findings of ACL 2026*. https://doi.org/10.18653/v1/2026.findings-acl.1330
4. Zhang, M., Yang, Y., Xie, R., Dhingra, B., Zhou, S., & Pei, J. (2026). Generalizability of Large Language Model-Based Agents: A Comprehensive Survey. *ACM Computing Surveys*. https://doi.org/10.1145/3794858
5. Kim, J., Guo, W., & Song, D. (2026). SoK: Attack and Defense Landscape of Agentic AI Systems. *USENIX Security Symposium 2026*. https://www.usenix.org/conference/usenixsecurity26/presentation/kim-juhee-agentic
6. Gu, J., Jiang, X., Shi, Z., et al. (2026). A survey on LLM-as-a-judge. *The Innovation, 7*(6), 101253. https://doi.org/10.1016/j.xinn.2025.101253
7. Mirto, F. O., D'Agati, L., Tricomi, G., et al. (2026). Beyond Component Testing: Validating Agentic AI Systems. arXiv:2607.29405. https://arxiv.org/abs/2607.29405
