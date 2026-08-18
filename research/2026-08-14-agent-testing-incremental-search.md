# AI 智能体测试与测评增量检索（2026-08-14）

## 1. 范围与检索策略

- 研究问题：在现有证据库之外，2024–2026 年有哪些直接贡献于 LLM/AI agent 测试方法、评测有效性、故障定位、运行时监控和工具安全的新论文？
- 纳入：直接以 agent 或 agent system 为被测对象，并提供 benchmark、测试框架、故障模型、oracle、监控或诊断方法。
- 降级/排除：仅使用 agent 去测试普通软件、仅做某应用能力榜单、普通 LLM 安全或缺乏可核验论文身份的产品资料。
- 数据源：`conference_search.py` 汇合 Semantic Scholar、OpenAlex、Crossref、arXiv、DBLP 和开放获取解析；检索日期为 2026-08-14。
- 精确查询：
  1. `LLM agent testing trajectory oracle fault injection metamorphic testing`
  2. `AI agent runtime monitoring observability reliability evaluation`
  3. `multi agent system evaluation cascading failure fault injection LLM`
  4. `tool using agent benchmark safety permissions MCP evaluation`
- 时间窗：2024–2026；每组最多 80 条；不限定会议。四组原始、未人工筛选结果保存在 `tmp/literature-search-20260814/*/results.json` 和 `.csv`。
- 去重：先 DOI，再 arXiv ID，再规范化题名与作者。下表是与当前 `research/evidence/evidence-table.csv` 逐题名比对后的增量候选。

本轮 Semantic Scholar 在三组查询中返回 HTTP 429，DBLP 四组均发生 SSL EOF；脚本保留了逐源错误，OpenAlex、Crossref 和 arXiv 仍返回结果。因此，“未发现”不能解释为数据库中不存在。

## 2. 增量证据表

证据等级除特别说明外均为“仅阅读摘要”：下列方法、规模和结论只复述摘要明确陈述的内容，不能支持更细的实验过程或独立有效性判断。

