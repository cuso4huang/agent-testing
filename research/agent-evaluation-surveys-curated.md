# 智能体评测与测试综述论文：精选清单

> 检索与核验日期：2026-08-13。范围聚焦 LLM/Agentic AI 的评测、测试、验证、安全评估和 benchmark 方法学。排序优先考虑：正式发表与同行评审、综述方法透明度、与“测试/评测”问题的直接相关性、开放全文，以及是否有配套开源资料。

> 已完成核心综述全文阅读及原始论文反向追踪，详细证据地图见 `research/survey-to-primary-agent-testing-map.md`。

## 1. 最值得优先阅读的五篇

| 优先级 | 论文 | 状态 | 为什么值得读 | 开放性 |
|---|---|---|---|---|
| S | [A Survey on Evaluation of LLM-based Agents](https://aclanthology.org/2026.findings-acl.1330/) | Findings of ACL 2026；DOI `10.18653/v1/2026.findings-acl.1330` | 当前最合适的总入口。覆盖规划、工具使用、自反思、记忆、Web、软件工程、科学、对话、通用 agent 和评测框架，并讨论 cost、safety、robustness 与细粒度评测缺口。 | [开放 PDF](https://aclanthology.org/2026.findings-acl.1330.pdf)；[官方配套 GitHub 阅读清单](https://github.com/Asaf-Yehudai/LLM-Agent-Evaluation-Survey) |
| S | [Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/abs/2507.21504) | KDD 2025；DOI `10.1145/3711896.3736570` | 用“评什么”和“怎样评”组成二维分类，特别适合建立论文或项目的评测框架；还覆盖企业中的权限、合规、长时交互和可靠性。 | [开放 arXiv PDF](https://arxiv.org/pdf/2507.21504)；未发现论文作者维护的专用代码仓库；有[开放教程材料](https://sap-samples.github.io/llm-agents-eval-tutorial/2025_KDD_Evaluation_and_Benchmarking_of_LLM_Agents.pdf) |
| S | [Evolutionary Perspectives on the Evaluation of LLM-Based AI Agents: A Comprehensive Survey](https://arxiv.org/abs/2506.11102) | Frontiers of Computer Science 2026；DOI `10.1007/s11704-026-51590-2` | 明确区分 chatbot 与 agent，从复杂环境、多源指令、动态反馈、多模态感知和高级能力解释 benchmark 如何演进；适合写“为什么普通 LLM 评测不够”。 | [开放 arXiv PDF](https://arxiv.org/pdf/2506.11102)；未发现明确的官方配套代码库 |
| S | [From benchmarks to deployment: a comprehensive review of agentic AI evaluation](https://doi.org/10.1007/s10462-026-11571-0) | Artificial Intelligence Review 2026 | 采用 PRISMA、明确检索式和质量评估，集中分析 15 个代表性 agent benchmark；在“系统综述方法严谨性”上比普通 narrative survey 更强。 | Springer 页面可读；是否可直接下载 PDF 取决于页面开放状态；未发现官方代码仓库 |
| S | [The Attack and Defense Landscape of Agentic AI: A Comprehensive Survey](https://arxiv.org/abs/2603.11088) | USENIX Security 2026 正式 SoK 的扩展/更新版本 | 从 agent 系统设计空间、攻击面、防御层和案例研究组织安全知识。适合作为安全测试、威胁模型和防御评测的主综述。 | [开放 arXiv PDF](https://arxiv.org/pdf/2603.11088)；[USENIX 正式页面](https://www.usenix.org/conference/usenixsecurity26/presentation/kim-juhee-agentic)；可配合 [Awesome Agent Security](https://github.com/ucsb-mlsec/Awesome-Agent-Security) 阅读 |

### 建议阅读顺序

1. ACL 2026：获得完整领域地图和 benchmark 索引。
2. KDD 2025：建立“评什么/怎么评”的方法框架。
3. FCS 2026：理解 agent 评测相对 chatbot 评测的演化。
4. PRISMA 系统综述：核查代表 benchmark 的选择依据和部署差距。
5. USENIX SoK：补齐攻击面、安全测试与防御验证。

## 2. 高质量专题综述

| 专题 | 论文 | 价值 | 证据/开放性判断 |
|---|---|---|---|
| 多轮对话 agent | [Evaluating LLM-based Agents for Multi-Turn Conversations: A Survey](https://arxiv.org/abs/2503.22458) | PRISMA-inspired，检索近 250 个来源；用“评什么/怎么评”覆盖任务完成、响应质量、用户体验、记忆、规划、工具集成、人工/自动/混合/自评方法。 | arXiv 开放全文；当前按高质量预印本使用，未核验正式出版版本，也未发现官方配套仓库 |
| GUI/电脑操作安全 | [A Survey on the Safety and Security Threats of Computer-Using Agents: JARVIS or Ultron?](https://arxiv.org/abs/2505.10924) | 聚焦桌面、浏览器和移动 agent；包含威胁、防御、benchmark、数据集和评测指标。 | arXiv 开放全文；当前正式出版状态需继续跟踪 |
| 长时、状态化安全 | [Toward Secure LLM Agents: Threat Surfaces, Attacks, Defenses, and Evaluation](https://arxiv.org/abs/2606.10749) | 综合 247 篇论文，以信息流、委托权限、持久状态和 agent 生命周期组织攻击、防御与评测；特别指出长期状态、多 agent 传播和部署敏感风险覆盖不足。 | 2026 arXiv 预印本，开放全文；新、覆盖广，但尚不应替代正式 USENIX SoK |
| 多智能体系统 | [Large Language Model based Multi-Agents: A Survey of Progress and Challenges](https://arxiv.org/abs/2402.01680) | 适合补充协作、通信、角色、拓扑和多智能体评测问题；不是专门的测试综述。 | arXiv 开放全文，并声明维护配套开源论文列表 |
| OS/GUI agent | [OS Agents: A Survey on MLLM-based Agents for Computer, Phone and Browser Use](https://github.com/OS-Agent-Survey/OS-Agent-Survey) | ACL 2025 Oral；覆盖 computer、phone、browser agent 的方法、能力与 benchmark，是 GUI/OS 场景的重要入口。 | 官方 GitHub 提供论文和持续整理的论文/benchmark 资源 |

## 3. 可作为背景，但不应代替评测综述

以下论文质量或影响力可能不错，但主体是 agent 架构、方法或应用，不是测试方法学。适合写背景章节，不适合承担“当前如何测试智能体”的核心论证。

| 论文/资源 | 使用方式 |
|---|---|
| [A Survey on Large Language Model based Autonomous Agents](https://github.com/paitesanshi/llm-agent-survey) | 用于 profile、memory、planning、action 的通用 agent 架构；有维护良好的开源资料库，但评测只是其中一节。 |
| [Large Language Model Agent: A Survey on Methodology, Applications and Challenges](https://arxiv.org/abs/2503.21460) | 用于 agent 构造、协作和演化背景；配套 [Awesome Agent Papers](https://github.com/luo-junyu/Awesome-Agent-Papers)。 |
| [A Review of Prominent Paradigms for LLM-Based Agents](https://arxiv.org/abs/2406.05804) | 用于工具/RAG、规划和反馈学习范式；不是 benchmark/test survey。 |

## 4. 如何理解“有开源”

不能把“PDF 免费下载”和“研究配套开源”混为一谈。本清单采用三级标记：

1. **开放全文**：ACL Anthology、arXiv、USENIX 等可合法直接阅读 PDF。
2. **开放资料库**：作者维护 GitHub 阅读清单、benchmark 索引或数据表，但不一定包含可执行代码。
3. **开源实现**：论文提供 benchmark、数据、harness 或评测代码，可以复现实验。

综述论文通常没有“算法代码”，因此最有价值的开源形式往往是持续维护的文献/benchmark 数据库。就这一标准而言，目前最佳入口是：

- [LLM-Agent-Evaluation-Survey](https://github.com/Asaf-Yehudai/LLM-Agent-Evaluation-Survey)：与你给出的 ACL 2026 论文直接配套，最相关。
- [OS-Agent-Survey](https://github.com/OS-Agent-Survey/OS-Agent-Survey)：GUI/浏览器/手机 agent 专题质量较高。
- [Awesome-Agent-Security](https://github.com/ucsb-mlsec/Awesome-Agent-Security)：安全论文与 benchmark 的补充索引。
- [Awesome Auditable AI](https://github.com/yzhao062/awesome-auditable-ai)：偏审计、可观测性、评测和治理，适合寻找测试工程方向。
- [LLM-Agent-Survey](https://github.com/paitesanshi/llm-agent-survey)：通用 agent 背景资料丰富，但测试针对性低于 ACL 配套仓库。

## 5. 各综述之间的覆盖差异

| 问题 | ACL 2026 | KDD 2025 | FCS 2026 | PRISMA Review | USENIX SoK | 多轮综述 |
|---|---:|---:|---:|---:|---:|---:|
| 通用能力与 benchmark | 强 | 强 | 强 | 中 | 弱 | 中 |
| 评测过程与指标 | 强 | 强 | 强 | 强 | 中 | 强 |
| 工程/企业部署 | 中 | 强 | 中 | 强 | 强 | 中 |
| 安全与攻击测试 | 中 | 中 | 中 | 中 | 强 | 中 |
| 记忆与长时交互 | 中 | 强 | 中 | 中 | 强 | 强 |
| 多智能体 | 中 | 中 | 中 | 弱 | 强 | 弱 |
| 系统综述方法透明度 | 中 | 中 | 中 | 强 | 强 | 强 |
| 官方开放资料库 | 强 | 弱 | 未发现 | 未发现 | 中 | 未发现 |

## 6. 推荐形成的核心参考集合

如果只保留一个紧凑而质量较高的综述集合，建议使用以下 8 篇：

1. Yehudai et al., *A Survey on Evaluation of LLM-based Agents*, Findings of ACL 2026。
2. Mohammadi et al., *Evaluation and Benchmarking of LLM Agents: A Survey*, KDD 2025。
3. Zhu et al., *Evolutionary Perspectives on the Evaluation of LLM-Based AI Agents*, FCS 2026。
4. *From benchmarks to deployment: a comprehensive review of agentic AI evaluation*, Artificial Intelligence Review 2026。
5. Kim et al., *The Attack and Defense Landscape of Agentic AI*, USENIX Security 2026。
6. Guan et al., *Evaluating LLM-based Agents for Multi-Turn Conversations*, arXiv 2025。
7. Chen et al., *JARVIS or Ultron?*, arXiv 2025。
8. Ling et al., *Toward Secure LLM Agents*, arXiv 2026。

其中前五篇适合作为正式综述主干；后三篇作为多轮、GUI 和长期安全专题补充。引用具体 benchmark 实验结果时，仍应回到 benchmark 原论文，而不是只引用综述的二手概括。

## 7. 检索限制

- 新近 2026 论文在 Crossref/OpenAlex 的收录可能延迟，数据库 HTTP 429 也会造成单源核验；“未核验正式版本”不等于论文无效。
- GitHub 搜索结果只能证明公开仓库存在，不能单凭 star 数判断论文质量；本清单优先判断是否为作者官方配套、是否与论文分类结构一致。
- arXiv 上标题包含 `survey` 的论文很多，但缺少明确检索过程、纳排标准或正式发表记录的，未进入首选层。
- 本清单聚焦 LLM agent。传统 BDI、多智能体模型检查和强化学习 agent testing 综述未纳入，除非其方法直接被 LLM-agent 工作采用。
