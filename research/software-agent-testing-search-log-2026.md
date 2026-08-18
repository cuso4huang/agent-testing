# 软件智能体测试方法学：可复现检索日志

## 1. 范围和筛选规则

- 检索日期：2026-08-15；时间范围：2023–2026。
- 语言：英文学术记录；综述交付为中文。
- 文献类型：会议、期刊和有独特方法贡献的预印本。
- 纳入：直接测试软件 Agent、Agent trace、harness 或相关多 Agent 基础设施，并提供测试生成、执行、oracle、注错、可靠性、诊断或可观测方法。
- 排除：用 Agent 测试传统软件、普通 LLM 评测、机器人/自动驾驶/网络控制的传统多 Agent 研究，以及没有方法贡献的能力排行榜。

## 2. 工具与数据源

使用 literature-research 技能的 `conference_search.py`，每个查询都以下列参数执行：

```bash
python3 conference_search.py \
  --query "<QUERY>" \
  --start-year 2023 --end-year 2026 \
  --limit 100 --no-conference-only \
  --output <OUTPUT_DIR>
```

脚本合并 Semantic Scholar、OpenAlex、Crossref、arXiv 与 DBLP，并保留每个请求的状态。Unpaywall 只用于发现法律允许的开放全文候选；“未找到开放 PDF”不代表论文没有合法全文。

## 3. 精确查询和结果

| ID | 查询 | 合并返回 | 来源错误 |
|---|---|---:|---|
| Q1 | `LLM agent testing evaluation validation quality assurance` | 100 | DBLP TLS unexpected EOF |
| Q2 | `agent test generation fuzzing metamorphic testing fault injection` | 100 | DBLP TLS handshake timeout |
| Q3 | `agent trajectory evaluation process evaluation oracle judge` | 100 | DBLP TLS unexpected EOF |
| Q4 | `agent reliability regression flakiness repeated trials` | 100 | DBLP TLS unexpected EOF |
| Q5 | `tool-use web code agent security testing red teaming` | 100 | DBLP TLS unexpected EOF |
| Q6 | `multi-agent failure diagnosis attribution chaos testing` | 100 | DBLP TLS handshake timeout |

六组共 600 条查询内记录，按规范化标题跨查询去重后为 584 个题名。DBLP 本轮六组均失败，不能将其解读为 DBLP 零命中；其他四个主要结构化来源仍返回了结果。

### 3.1 DBLP TLS 故障修复

后续诊断用同一个 DBLP API 请求建立了红/绿探针：默认网络路径只完成代理 `CONNECT`，8 秒后 TLS 超时；对 `dblp.org` 直连立即返回 HTTP 200 和有效 JSON。Python `urllib` 交叉检查也得到同样结果：默认 opener 超时，`ProxyHandler({})` 直连 opener 成功。

`conference_search.py` 已改为仅对 DBLP 使用不继承环境代理的 opener；Semantic Scholar、OpenAlex、Crossref、arXiv 及 PDF 下载仍保持原有网络路径。新增的回归测试会在 DBLP 回退到默认代理 opener 时立即失败。

修复后验证：

- 9 个 `conference_search.py` 单元测试全部通过；
- DBLP-only 真实 smoke test 在 0.775 秒内返回 HTTP 200，`source_errors={}`；
- 原六组紧接重跑时 Q1–Q4 均返回 HTTP 200，Q5–Q6 在连续请求后被远端主动断开，说明并发请求还会触发服务端节流。改为每组间隔 3 秒的低频顺序重跑后，Q1–Q5 均返回 HTTP 200；Q6 首次收到明确的 HTTP 503，冷却 10 秒后按标准指数退避单独重试，1.784 秒内返回 HTTP 200，`source_errors={}`。最终六组均完成 DBLP API 访问，且不再出现 TLS EOF/握手超时。

## 4. 去重与人工筛选