| 论文 | 年份/版本 | 身份与来源核验 | 补充价值 | 建议 |
|---|---|---|---|---|
| AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection | 2026；arXiv:2608.06790；DOI 10.1145/3832783.3837437 | OpenAlex 与 arXiv/S2 一致；Crossref 暂未解析，部分核验 | 在共享 HTTP/LLM API 层做非侵入运行时故障注入；覆盖 crash、omission、value fault，并检查 fault 是否真正触发 | **核心纳入，优先全文** |
| AgentTelemetry: A Fault Detection Benchmark and Toolkit for LLM Agent Observability | 2026；ACM AIware；DOI 10.1145/3805760.3814931 | Crossref 与 OpenAlex 精确一致，已核验 | 直接补足 agent observability、故障检测 benchmark 与工具链 | **核心纳入，优先全文** |
| Observability and Fault Injection for LLM-Based Multi-Agent Systems in Software Engineering | 2026；ICST；DOI 10.1109/ICST69053.2026.00037 | Crossref 与 OpenAlex 精确一致，已核验 | 用 OpenTelemetry 对 workflow、agent step、通信、tool call、LLM call 对齐追踪，并支持定点注错 | **核心纳入** |
| OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality | 2026；arXiv:2608.05263 | Semantic Scholar/arXiv 身份；未核验正式版本 | 将 cascade radius、分故障模式恢复率和分解质量作为一等指标，并用可复现注错 harness 测 orchestration | **核心观察，需全文/元数据复核** |
| Who Broke the System? Failure Localization in LLM-Based Multi-Agent Systems | 2026；arXiv:2607.07989 | arXiv 身份；Crossref 模糊返回他文，不采纳 | 同时定位责任 agent 与最早决定性失败步骤，代表从最终分数到根因定位的转向 | **核心观察** |
| VerifyMAS: Hypothesis Verification for Failure Attribution in LLM Multi-Agent Systems | 2026；arXiv:2605.17467 | arXiv 身份；结构化源未确认正式版本 | 用整条轨迹验证 failure hypothesis，再定位 agent，针对跨步不一致和协同错误 | **核心观察** |
| POIROT: Interrogating Agents for Failure Detection in Multi-Agent Systems | 2026；arXiv:2606.02282 | arXiv/S2 一致；10.48550 仅为 arXiv 注册 DOI，不视为正式出版 DOI | 让系统内部 agent 构成诊断层，并发布 BLAME failure-attribution benchmark | **相关纳入，需验证 judge 独立性** |
| Preventing Error Propagation in Multi-Agent AI through Runtime Monitoring | 2026；arXiv:2606.29026 | arXiv 身份 | 观察 reasoning exchange 后由错到对、由对到错的状态转移，直接研究错误传播 | **观察名单**：当前摘要更像受控问答实验，生产外推有限 |
| When the Manual Lies: A Realistic Benchmark to Evaluate MCP Poisoning Attacks for LLM Agents | 2026；CSCWD；DOI 10.1109/CSCWD68734.2026.11582512；arXiv:2605.24069 | Crossref 与 OpenAlex 精确一致，已核验 | 将工具描述元数据投毒作为独立攻击面，提供 MCP-TDP 沙箱和状态可观察测试案例 | **核心纳入** |
| MCPHunt: An Evaluation Framework for Cross-Boundary Data Propagation in Multi-Server MCP Agents | 2026；arXiv:2604.27819 | arXiv 身份；Crossref 模糊误匹配，正式版本未核验 | 用 canary/taint tracking 和 hard negative 客观检测跨 server 凭据传播，区分任务要求与策略违规 | **核心纳入，优先全文** |
| MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers | 2026；arXiv:2607.14642 | arXiv 身份 | 以 11 类 mutation operator 模拟 123 个 MCP server 的接口演化，测试 agent 对工具变更的适应性 | **核心纳入**，非常接近变形/回归测试 |
| OSGuard: A Benchmark for Safety in Computer-Use Agents | 2026；arXiv:2606.15034 | arXiv 身份；Crossref 模糊误匹配，正式版本未核验 | 把局部 action guardrail 与端到端执行分开，并在保留 task-success oracle 时加入 state-based safety invariant | **核心纳入，优先全文** |
| Unsafer in Many Turns: Benchmarking and Defending Multi-Turn Safety Risks in Tool-Using Agents | 2026；arXiv:2602.13379 | arXiv/OpenAlex 身份；正式版本未核验 | 将单轮伤害任务系统转换为多轮工具攻击序列，并提出新工具的自探索安全测试 | **相关纳入** |
| SafeToolBench: Pioneering a Prospective Benchmark to Evaluating Tool Utilization Safety in LLMs | 2025；Findings EMNLP；DOI 10.18653/v1/2025.findings-emnlp.958 | Crossref 与 OpenAlex 精确一致，已核验 | 现有证据库遗漏的正式 tool-utilization safety benchmark，可补工具选择/调用安全线 | **补录正式论文** |
| ToolSafety: A Comprehensive Dataset for Enhancing Safety in LLM-Based Agent Tool Invocations | 2025；EMNLP；DOI 10.18653/v1/2025.emnlp-main.714 | Crossref 与 OpenAlex精确一致，已核验 | 现有证据库遗漏的正式工具调用安全数据集论文 | **补录正式论文** |

## 3. 主题综合

### 3.1 从 benchmark 分数转向可控实验

AgentChaos、ICST 的 `llmmas-otel` 和 OrchestraBench 的共同变化，是先定义故障模型，再确保故障实际触发，并比较基线/故障轨迹。相比只报告 task success，这更接近传统软件可靠性测试：实验变量可控，失败影响可以沿调用链观察，恢复能力可以按故障类别分层。

### 3.2 “哪个 agent、哪一步、为什么”成为独立研究对象

Who Broke the System、VerifyMAS、POIROT 都不满足于判断最终答案是否错误，而是定位责任 agent、首次决定性错误或 failure hypothesis。这说明多智能体测试正在形成新的 oracle 层级：最终状态 oracle → step/trajectory oracle → causal/failure-attribution oracle。关键风险是这些工作大量依赖 LLM judge；后续全文阅读应核查人工标注协议、judge 与被测模型的同源偏差、长轨迹截断和置信度校准。

