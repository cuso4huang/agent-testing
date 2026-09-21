# 2026 年智能体测试顶会论文与代码汇总

汇总日期：2026-09-02

本报告合并：

- 《2026年智能体测试顶会专项复查》：逐会扫描官方 accepted papers/program；
- 《2026软件工程智能体测试论文代码审计》：逐篇检查正文、Data Availability、Artifact Evaluation、GitHub、Zenodo、Figshare 和作者主页。

## 1. 口径与状态

### 相关性

- **A：直接测试智能体**——被测对象是 agent、agent framework、轨迹、工具链、MCP、记忆或多智能体系统。
- **B：智能体执行测试**——agent 用于 GUI/API/安全测试、fuzzing、concolic execution、验证或漏洞复现。
- **C：宽口径**——LLM 驱动测试生成、oracle、failure diagnosis，但自主性不明显。

### 代码状态

- `verified_code`：代码仓库已通过论文正文、会议页面、作者页面或 README 与论文准确对应。
- `verified_artifact`：公开复现包已核实，可能位于 Zenodo/Figshare，或以 Docker/数据包形式存在。
- `broken_official_link`：论文明确给出代码链接，但当前失效。
- `pending_verification`：可能存在代码或项目页，但尚未完成准确归属核验。
- `no_public_artifact_found`：截至检索日未找到公开 Artifact；不代表作者没有向审稿人提供私有材料。

## 2. 会议状态

| 领域 | 会议 | 状态 |
|---|---|---|
| 软件工程 | ICSE、FSE、ASE、ISSTA、ICST | 官方录用列表/日程已公布并扫描 |
| AI/NLP | ICLR、ICML、AAAI、ACL/EACL、IJCAI-ECAI | 正式 proceedings 或官方 accepted list 已扫描 |
| AI/NLP | EMNLP | accepted main list 已发布；正式 Anthology/DOI 尚未发布 |
| AI/NLP | NeurIPS | 论文通知日为 2026-09-24；截至当前不能列任何正式录用论文 |
| 安全 | IEEE S&P、USENIX Security、NDSS | 官方 program/proceedings 已扫描 |
| 安全 | ACM CCS | accepted papers 已公布；部分 DOI、PDF 和 Artifact 尚未齐全 |

## 3. 软件工程顶会

### 3.1 代码已核实的核心论文