去重顺序为：规范化 DOI → arXiv ID → 标题+年份 → 模糊标题+作者交叠。预印本和正式版本保留版本关系，不算作两篇独立论文。

自动标题过滤会产生大量假阳性，主要包括：

- LLM/MAS 用于 REST API、GUI、网络、硬件或传统软件测试，被测对象不是 Agent；
- 机器人、无人机、自动驾驶和多 Agent 强化学习的传统容错/轨迹预测；
- 医疗、制造、通信等领域中“多 Agent 诊断”，实际是用 Agent 诊断外部对象；
- 普通 LLM-as-a-Judge 或单轮安全评测，没有 Agent 状态、行动或轨迹。

与已有 102 篇证据库比较后，本轮新增 9 个直接相关候选，均以 `watchlist` 同步至总证据表和筛选日志，不在没有全文证据时冒充成熟代表：

| 候选 | 身份/证据 | 筛选理由 |
|---|---|---|
| Automated Structural Testing of LLM-Based Agents | IEEE BigData 2025；DOI 双源核验；摘要 | trace、mock、assertion 和测试金字塔直接属于工程测试方法 |
| SpecOps | ACM DOI 部分核验；arXiv `2603.10268`；摘要 | 完整覆盖 GUI Agent 用例生成、环境搭建、执行和验证 |
| Assessing and Enhancing Robustness...Through Chaos Engineering | CAIN 2025；DOI 双源核验；元数据 | 是 AgentChaos 之前的直接 MAS 混沌工程候选，需补全文 |
| Agent vs. Agent | EMNLP Industry 2025；DOI 双源核验；元数据 | 针对定制 Agent 工作流的自动数据生成和红队 |
| Towards a Science of AI Agent Reliability | arXiv `2602.16666`；摘要 | 把可靠性分解为一致性、鲁棒性、可预测性和安全 |
| On the Reliability of Computer Use Agents | arXiv `2604.17849`；摘要 | 用重复执行和配对统计分析计算机使用 Agent 的不稳定性 |
| GroundEval | arXiv `2606.22737`；摘要 | 用确定性的证据访问和轨迹检查取代单一 Judge |
| Gaming the Judge | arXiv `2601.14691`；摘要 | 保持行动/观察不变，专门测试推理 trace 改写对 Judge 的影响 |
| TelemetrySuffBench | arXiv `2608.07899`；单源摘要 | 区分故障检测、来源定位和证据不足时弃权 |

## 5. 元数据核验

对四个有正式 DOI 的新候选使用 `verify_metadata.py`：

```bash
python3 verify_metadata.py --doi "10.1109/bigdata66926.2025.11401679" --pretty
python3 verify_metadata.py --doi "10.1145/3744916.3787778" --pretty
python3 verify_metadata.py --doi "10.1109/cain66642.2025.00039" --pretty
python3 verify_metadata.py --doi "10.18653/v1/2025.emnlp-industry.62" --pretty
```

- Structural Testing、CAIN Chaos Engineering 和 Agent vs. Agent：Crossref/OpenAlex DOI、标题和年份一致，标为已核验。
- SpecOps：Crossref 返回精确 DOI/标题，OpenAlex 未在本次查询中返回匹配，标为部分核验。
- 预印本按 arXiv ID 保留；没有正式 DOI 时不伪造 venue 或出版字段。

BibTeX 只为上述四个有可核验 DOI 的候选新增条目。其他预印本暂保留在证据表/watchlist，避免未解决字段进入引用库。

## 6. 证据使用限制

- 实时增量候选当前是摘要或元数据证据，未用于主综述中的细节性实验结论。
- 主综述的详细方法结论来自仓库已有全文笔记；专用证据表中 VeriGrey 明确标为摘要级前沿。
- 引用数只是时间敏感的发现信号，本轮没有用它单独决定代表性或排名。
- 学术数据库对 2026 新论文有收录滞后，DBLP 又在本轮失败；因此该检索是截止日期的高覆盖叙述综述，不声称系统综述式的绝对穷尽。
