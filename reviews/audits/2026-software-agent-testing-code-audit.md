# 2026 软件工程智能体测试论文代码与 Artifact 审计

核验日期：2026-09-02

## 状态定义

- `verified_code`：论文正文、会议页面、作者页面或仓库 README 能把仓库与论文准确对应。
- `verified_artifact`：已找到公开复现包，可能是 Zenodo/Figshare/Docker，不一定是日常开发仓库。
- `broken_official_link`：论文明确给出公开链接，但当前失效。
- `no_public_artifact_found`：本轮已查官方 AE、正文、作者页、GitHub 和归档站，仍未找到；不代表作者从未向审稿人提交私有 artifact。
- `false_match`：发现同名项目，但作者、方法或论文身份不符。

## 1. ICSE 2026

| 论文 | 状态 | 代码/Artifact | 核验证据 |
|---|---|---|---|
| Breaking Single-Tester Limits: Multi-Agent LLMs for Multi-User Feature Testing | `verified_code` | [MAdroid](https://github.com/sidongfeng/MAdroid) | arXiv `2506.17539` 正文脚注明确给出 source code/dataset；README 的 Coordinator、Operator、Observer 与论文匹配 |
| An LLM Agentic Approach for Legal-Critical Software | `no_public_artifact_found` | — | arXiv `2509.13471`、IBM Research 和作者页面均未给代码/归档链接；精确标题和作者检索无匹配 |
| E-Test: E’er-Improving Test Suites | `broken_official_link` | 论文给出的 `github.com/ketaiq/E-Test-package` 当前 404 | 找到 [FSE 2025 SRC 早期包](https://github.com/ketaiq/etest-replication-package-fse25src)，但 README 明确对应早期版本，不能冒充 ICSE 2026 完整 Artifact |
| Testora | `verified_code` | [michaelpradel/Testora](https://github.com/michaelpradel/Testora) | 论文脚注直接链接；含 Docker/devcontainer、evaluation scripts 与 paper results，MIT |
| TestWeaver | `verified_code` | [FSoft-AI4Code/TestWeaver](https://github.com/FSoft-AI4Code/TestWeaver) | arXiv `2508.01255` Data Availability 直接链接；含主程序、数据准备、ablation 和 baselines |
| SAFE: Scenario-Driven ADS Testing | `verified_code` | [SAFE-ADS-Testing](https://github.com/Siwei-Luo-MQ/SAFE-ADS-Testing) | ICSE 页面给出的匿名链接已不可访问，但作者仓库题名、流程、Crash dataset、MetaDrive/BeamNG 与论文一致 |

ICSE 小结：6 篇中 4 篇当前代码可用，1 篇正式链接失效但有早期包，1 篇未发现公开 Artifact。

## 2. FSE 2026

| 论文 | Track | 状态 | 代码/Artifact |
|---|---|---|---|
| WebTestPilot | Research | `verified_code` | [code-philia/WebTestPilot](https://github.com/code-philia/WebTestPilot) |
| Failure-Based Testing for DRL Agents / PRT | Research | `verified_code` | [Avagnes/PRT-DRL-Experiments](https://github.com/Avagnes/PRT-DRL-Experiments) |
| IntentTester | Research | `verified_code` | [testmigrator/intenttest](https://github.com/testmigrator/intenttest) |
| Towards Automated Crowdsourced Testing via Personified-LLM / PersonaTester | Research | `verified_code` | [iGUITest/PersonaTester](https://github.com/iGUITest/PersonaTester) |
| Agentic Verification of Software Systems / AutoRocq | Research | `verified_code` | [NUS-Program-Verification/AutoRocq](https://github.com/NUS-Program-Verification/AutoRocq) |
| Event-B Agent | Research | `verified_code` + `verified_artifact` | [EventB_Agent](https://github.com/HongshuW/EventB_Agent)；[Zenodo DOI](https://doi.org/10.5281/zenodo.19642103) |
| AgentBound | Research | `verified_artifact` | [Zenodo replication package](https://zenodo.org/records/19571298)，DOI `10.5281/zenodo.19571298` |
| Evaluating Privilege Usage of Agents / GrantBox | **IVR** | `verified_code` | [Agent-GrantBox](https://github.com/ZQ-Struggle/Agent-GrantBox) |
| TestAgent | **Tool Demonstration** | `verified_code` | [TestAgent VS Code Extension](https://github.com/iSEngLab/TestAgent-VSCode-Extension) |

FSE 小结：本轮目标 9/9 找到公开实现或复现包。其中严格 Research Papers 为7篇；GrantBox 是 Ideas, Visions and Reflections，TestAgent 是 Tool Demonstration。

需要排除的误匹配：[dortort/agent-bound](https://github.com/dortort/agent-bound) 自称受论文启发，作者身份不符，不是 AgentBound 官方实现。

## 3. ISSTA 2026

| 论文 | 状态 | 代码/Artifact | 核验证据 |
|---|---|---|---|
| AgentInspect | `no_public_artifact_found` | — | `rajudandigam/agent-inspect` 是无关 TypeScript 调试器，属于 `false_match` |
| Datura | `verified_code` | [Datura_RedTeaming_Testing](https://github.com/ycshao12/Datura_RedTeaming_Testing) | README 明确为论文 Artifact；README 仍保留 camera-ready 改题前的旧副标题，但作者与方法链一致 |
| LogicHunter | `verified_code` + `verified_artifact` | [GitHub](https://github.com/security-pride/LogicHunter)；[Zenodo v1.0.0](https://zenodo.org/records/21936443)，DOI `10.5281/zenodo.21936443` | Zenodo 明确写明伴随 ISSTA 2026 论文，并链接 paper-version tag |
| Test vs Mutant / AdverTest | `verified_artifact` | [jmueducn/AdverTest](https://github.com/jmueducn/AdverTest) | README 明确为论文 replication package；Data Availability 亦指向该仓库 |
| MuMuTestUp | `verified_code` | [crazyTang-cloud/MuMuTestUp](https://github.com/crazyTang-cloud/MuMuTestUp) | README 明确写明是论文的 official implementation |
| Learning from the Test / Delta | `no_public_artifact_found` | — | arXiv `2608.22284` 可核实论文；CatalyzeX 仍显示 Request Code |
| PAGENT | `no_public_artifact_found` | — | arXiv `2604.07624` 与作者页均未发现实现链接 |
| Red-Teaming Coding Agents from a Tool-Invocation Perspective | `verified_code` | [TIPExploit](https://github.com/TIPExploit/TIPExploit) | 仓库 description 写出论文全名和 ISSTA’26 |
| On the Role of LLMs in Robustness-Guided Requirement Falsification | `verified_artifact` | [Zenodo](https://zenodo.org/records/21294060) | 4.9 GB Docker/实验/Notebook Artifact Evaluation package |
| CAST | `verified_artifact` | [Zenodo](https://zenodo.org/records/21010284) | 包含完整 reference implementation、CAIR、oracle、dataset loaders 和 baseline testers |

ISSTA 小结：此前“普通 GitHub 搜索”漏掉了大量较晚发布的 Zenodo/AE 包。核心六篇 AgentInspect/Datura/LogicHunter/Test-vs-Mutant/MuMuTestUp/Delta 中，当前4篇已有公开实现或复现包。

## 4. ASE 2026

| 论文 | 状态 | 代码/Artifact | 备注 |
|---|---|---|---|
| Understanding Bugs in Modern Agentic Frameworks | `no_public_artifact_found` | — | 可能后续发布 bug dataset；当前未检出 |
| Breaking Customized LLMs for Coding / ARIA | `no_public_artifact_found` | — | arXiv `2608.05659` 已公开，代码未检出 |
| Breaking the Isolation / SynerFuzz | `no_public_artifact_found` | — | DOI `10.1145/3832783.3837466`；作者页仅有 Paper/Bib |
| Automated Lemma Discovery / LemmaNet | `no_public_artifact_found` | — | 作者页面该论文仅列 PDF，没有 Code 链接 |
| IntOAgent | `no_public_artifact_found` | — | 通讯作者页面仅列论文 |
| Piece by Piece GUI Testing | `no_public_artifact_found` | — | 作者/实验室索引未发现仓库 |
| When Knowledge Changes: Metamorphic Testing of RAG Systems | `verified_code` + data | [RAG-metamorphic-mutation](https://github.com/dbr7/RAG-metamorphic-mutation)；[Figshare outputs](https://figshare.com/s/96fc3abb168180c0a215) | README 含完整 pipeline、11种 mutation operators |
| When Compression Becomes an Attack Surface / COMA | `verified_artifact` | [zsLiu2003/Comattack](https://github.com/zsLiu2003/Comattack) | README 明确为 ASE’26 Artifact，含 RQ1–RQ5 reproduction scripts |
| To Think or Not to Think | `no_public_artifact_found` | — | 不要误配 NeurIPS 2025 的 `wangyuenlp/underthinking` |

ASE 小结：目前2/9找到公开实现。ASE 2026 Artifact Evaluation 仍在进行，major-revision artifact 的最终通知日期晚于本次检索，因此其余项目应继续观察。

## 5. ICST 2026

| 论文 | 状态 | 代码/Artifact | 核验证据 |
|---|---|---|---|
| Metamorphic Testing of Vision-Language Action-Enabled Robots | `verified_code` + `verified_artifact` | [GitHub](https://github.com/pablovalle/MT_of_VLAs)；[Zenodo](https://zenodo.org/records/18750977)，DOI `10.5281/zenodo.18750977` | ICST 官方 Artifact Evaluation 已评审并授予徽章；含源码、数据、Docker、结果和9.5GB camera-ready package |

## 6. 汇总

| Venue | 本轮目标 | 已核实公开代码/Artifact | 链接失效/待恢复 | 未发现公开 Artifact |
|---|---:|---:|---:|---:|
| ICSE | 6 | 4 | 1 | 1 |
| FSE | 9（含1 IVR、1 Tool Demo） | 9 | 0 | 0 |
| ISSTA | 10（含宽口径2篇） | 7 | 0 | 3 |
| ASE | 9 | 2 | 0 | 7 |
| ICST | 1个最直接目标 | 1 | 0 | 0 |

最值得直接下载复现的新增项目：LogicHunter、WebTestPilot、PRT、IntentTester、PersonaTester、AutoRocq、Event-B Agent、MAdroid、Testora、TestWeaver、Datura、AdverTest、TIPExploit 和 ICST VLA Artifact。