| 论文 | Venue/Track | 类别 | 方法概要 | 代码/Artifact |
|---|---|---:|---|---|
| Breaking Single-Tester Limits / MAdroid | ICSE Research | B | 多个 tester agents 扮演不同用户，协作测试多用户功能 | [代码](https://github.com/sidongfeng/MAdroid) |
| Testora | ICSE Research | C | 生成测试、差分执行，以 PR 自然语言意图为 regression oracle | [代码](https://github.com/michaelpradel/Testora) |
| TestWeaver | ICSE Research | C | execution-aware、feedback-driven 回归测试生成 | [代码](https://github.com/FSoft-AI4Code/TestWeaver) |
| SAFE | ICSE Research | B/C | 从多模态事故材料生成可重放 ADS 测试场景并 self-validate | [代码/数据](https://github.com/Siwei-Luo-MQ/SAFE-ADS-Testing) |
| WebTestPilot | FSE Research | B | 根据自然语言规格自主执行 Web E2E 测试，并推断 GUI oracle | [代码](https://github.com/code-philia/WebTestPilot) |
| Failure-Based Testing for DRL Agents / PRT | FSE Research | A | 用失败信息替代高 reward 信号，指导 Prior Random Testing | [代码](https://github.com/Avagnes/PRT-DRL-Experiments) |
| IntentTester | FSE Research | B | 多 agent 完成测试意图提取、跨库迁移、执行与修复 | [代码](https://github.com/testmigrator/intenttest) |
| PersonaTester | FSE Research | B | 人格化 LLM 模拟不同众包测试人员 | [代码](https://github.com/iGUITest/PersonaTester) |
| Agentic Verification / AutoRocq | FSE Research | B | LLM proof agent 迭代验证程序 | [代码](https://github.com/NUS-Program-Verification/AutoRocq) |
| Event-B Agent | FSE Research | B | 根据模型检查和证明反馈修复 Event-B 模型 | [代码](https://github.com/HongshuW/EventB_Agent) / [Zenodo](https://doi.org/10.5281/zenodo.19642103) |
| AgentBound | FSE Research | A | MCP server 声明式访问控制和运行期执行边界 | [复现包](https://zenodo.org/records/19571298) |
| Datura | ISSTA Research | A | 渐进式红队测试 agent 工具调用链与 chained tool hijacking | [代码](https://github.com/ycshao12/Datura_RedTeaming_Testing) |
| LogicHunter | ISSTA Research | A | 规格驱动 fuzzing，并使用可查询文档/源码/状态的 agentic oracle | [代码](https://github.com/security-pride/LogicHunter) / [Zenodo](https://zenodo.org/records/21936443) |
| Test vs Mutant / AdverTest | ISSTA Research | B | tester 与 mutant agents 对抗演化，增强单元测试 | [复现包](https://github.com/jmueducn/AdverTest) |
| MuMuTestUp | ISSTA Research | B | mutation-guided multi-agent test-case update | [代码](https://github.com/crazyTang-cloud/MuMuTestUp) |
| Red-Teaming Coding Agents / TIPExploit | ISSTA Research | A | 从工具调用角度对 coding agents 进行红队测试 | [代码](https://github.com/TIPExploit/TIPExploit) |
| CAST | ISSTA Research | A/C | 编译器式系统测试 LLM compositional safety | [Artifact](https://zenodo.org/records/21010284) |
| RAG Metamorphic Mutation | ASE Research | A/C | 通过知识变异和11种 metamorphic operators 测试 RAG 系统 | [代码](https://github.com/dbr7/RAG-metamorphic-mutation) / [数据](https://figshare.com/s/96fc3abb168180c0a215) |
| COMA / Comattack | ASE Research | A | 黑盒攻击 prompt-compressed LLM agents | [Artifact](https://github.com/zsLiu2003/Comattack) |
| Metamorphic Testing of VLA-Enabled Robots | ICST Main | A | 使用 metamorphic relations 测试 VLA robotic agents | [代码](https://github.com/pablovalle/MT_of_VLAs) / [AE包](https://zenodo.org/records/18750977) |

补充但不是 Research Paper：

- GrantBox 是 FSE Ideas, Visions and Reflections：[代码](https://github.com/ZQ-Struggle/Agent-GrantBox)。
- TestAgent 是 FSE Tool Demonstration：[代码](https://github.com/iSEngLab/TestAgent-VSCode-Extension)。
- Robustness-Guided Requirement Falsification 有 [ISSTA Artifact](https://zenodo.org/records/21294060)。

### 3.2 相关但公开代码尚未找到或不可用

| 论文 | Venue | 状态 |
|---|---|---|
| An LLM Agentic Approach for Legal-Critical Software | ICSE | `no_public_artifact_found` |
| E-Test | ICSE | `broken_official_link`；正式 `E-Test-package` 返回404，仅找到FSE 2025早期版本 |
| AgentInspect | ISSTA | `no_public_artifact_found`；同名 TypeScript 项目是误匹配 |
| Learning from the Test / Delta | ISSTA | `no_public_artifact_found` |
| PAGENT | ISSTA | `no_public_artifact_found` |
| Understanding Bugs in Modern Agentic Frameworks | ASE | `no_public_artifact_found` |
| ARIA: Automated Red Teaming for Instruction Backdoors | ASE | `no_public_artifact_found` |
| SynerFuzz: Coordinated Multi-Agent Smart-Contract Fuzzing | ASE | `no_public_artifact_found` |
| Automated Lemma Discovery / LemmaNet | ASE | `no_public_artifact_found` |
| IntOAgent | ASE | `no_public_artifact_found` |
| Piece by Piece GUI Testing | ASE | `no_public_artifact_found` |
| To Think or Not to Think | ASE | `no_public_artifact_found` |

ASE 2026 Artifact Evaluation 在检索日仍未完全结束，以上状态需要后续复查。

## 4. AI/NLP 顶会

### 4.1 ICLR 2026

ICLR 2026 是今年最密集的 agent evaluation/testing 集群，正式论文超过20篇。

| 方向 | 代表论文 |
|---|---|
| 故障归因与调试 | AgenTracer、DoVer、Aegis、Talk-Evaluate-Diagnose |
| 软件与终端 agents | DevOps-Gym、Terminal-Bench、EXP-Bench、Process-Level Trajectory Evaluation |
| MCP/工具使用 | MCPMark、MCP-Bench、MCP-SafetyBench |
| computer-use agent 红队 | VPI-Bench、RedTeamCUA、ST-WebAgentBench、OpenApps |
| 安全与治理 | OpenAgentSafety、A2ASecBench、RedCodeAgent、Just Do It!? |
| 长期能力 | Gaia2、ManagerBench、agent memory evaluation、CyberGym |

已核实代码：

- [RedTeamCUA](https://github.com/OSU-NLP-Group/RedTeamCUA)：混合 Web–OS 沙箱与 RTC-Bench。
- [Terminal-Bench](https://github.com/jvpoulos/terminal-bench)：真实终端环境、程序化测试和 oracle。
- [MCPMark](https://github.com/eval-sys/mcpmark)：真实 MCP 工具环境压力测试。
- [MCP-SafetyBench](https://github.com/xjzzzzzzzz/MCPSafety)：MCP agent safety benchmark。

### 4.2 ICML 2026

| 论文 | 重点 | 代码状态 |
|---|---|---|
| AgentSuite | 审计 agent benchmark 的隐藏缺陷 | 待核验 |
| Agent Memory in Multi-Session Tasks | 状态化、跨 session memory evaluation | 待核验 |
| FormulaCode | 大型代码库上的 agentic optimization | 项目公开，仓库待核 |
| GameDevBench | 用游戏开发测试多模态软件开发 agents | [代码](https://github.com/waynchi/gamedevbench) |
| Implicit Intelligence | 测试 agent 对未明说约束的处理 | 待核验 |
| SafeHarbor | agent safety 的层级记忆 guardrail | [代码](https://github.com/ljj-cyber/SafeHarbor) |
| SafeLab | 科研机器人 embodied safety | 待核验 |
| AgentWebBench | multi-agent Web coordination | 项目公开，仓库待核 |

### 4.3 ACL/EACL、AAAI、IJCAI、EMNLP

- ACL Main：AgencyBench、SafeAgent、Plan-RewardBench。
- ACL Findings：AgenticEval、PerMemSafe、TraineeBench、SecureWebArena、ToolSafe/TS-Bench、ABC-Bench，以及作为追踪入口的 [Agent Evaluation Survey](https://aclanthology.org/2026.findings-acl.1330/)。
- EACL Long：[Agent-Testing Agent](https://aclanthology.org/2026.eacl-long.339/)，自动分析被测 agent、生成 persona 驱动对抗测试，并根据 judge 反馈提高难度。
- AAAI：MCP-AgentBench、ShoppingBench、AMS-IO-Bench/Agent。
- IJCAI-ECAI：ResearchEnvBench、role-playing agent safety、multi-agent RL probabilistic verification、人机协作 testbed。
- EMNLP accepted list：Misaligned Action Detection、IPIGuard、WebInject、Policy-Adherent Agent Red-Teaming、ToolSafety、Beyond Static Testbeds、Breaking Agents 等；正式 DOI/PDF 尚待 proceedings。
- NeurIPS 2026 尚未通知，暂不列论文。

## 5. 安全顶会

### 5.1 代码已核实核心集

| 论文 | Venue | 类别 | 方法 | 代码/Artifact |
|---|---|---:|---|---|
| MUZZLE | USENIX Security | A | 基于轨迹反馈，自适应红队测试 Web-agent indirect prompt injection | [代码](https://github.com/gsiros/muzzle) |
| Agentic Concolic Execution / ConcoLLMic | IEEE S&P | B | agent 与 concolic execution 结合生成路径触发输入 | [代码](https://github.com/ConcoLLMic/ConcoLLMic) |
| Cottontail | IEEE S&P | B | LLM-driven concolic execution 生成高度结构化输入 | [代码](https://github.com/Cottontail-Proj/cottontail) |
| Incalmo | IEEE S&P | B | 自主多主机网络红队测试 | [代码](https://github.com/bsinger98/incalmo) |
| FirmAgent | NDSS | B | fuzzing feedback 辅助 agent 发现固件漏洞并生成 PoC | [代码](https://github.com/vul337/FirmAgent) |
| ObliInjection | NDSS | A | multi-source data 下的 order-oblivious prompt injection | [代码](https://github.com/ReachalWang/ObliInjection) |
| CVE-Genie | CCS | B | multi-agent 自动复现 CVE | [代码](https://github.com/BUseclab/cve-genie) |
| PBFuzz | CCS | B | PLAN–IMPLEMENT–EXECUTE–REFLECT 的 agentic directed fuzzing | [代码](https://github.com/sgzeng/pbfuzz)；Zenodo `10.5281/zenodo.20769185` |
| MirrorGuard | CCS | A | simulation-to-real reasoning correction，保护 computer-use agents | [代码](https://github.com/WhitzardAgent/MirrorGuard) |

### 5.2 重要但代码仍待核验

- USENIX Security：AgentDoS、PANGOLIN、Bulbasaur、Malicious Agent Skills、AIOpsDoom。
- IEEE S&P：PromptLocate、agentic-browser site isolation、AI-agent permissions、dark-pattern effects。
- NDSS：ACE、SAGA、ToolHijacker、Chimera、Les Dissonances。
- CCS：BACAgent、Android GUI agent action-rebinding attacks、LLM-driven PDF JavaScript-engine fuzzing。

## 6. 跨领域方法演进

### 轨迹诊断与可执行 Oracle

AgentBoard/早期轨迹评测
→ AgenTracer、Aegis、DoVer
→ AgentInspect、LogicHunter
→ WebTestPilot。

研究重点从最终成功率转向步骤级归因、异常工具模拟、agent-specific coverage 和可执行 oracle。

### 工具链安全测试

早期 prompt-injection benchmark
→ ToolHijacker、ObliInjection
→ ACE、SAGA、MirrorGuard
→ MUZZLE、Datura、RedTeamCUA。

### Agentic Fuzzing

AgentFuzz（USENIX Security 2025）
→ AgentDoS、FirmAgent
→ PBFuzz、CVE-Genie、BACAgent。

### 多智能体执行软件测试

MAdroid/PersonaTester
→ IntentTester
→ Test-vs-Mutant、MuMuTestUp
→ SynerFuzz 等协同 fuzzing。

## 7. 最推荐复现的项目

如果研究目标是“智能体自身的测试”，优先：

1. LogicHunter
2. Datura
3. RedTeamCUA
4. MUZZLE
5. MCP-SafetyBench
6. RAG Metamorphic Mutation
7. COMA

如果研究目标是“使用智能体做测试”，优先：

1. WebTestPilot
2. MAdroid
3. PersonaTester
4. IntentTester
5. AdverTest
6. PBFuzz
7. CVE-Genie
8. ConcoLLMic/Cottontail

如果研究目标是“构建通用评测基础设施”，优先：

1. AgentSuite（代码待核）
2. Terminal-Bench
3. MCPMark
4. AgentInspect（代码待公开）
5. AgenTracer/Aegis/DoVer（代码待逐篇核验）

## 8. 数量总结与限制

- 软件工程严格相关论文约20篇；扩大至LLM测试生成、oracle和验证后超过40篇。
- 本轮重点审计的SE项目中：ICSE 4个公开实现、FSE 9/9、ISSTA 7个、ASE 2个、ICST 1个官方AE包。
- AI方向以ICLR 2026最密集；安全方向已经形成从benchmark到adaptive red teaming和agentic fuzzing的完整链条。
- `no_public_artifact_found` 只表示截至2026-09-02未发现公开材料。ASE、CCS、EMNLP等仍可能继续发布Artifact。
- NeurIPS 2026结果尚未公布，需要在2026-09-24之后增量更新。