### 3.3 MCP 测试开始覆盖“变化”和“组合”

When the Manual Lies 测工具描述投毒，MCPHunt 测多 server 组合后的跨边界数据流，MCPEvol-Bench 用 mutation operator 测接口演化。三者分别对应供应链输入、组合权限和回归兼容性，显著超出“工具是否调用成功”的能力评测。它们很适合沉淀为工程测试套件：metadata fuzzing、canary taint tracking、schema mutation、版本差分和安全不变量。

### 3.4 安全 oracle 正从文本 judge 转向环境状态

OSGuard 的摘要明确区分局部 action 判断和端到端安全执行，并用状态不变量捕捉“任务完成但走了危险捷径”。这与 AgentDojo、AppWorld、WebArena 的 executable state evaluator 路线一致，也说明 agent 安全测试至少要同时报告 utility、最终安全状态和中间关键动作。

## 4. 冲突、限制与研究空白

1. **最新论文的出版状态不稳定。** 2026 年 arXiv 论文多数没有可核验正式版本；Crossref 题名检索对 MCPHunt、OSGuard、POIROT、VerifyMAS 返回了不相关模糊匹配，本报告没有把这些结果升级为正式 DOI。
2. **10.48550 不是同行评审证明。** POIROT 等记录中的 `10.48550/arXiv...` 仅对应 arXiv 注册，版本状态仍是预印本。
3. **摘要数字不可横比。** fault 配置、轨迹长度、模型快照、恢复定义和 attack success oracle 不同；本报告不把各摘要的百分比合并排序。
4. **故障模型覆盖仍缺少实证。** AgentChaos 的 API fault、OrchestraBench 的 orchestration fault 和 MCP mutation 是否代表真实生产分布，仍需 incident/telemetry 数据校准。
5. **失败归因缺少因果 ground truth。** 多 agent 之间存在补偿、冗余和共同原因；“最早错误步骤”未必等于“根因”。需要 counterfactual replay、组件替换和干预实验。
6. **安全与可用性的联合测量仍不充分。** 状态不变量、拦截器和自我修复都可能提高误阻断、延迟与成本，应统一报告 safety–utility–cost–latency。

## 5. 建议的下一轮精读顺序

1. AgentChaos：建立 agent chaos/fault taxonomy 与实验设计。
2. AgentTelemetry + ICST `llmmas-otel`：建立 telemetry schema、注错点和检测指标。
3. MCPHunt：复核 canary、hard negative 与信息流 oracle。
4. OSGuard：复核 action-level 与 execution-level 安全 oracle。
5. OrchestraBench、Who Broke the System、VerifyMAS：比较 cascade、定位和归因 ground truth。
6. MCPEvol-Bench、When the Manual Lies：整理 MCP mutation 与 poisoning 测试算子。

## 6. 可追溯入口

- AgentChaos: https://arxiv.org/abs/2608.06790
- AgentTelemetry: https://doi.org/10.1145/3805760.3814931
- Observability and Fault Injection: https://doi.org/10.1109/ICST69053.2026.00037
- OrchestraBench: https://arxiv.org/abs/2608.05263
- Who Broke the System?: https://arxiv.org/abs/2607.07989
- VerifyMAS: https://arxiv.org/abs/2605.17467
- POIROT: https://arxiv.org/abs/2606.02282
- Preventing Error Propagation: https://arxiv.org/abs/2606.29026
- When the Manual Lies: https://doi.org/10.1109/CSCWD68734.2026.11582512
- MCPHunt: https://arxiv.org/abs/2604.27819
- MCPEvol-Bench: https://arxiv.org/abs/2607.14642
- OSGuard: https://arxiv.org/abs/2606.15034
- Unsafer in Many Turns: https://arxiv.org/abs/2602.13379
- SafeToolBench: https://doi.org/10.18653/v1/2025.findings-emnlp.958
- ToolSafety: https://doi.org/10.18653/v1/2025.emnlp-main.714

