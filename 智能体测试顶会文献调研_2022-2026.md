# 智能体测试顶会文献调研（2022–2026）

检索日期：2026-09-02

## 1. 范围与判定标准

- 主题：LLM/自主智能体的测试、评测、失效诊断、红队与安全验证；同时单列“用智能体执行软件/安全测试”。
- Venue：软件工程以 ICSE、FSE、ASE、ISSTA、ICST 为主；AI 以 ICLR、NeurIPS、ICML、ACL/EMNLP 为主；安全以 IEEE S&P、USENIX Security、CCS、NDSS 为主。
- 年份：2022–2026。实际满足条件的核心论文集中在 2024–2026；未发现 2022 年满足全部硬条件的条目。
- 硬门槛：具体方法论文必须核实公开代码；只有 survey/vision 的论文只作为追踪入口，不冒充可复现方法。
- 证据：优先会议/出版方、论文全文、Crossref/OpenAlex/arXiv 与论文官方仓库。引用数是 2026-09-02 的 OpenAlex 或 Semantic Scholar 动态快照，不作为唯一质量指标。

## 2. 最值得优先读的 10 篇

1. **AgentFuzz**（USENIX Security 2025）：真正把灰盒 fuzzing 用到 LLM agent 污点式漏洞检测，最贴近“智能体测试方法”。[论文](https://www.usenix.org/conference/usenixsecurity25/presentation/liu-fengyu)｜[代码](https://github.com/LFYSec/AgentFuzz)
2. **Datura**（ISSTA 2026）：对智能体工具调用链做渐进式红队测试，是软件测试顶会中最直接的 agent red-teaming 工作。[会议页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/10/Datura-Progressive-Red-Teaming-Testing-for-Tool-Invocation-Chain-in-LLM-Agents)｜[代码](https://github.com/ycshao12/Datura_RedTeaming_Testing)
3. **AgentDojo**（NeurIPS 2024 D&B）：动态评测 agent 的 prompt injection 攻击与防御。[论文](https://arxiv.org/abs/2406.13352)｜[代码](https://github.com/ethz-spylab/agentdojo)
4. **Agent Security Bench / ASB**（ICLR 2025）：系统化攻击、防御和评测 LLM agents。[论文](https://openreview.net/forum?id=V4y0CpX4hK)｜[代码](https://github.com/agiresearch/ASB)
5. **Understanding Software Engineering Agents**（ASE 2025 Distinguished Paper）：从 Thought–Action–Result 轨迹诊断 SE agent 失效。[论文](https://arxiv.org/abs/2506.18824)｜[代码/数据](https://github.com/sola-st/llm-agents-study)
6. **AgentBoard**（NeurIPS 2024 D&B Oral）：不仅看最终成功率，还做细粒度多轮轨迹分析。[论文](https://arxiv.org/abs/2401.13178)｜[代码](https://github.com/hkust-nlp/AgentBoard)
7. **WebArena**（ICLR 2024）：在可复现动态网站中端到端测试 Web agents。[论文](https://arxiv.org/abs/2307.13854)｜[代码](https://github.com/web-arena-x/webarena)
8. **τ-bench**（ICLR 2025）：测试 agent、工具与模拟用户在多轮交互中的策略一致性。[论文](https://arxiv.org/abs/2406.12045)｜[代码](https://github.com/sierra-research/tau-bench)
9. **DroidAgent**（ICST 2024）：自主 LLM agent 进行意图驱动的移动 GUI 测试。[论文](https://arxiv.org/abs/2311.08649)｜[代码](https://github.com/coinse/droidagent)
10. **Incalmo**（IEEE S&P 2026）：agent 驱动多主机网络红队测试，并发布 MHBench。[论文](https://arxiv.org/abs/2501.16466)｜[代码](https://github.com/bsinger98/Incalmo)

## 3. 软件工程顶会核心论文

| 论文 | 年份/Venue | 测试对象与贡献 | 标识/引用快照 | 代码与全文 | 核验 |
|---|---|---|---|---|---|
| Intent-Driven Mobile GUI Testing with Autonomous Large Language Model Agents (DroidAgent) | ICST 2024 | LLM agent 自主探索 Android GUI，并以用户意图引导测试 | DOI `10.1109/ICST60714.2024.00020`; arXiv `2311.08649`; OA≈31 | [代码](https://github.com/coinse/droidagent) / [PDF](https://arxiv.org/pdf/2311.08649) | Verified；全文 |
| Make LLM a Testing Expert | ICSE 2024 | 功能感知决策与类人交互的移动 GUI 测试 | DOI `10.1145/3597503.3639180`; arXiv `2310.15780`; OA≈103 | [代码汇总](https://github.com/LLM-Testing/LLM4SoftwareTesting) / [PDF](https://arxiv.org/pdf/2310.15780) | 部分核验；摘要+仓库 |
| AutoRestTest | ICSE 2025 Demo | LLM + 多智能体强化学习自动生成 REST API 测试 | DOI `10.1109/ICSE-Companion66252.2025.00015`; arXiv `2501.08600`; OA≈8 | [代码](https://github.com/selab-gatech/AutoRestTest) / [PDF](https://arxiv.org/pdf/2501.08600) | 部分核验；官方摘要+仓库 |
| LLMDroid | FSE 2025 | 用 LLM 引导提升移动 App GUI 测试覆盖率 | DOI `10.1145/3715763`; OA≈17 | [代码](https://github.com/LLMDroid-2024/LLMDroid) | 部分核验；官方摘要+仓库 |
| You Name It, I Run It (ExecutionAgent) | ISSTA 2025 | agent 自动理解并执行任意项目的测试套件，解决环境/命令配置问题 | DOI `10.1145/3728922`; arXiv `2412.10133`; OA≈30 | [代码](https://github.com/sola-st/ExecutionAgent) / [PDF](https://arxiv.org/pdf/2412.10133) | Verified；全文 |
| Understanding Software Engineering Agents | ASE 2025 | 用 Thought–Action–Result 轨迹分析 agent 的行为与失败原因 | DOI `10.1109/ASE63991.2025.00234`; arXiv `2506.18824`; OA≈5 | [代码/数据](https://github.com/sola-st/llm-agents-study) / [PDF](https://arxiv.org/pdf/2506.18824) | Verified；全文 |
| Datura | ISSTA 2026 | 渐进式生成/变异攻击，红队测试 agent 工具调用链 | 新录用，DOI 尚未稳定 | [代码](https://github.com/ycshao12/Datura_RedTeaming_Testing) / [会议页](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/10/Datura-Progressive-Red-Teaming-Testing-for-Tool-Invocation-Chain-in-LLM-Agents) | 部分核验；官方摘要+仓库 |

说明：ICST 是测试领域核心会议，但通常不列为 CCF-A；这里因其对“智能体测试”高度直接而保留。AutoRestTest 是 ICSE Companion/Demo，已明确标注，不与 ICSE research track 混写。

## 4. AI 顶会核心论文

| 论文 | 年份/Venue | 评测维度 | 标识/引用快照 | 代码与全文 | 核验 |
|---|---|---|---|---|---|
| AgentBench | ICLR 2024 | 8 类交互环境中的推理与决策能力 | arXiv `2308.03688`; OA≈55 | [代码](https://github.com/THUDM/AgentBench) / [PDF](https://openreview.net/pdf?id=zAdUB0aCTQ) | 官方全文+仓库 |
| WebArena | ICLR 2024 | 动态网站中的端到端任务成功 | arXiv `2307.13854`; OA≈27 | [代码](https://github.com/web-arena-x/webarena) / [PDF](https://arxiv.org/pdf/2307.13854) | 官方全文+仓库；OpenAlex 标题字段有污染 |
| MINT | ICLR 2024 | 工具和语言反馈下的多轮交互 | arXiv `2309.10691`; OA≈16 | [代码](https://github.com/xingyaoww/mint-bench) / [PDF](https://arxiv.org/pdf/2309.10691) | 部分核验 |
| ToolLLM / ToolBench | ICLR 2024 Spotlight | 真实 API 选择、调用与泛化 | arXiv `2307.16789`; OA≈72 | [代码](https://github.com/OpenBMB/ToolBench) / [PDF](https://arxiv.org/pdf/2307.16789) | 官方全文+仓库；OpenAlex 标题字段有污染 |
| AgentBoard | NeurIPS 2024 D&B Oral | 多任务、多轮、细粒度进度与失败分析 | DOI `10.52202/079017-2365`; arXiv `2401.13178`; OA≈8–9 | [代码](https://github.com/hkust-nlp/AgentBoard) / [PDF](https://arxiv.org/pdf/2401.13178) | Verified |
| AgentDojo | NeurIPS 2024 D&B | 动态 prompt injection 攻防测试 | DOI `10.52202/079017-2636`; arXiv `2406.13352`; OA 版本计数冲突（约7/48） | [代码](https://github.com/ethz-spylab/agentdojo) / [PDF](https://arxiv.org/pdf/2406.13352) | 身份 Verified；引用数冲突 |
| τ-bench | ICLR 2025 | agent–tool–user 多轮策略遵循与可靠性 | arXiv `2406.12045`; OA≈7 | [代码](https://github.com/sierra-research/tau-bench) / [PDF](https://arxiv.org/pdf/2406.12045) | 部分核验 |
| Agent Security Bench (ASB) | ICLR 2025 | 对 agent 攻击与防御做统一形式化和 benchmark | arXiv `2410.02644`; OA≈6 | [代码](https://github.com/agiresearch/ASB) / [PDF](https://openreview.net/pdf?id=V4y0CpX4hK) | 部分核验 |
| R-Judge | Findings of EMNLP 2024 | agent 行为的安全风险意识评测 | DOI `10.18653/v1/2024.findings-emnlp.79`; arXiv `2401.10019`; OA≈36 | [代码](https://github.com/Lordog/R-Judge) / [PDF](https://aclanthology.org/2024.findings-emnlp.79.pdf) | Verified；**不是 EMNLP main** |

## 5. 安全顶会核心论文

| 论文 | 年份/Venue | 方法 | 标识/引用快照 | 代码与全文 | 核验 |
|---|---|---|---|---|---|
| Make Agent Defeat Agent (AgentFuzz) | USENIX Security 2025 | 定向灰盒 fuzzing：语义/路径距离反馈、prompt 变异、sink oracle；在 20 个 agent 应用中发现 34 个高危 0-day | USENIX proceedings；Zenodo `10.5281/zenodo.15590097` | [代码](https://github.com/LFYSec/AgentFuzz) / [论文](https://www.usenix.org/conference/usenixsecurity25/presentation/liu-fengyu) | 官方页+软件记录+仓库；全文 |
| Incalmo | IEEE S&P 2026 | 自主多主机渗透测试；MHBench 40 个网络 | DOI `10.1109/SP63933.2026.00132`; arXiv `2501.16466`; S2≈24 | [代码](https://github.com/bsinger98/Incalmo) / [PDF](https://arxiv.org/pdf/2501.16466) | Verified；全文 |
| IsolateGPT | NDSS 2025 | 隔离 LLM app/agent 组件，限制间接 prompt injection 与权限滥用 | DOI `10.14722/ndss.2025.241131`; arXiv `2403.04960`; S2≈132 | [代码](https://github.com/llm-platform-security/SecGPT) / [PDF](https://arxiv.org/pdf/2403.04960) | Verified；全文 |
| ACE | NDSS 2026 | 抽象–具体–执行规划、静态信息流检查、运行时 data/capability barriers | DOI `10.14722/ndss.2026.230352`; arXiv `2504.20984`; S2≈47 | [代码](https://github.com/llm-platform-security/SecGPT) / [PDF](https://arxiv.org/pdf/2504.20984) | Verified；全文 |
| SAGA | NDSS 2026 | 跨 agent 身份、注册、授权、委托和策略治理 | DOI `10.14722/ndss.2026.230869`; arXiv `2504.21034`; S2≈51 | [代码](https://github.com/gsiros/saga) / [PDF](https://arxiv.org/pdf/2504.21034) | Verified；摘要+仓库 |

## 6. “顺藤摸瓜”检索链

### 链 A：SE 测试智能体

**Towards Autonomous Testing Agents via Conversational LLMs**（ASE 2023，vision/taxonomy，DOI `10.1109/ASE56229.2023.00148`）
→ 同作者后续的 **DroidAgent**（ICST 2024，有代码）
→ GUI 测试分支的 **Make LLM a Testing Expert**（ICSE 2024）
→ 覆盖率增强的 **LLMDroid**（FSE 2025）。

这条链说明研究从“测试 agent 概念与架构”推进到可运行的自主探索、功能感知决策和覆盖率优化。

### 链 B：通用 agent benchmark 到细粒度诊断

自治智能体综述 / ACL 2026 agent evaluation survey
→ **AgentBench、WebArena、ToolLLM**（跨环境/网页/API 的最终结果评测）
→ **AgentBoard**（加入轨迹进度、步骤级分析）
→ **Understanding Software Engineering Agents**（聚焦 SE agent 的 Thought–Action–Result 轨迹失效）。

### 链 C：agent 安全评测

**R-Judge**（行为风险意识）
→ **AgentDojo**（动态 prompt injection 攻防）
→ **ASB**（统一攻击/防御 benchmark）
→ **Datura / AgentFuzz**（从 benchmark 走向测试输入生成、反馈引导变异和漏洞 oracle）。

### 链 D：防御架构演进

**IsolateGPT**（组件隔离）
→ **ACE**（指出规划/执行完整性与可用性缺口，加入信息流和 capability barriers）
→ **SAGA**（扩展到跨 agent 的身份、授权、委托与用户治理）。

### 链 E：agent 用于安全测试

**Incalmo** 的 related work
→ PentestGPT、CyberSecEval3、CAI 等非四大安全顶会方法
→ Incalmo 将任务推进到可复现的多主机网络和 MHBench。

## 7. 主题综合与研究空白

1. **测试 oracle 仍是瓶颈。** GUI/API/SWE benchmark 多依赖任务成功或单元测试；开放式 agent 行为缺少稳定、可解释的 oracle。AgentBoard 与轨迹研究改善诊断，但仍常依赖规则或 LLM judge。
2. **动态环境比静态问答更重要。** WebArena、AgentDojo、τ-bench、AgentFuzz 都把测试从单轮输出推进到 agent–environment 长轨迹，这是该方向最清晰的共同趋势。
3. **能力与安全必须配对测量。** 单看拒答可能把“不会操作”误判为“安全”；应使用能力匹配的 benign/harmful task pair，并同时报告安全成功和正常任务能力。
4. **覆盖率概念尚未统一。** 传统代码覆盖率不能完整表达 prompt、工具、状态、记忆、策略和跨 agent 通信空间。值得研究“轨迹覆盖 + 数据流覆盖 + 权限/工具覆盖”的联合指标。
5. **非确定性与重放不足。** 应报告多次运行的 pass@k/pass^k、模型版本、成本、环境快照和完整轨迹；否则 benchmark 排名很难复现。
6. **攻击测试与治理脱节。** AgentFuzz/Datura 擅长发现具体漏洞，SAGA/ACE 擅长约束执行，但“发现的轨迹自动生成最小权限策略或回归测试”仍缺少端到端闭环。
7. **真实 SE agent 的长期演化测试不足。** 当前大量 benchmark 是一次性 issue 或短任务；多版本需求变化、长期维护、记忆漂移和工具升级后的回归测试仍是明显空白。

一个较有潜力的研究切口是：**面向工具调用链的状态化、覆盖引导 agent fuzzing**。将 AgentFuzz 的数据流/sink 距离、Datura 的渐进式红队生成、AgentBoard/ASE 轨迹诊断，以及 ACE/SAGA 的权限策略统一到一个可重放测试框架中；oracle 同时检查任务成功、策略违规、数据泄漏和不可逆副作用。

## 8. 检索式、数据库与限制

主要检索式：

```text
("LLM agent" OR "language agent" OR "autonomous agent")
AND (testing OR evaluation OR benchmark OR validation OR fuzzing OR red teaming
     OR prompt injection OR failure diagnosis)
AND (ICSE OR FSE OR ASE OR ISSTA OR ICST OR ICLR OR NeurIPS OR ICML
     OR ACL OR EMNLP OR "IEEE S&P" OR "USENIX Security" OR CCS OR NDSS)
```

补充精确检索包括论文标题 + `GitHub/code/artifact`、会议官网 site query，以及 survey/benchmark 的 related work 与参考文献反向追踪。数据库/来源包括 Semantic Scholar、OpenAlex、Crossref、arXiv、DBLP、OpenReview、ACL Anthology、USENIX/NDSS/Researchr 官方页面和 GitHub。

限制：Semantic Scholar 无 key 时部分请求出现 429，按技能规则未重复轰炸，改用 OpenAlex；Google Scholar 因 Chrome CDP 未开启未使用。OpenAlex 对 WebArena、ToolLLM、AgentDojo 出现版本或标题污染，表中已标注冲突。该清单是“高精度、代码可复现”的核心集，而不是声称穷尽所有论文。

## 9. 排除记录（代表性）

- AgentInspect（ISSTA 2026）、MARG（ASE 2024）、Test vs Mutant / Sakura / TestDecision（ISSTA 2026）：主题相关，但未核实与论文匹配的公开代码，按硬门槛排除。
- ST-WebAgentBench、FirmAgent：有前沿价值，但本轮未核实官方代码，暂不进核心表。
- General AgentBench、RExBench：未录取/撤稿或 venue 不符合。
- workshop-only、仅 arXiv、普通期刊或仅 awesome list：可作线索，不作为顶会具体方法。
- AndroidWorld、BrowserGym 等：可作为环境/基础设施补充，但没有优先于上述更直接的 agent-testing 论文。

