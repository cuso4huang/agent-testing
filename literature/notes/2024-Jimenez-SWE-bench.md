# SWE-bench：结构化阅读笔记

## 1. 基本信息

- 标题：*SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*
- 作者：Carlos E. Jimenez；John Yang；Alexander Wettig；Shunyu Yao；Kexin Pei；Ofir Press；Karthik Narasimhan
- 正式发表年份：2024
- 正式发表：International Conference on Learning Representations（ICLR 2024，Oral）
- DOI：未发现可核验的 ICLR 正式出版 DOI；arXiv DataCite DOI 为 `10.48550/arXiv.2310.06770`
- arXiv：`2310.06770`
- 正式版本：https://proceedings.iclr.cc/paper_files/paper/2024/hash/edac78c3e300629acfe6cbe9ca88fb84-Abstract-Conference.html
- OpenReview：https://openreview.net/forum?id=VTF8yNQM66
- 开放全文：https://arxiv.org/abs/2310.06770
- 代码、数据和评测框架：https://github.com/SWE-bench/SWE-bench
- 项目与排行榜：https://www.swebench.com/
- 版本关系：论文先以 arXiv 预印本发布，后正式发表于 ICLR 2024。本项目保存的 PDF 是 `arXiv:2310.06770v3`（2024-11-11），页眉标注“Published as a conference paper at ICLR 2024”，并加入 Claude 3 Opus、GPT-4-turbo 和 SWE-bench Lite 等会后更新。因此正式引用应优先使用 ICLR 2024 版本；引用 v3 新增数字时应明确它们来自会后修订版，而不能默认等同于最初会议版本。

## 2. 研究问题

论文希望把代码能力评测从独立函数生成推进到真实仓库中的 issue 修复，核心问题包括：

1. 能否从公开 GitHub issue、修复 PR 和测试历史中自动构造可执行的软件工程任务？
2. 给定 issue 文本和修复前仓库，语言模型能否定位相关文件、理解跨模块关系并生成可应用的补丁？
3. 真实测试能否作为自动 oracle，同时检查问题是否修复及既有功能是否回归？
4. 检索质量、上下文长度、模型规模和领域微调分别如何影响仓库级修复能力？
5. 当最终 `resolved` 很低时，如何进一步区分补丁无法应用、未修复、部分修复、破坏既有行为等失败？

需要注意，原论文的主要 baseline 是“检索代码后一次生成补丁”的语言模型管线，并非完整的自主代码智能体。SWE-bench 提供的仓库、issue 和执行式 oracle 后来成为代码智能体的重要测试环境，但不能把原始 baseline 结果直接解释成对规划、反思或多轮工具使用智能体的实验结论。

## 3. 被测试的智能体类型

原实验评测以下仓库级补丁生成系统：

- ChatGPT-3.5：`gpt-3.5-turbo-16k-0613`；
- GPT-4：`gpt-4-32k-0613`；
- Claude 2；
- 基于 CodeLlama-Python 微调的 SWE-Llama 7B 和 13B；
- arXiv v3 结果表另加入 Claude 3 Opus 和 GPT-4-turbo。

系统先用 BM25 或 oracle 文件集合选取上下文，再让模型一次输出 patch；没有交互式 shell、测试—修复循环、长期记忆或自主工具调用。因此其直接对象更准确地说是长上下文代码模型/单步修复管线。基准本身则适用于能浏览仓库、运行测试、编辑文件并迭代修复的代码智能体。

## 4. 测试或评估方法

### 4.1 真实 issue 到可执行测试任务

构建流程分三阶段（Section 2.1；Figure 2）：

1. 从 12 个以 Python 为主的热门开源仓库抓取约 90,000 个 PR；
2. 保留已合并、关联一个被解决 issue 且修改测试文件的 PR；
3. 在 PR 的 base commit 上先加入测试改动，再比较完整修复前后的执行结果；保留至少有一个测试从失败转为通过、且仓库能安装和执行的实例。

最终得到 2,294 个任务。每个任务向系统提供 issue 文本和 base commit 的代码库，要求生成统一 diff patch。

### 4.2 双集合执行式 oracle

论文把评估测试分为：

- **FAIL_TO_PASS（F2P）**：修复前失败、参考 PR 后通过，用于判断 issue 是否被修复；
- **PASS_TO_PASS（P2P）**：修复前后均通过，用于发现模型补丁引入的回归。

模型 patch 先由 Unix `patch` 应用到仓库，再执行任务对应测试；只有 patch 成功应用且 F2P、P2P 均满足要求时才记为 resolved（Section 2.2；Appendix A.4）。Appendix Table 22 进一步根据两组测试通过比例划分 Resolved、Breaking Resolved、Partially Resolved、WIP、No-Op 和 Regression。

### 4.3 上下文检索对照

- BM25：对仓库非测试文件建立文档，文件路径前置到内容中；测试 13K、27K、50K 最大上下文；
- Oracle retrieval：只提供参考 PR 实际修改的非测试文件路径，用作定位上界而非可部署方法；
- Oracle-collapsed：进一步只保留 gold 修改位置附近约 ±15 行，用于分析无关上下文的影响。

Oracle 使用答案补丁中的文件信息，存在标签泄漏，不能与真实端到端系统成绩混为一谈。

### 4.4 训练开放模型

作者另构建 SWE-bench-train：约 19,000 个来自 37 个、与评测仓库不重叠的仓库的 issue-PR 对；训练集不要求 PR 修改测试。对序列长度筛选后使用约 10,000 个实例，以 LoRA 微调 CodeLlama-Python 7B/13B，得到 SWE-Llama（Section 3；Appendix B）。

## 5. 数据集、环境或基准

- **SWE-bench**：2,294 个任务，来自 12 个流行 Python 仓库。
- **SWE-bench Lite**：从完整版筛选的 300 个较自包含、侧重功能性 bug 修复的实例，覆盖 11 个仓库（Section 2.4；Appendix A.7）。
- **SWE-bench-train**：19,000 个非测试约束的训练实例，来自与评测集不重叠的 37 个仓库。
- 平均 issue 长 195.1 词；每个仓库快照平均有 3,010 个非测试文件、约 43.8 万行非测试代码（Table 1）。
- 参考补丁平均修改 32.8 行、1.7 个文件和 3 个函数（Table 1）。
- 每个实例平均有 9.1 个 F2P 测试、120.8 个总测试；正文另报告 40% 实例至少有两个 F2P 测试，额外回归测试中位数为 51（Section 2.3）。
- 每个任务使用特定 base commit、安装配置和测试命令，因而测试对象不只是文本数据，还包括可执行的软件环境。

## 6. 评价指标

- `% Resolved`：完整解决的任务数占比，是主指标；
- `% Apply`：模型 patch 能成功应用的比例；
- F2P/P2P 测试通过比例；
- Resolved、Breaking Resolved、Partially Resolved、WIP、No-Op、Regression 六类执行结果；
- BM25 对 gold 修改文件的平均召回率、全部文件召回率和任一文件召回率；
- 按仓库、issue 时间、patch 长度和代码复杂度的分组分析；
- 生成 patch 与 gold patch 的修改文件数、函数数、代码行数；
- Radon 圈复杂度和 Halstead 指标等补充代码质量分析；
- 训练损失和 held-out validation loss，用于选择 SWE-Llama checkpoint。

`Resolved` 是强而清晰的执行式指标，但不是完整质量证明：现有测试可能漏掉边界行为，且不会直接评价效率、可读性、可维护性、安全性或最小权限。

## 7. 实验设计

### 7.1 推理管线

- 输入提示由 issue、检索到的代码文件、格式说明和示例 patch 组成（Section 4；Appendix D.3）。
- BM25 分别在 13K、27K 和 50K 上下文预算下运行；不同模型实际上下文上限不同。
- 因生成昂贵，每个模型对每个任务只生成一个 patch，并统一使用 greedy decoding（Appendix D.2）。
- GPT-4 因预算限制只在随机 25% 子集（574 个任务）的 oracle 和 BM25-27K 设置运行（Appendix Table 18 注释；Section C.3）。

因此论文没有测量同一任务多次运行的方差、温度敏感性、`pass@k` 或智能体重试稳定性；不同闭源模型的全量结果也并非完全同样本比较。

### 7.2 环境执行

数据构建为每个任务创建隔离环境，在 base commit 安装仓库并运行测试；安装或运行错误的候选任务被过滤。评测时应用生成 patch 后重跑相应 F2P/P2P 测试（Appendix A.2、A.4）。

### 7.3 SWE-Llama 训练

- LoRA：`r=16`、`alpha=16`、dropout 0.05，作用于注意力层 query/key/value/output projection；
- 学习率 `6e-4`，每个梯度步 batch 32，最多 4 epochs；
- 每 50 steps 保存 checkpoint，以 100 个 held-out 实例的 validation loss 选最佳版本；
- 7B 使用 4 张 A100 训练约 20 小时，13B 使用 8 张 A100 约 47 小时（Appendix B.1）。

## 8. 主要发现

### 8.1 真实仓库修复远难于短函数生成

在 arXiv v3 的 BM25 主表中（Table 5）：

| 模型 | SWE-bench Resolved | Patch Apply | Lite Resolved |
|---|---:|---:|---:|
| Claude 3 Opus | 3.79% | 46.56% | 4.33% |
| Claude 2 | 1.97% | 43.07% | 3.00% |
| ChatGPT-3.5 | 0.17% | 26.33% | 0.33% |
| GPT-4-turbo | 1.31% | 26.90% | 2.67% |
| SWE-Llama 7B | 0.70% | 51.74% | 1.33% |
| SWE-Llama 13B | 0.70% | 53.62% | 1.00% |

正文仍保留原会议阶段的叙述：“Claude 2 以约 1.96% 为最佳”。v3 表格已加入后续模型且 Claude 3 Opus 为 3.79%，这是会后修订造成的时间切片差异，综述中应标明版本，不能同时把两者都写成同一实验时点的“最佳”。

### 8.2 文件定位是重要瓶颈，但知道文件仍远远不够

- BM25 在 13K/27K/50K 下对 gold 文件的平均召回率为 29.58%/44.41%/51.06%；27K 时召回全部 gold 文件的任务仅 39.83%，召回至少一个为 51.27%（Table 3）。
- Oracle retrieval 下，Claude 2 resolved 提升至 4.80%，SWE-Llama 13B 为 3.97%，GPT-4 在 25% 子集为 1.74%（Appendix Table 18）。
- Oracle-collapsed 进一步减少无关上下文后，v3 Table 6 报告 Claude 3 Opus 9.39%、Claude 2 5.93%、GPT-4 3.40%、ChatGPT-3.5 1.09%。

这些对照表明定位与上下文噪声显著影响结果，但即使泄漏 gold 文件/位置，成功率依然很低，说明代码理解、跨模块推理和正确修改仍是独立瓶颈。Oracle 结果只能做诊断上界。

### 8.3 更多上下文不保证更好

Table 2 中 Claude 2 的 BM25 resolved 从 13K 的 1.96% 降到 27K 的 1.87% 和 50K 的 1.22%；SWE-Llama 也呈下降。与此同时 BM25 文件召回随上下文增加而上升。这一反向变化支持“无关代码会干扰模型”的解释，但实验没有单独随机化上下文质量，不能证明长度本身是唯一因果因素。

### 8.4 Patch 可应用不等于问题解决

Table 5 中多个模型的 `% Apply` 为 26%-54%，而 resolved 低于 4%。Appendix Tables 22-23 显示，未解决但可应用的 patch 大量落在 No-Op 或 Regression。作者对各模型统计发现，未解决结果中多数为没有修复 F2P 的 no-op，且相当一部分破坏 P2P。因而只检查语法、diff 可应用或“改过文件”会严重高估代码智能体质量。

### 8.5 模型补丁倾向短而局部

Section 5 报告模型 patch 总修改长度通常不到 gold patch 的一半；正文示例以约 30.1 行对 74.5 行概括该差异。模型往往只改一个文件，虽可能得到更简洁解，也可能遗漏跨文件修复、测试更新和风格一致性。Figure 10 还展示了功能正确的模型 patch 可能采用与人工不同、复杂度更高的路径，说明 gold patch 相似度不应替代执行测试或代码质量评审。

## 9. 局限性

- 数据仅来自 12 个热门 Python 仓库，语言、仓库治理方式、测试文化和 issue 类型的代表性有限。
- 原始 baseline 是单轮检索—生成，不代表现代代码智能体的多轮浏览、运行测试、编辑和恢复能力。
- 每个任务只生成一次并使用 greedy decoding，没有重复运行、置信区间或稳定性分析。
- GPT-4 只跑 25% 随机子集，无法与其他模型做完全同样本的全量比较。
- Oracle retrieval/collapsed 依赖参考补丁位置，只能诊断，不是公平的端到端系统。
- F2P/P2P 来自现有 PR 和仓库测试，不能保证覆盖所有需求、隐藏边界条件、安全、效率、可读性与维护性；Section 7 明确承认仅靠执行式代码测试不足。
- 流行仓库和“PR 修改测试”筛选会偏向测试成熟、维护规范且可安装的任务，并排除没有新增测试但真实重要的问题。
- 连续更新和时间后移有助于降低记忆风险，但论文的时间分组没有发现稳定的训练日期前后差异，这不能证明不存在训练数据污染。
- 闭源模型端点和输出会随服务更新而漂移；v3 自身也显示模型和结果表在会议后继续变化。
- 完整仓库安装和测试成本很高；论文主要报告准确率，没有系统报告每任务美元成本、token、墙钟时间、环境失败率和碳成本。

## 10. 可复现性信息

- 论文 Section 9 声明提交时提供全部源代码、2,294 个任务及数据构建、评测、推理和训练目录；正式仓库现已公开。
- 数据实例保存 issue、base commit、参考 patch、测试 patch、F2P/P2P 列表和仓库版本，可重建执行环境。
- Appendix A.2/A.4 说明构建和评测逻辑，Appendix D 给出检索、单次 greedy 推理及提示模板。
- SWE-Llama 的训练数据、权重、LoRA 参数、硬件和训练时长有较详细记录。
- 代码仓库：https://github.com/SWE-bench/SWE-bench
- 数据/排行榜入口：https://www.swebench.com/
- 严格复现仍需固定 benchmark 数据版本、Docker/依赖镜像、仓库 commit、模型快照、提示模板和评测 harness commit；旧 Python 依赖、外部包源与操作系统变化可能使环境重建失败。
- 原实验没有多随机种子重复和统计区间；若用于智能体回归测试，应额外保存每次完整轨迹、模型参数、运行预算及环境日志。

## 11. 与“智能体测试”研究的关系

SWE-bench 把测试对象从静态文本答案扩展为“模型/智能体 + 仓库状态 + 补丁动作 + 可执行环境”，是代码智能体评测的基础范式：

- oracle 是环境中的测试结果，而非字符串匹配；
- F2P 检查任务完成，P2P 检查回归，体现功能正确性与副作用的双重要求；
- base commit 和依赖环境属于测试夹具，必须像数据集一样版本化；
- 可应用、部分修复、回归和完整解决需要分层诊断；
- 检索、定位、修改和验证是可分别评测的能力，而不能只看最终 resolved；
- 单次确定性补丁 baseline 无法回答真实 agent 的循环、恢复、成本、延迟和随机稳定性问题，后续测试框架需补齐这些维度。

## 12. 可借鉴的工程实现

1. 从 issue—PR—测试历史自动构建“修复前失败、修复后通过”的回归任务。
2. 每个任务保存不可变的仓库 commit、容器镜像、安装日志、测试选择和超时配置。
3. 将测试拆成 F2P 与 P2P，分别监测目标修复和既有行为回归。
4. 记录 patch apply、编译/导入、测试收集、F2P、P2P 和完整 resolved 的分阶段漏斗。
5. 对智能体轨迹增加定位 recall、首次正确文件时间、测试运行次数、无效编辑、回滚次数、token、费用和总延迟。
6. 设置 BM25、oracle-file 和 oracle-region 三档诊断，区分定位失败、上下文噪声与修复推理失败；oracle 档不得进入正式排行榜。
7. 保存 No-Op、Regression、Partial 和 Breaking 等失败类型，形成可复用的错误分类与回归集。
8. 使用时间后移、私有任务和定期新增实例降低显式记忆/污染，但同时审计测试充分性。
9. 对同一 agent 重复运行并报告均值、置信区间和预算约束，弥补原论文单次 greedy 评测的不足。
10. 在单元测试之外增加静态分析、安全扫描、性能、风格和人工抽检，避免“测试通过即高质量”的过度结论。

## 13. 证据等级和全文访问情况

- 证据等级：**已阅读全文**。
- 全文来源：本地 PDF `literature/papers/2024-Jimenez-SWE-bench.pdf`；因 arXiv Markdown 解析文件 `.codex-data/arxiv-papers/2310.06770.md` 内容损坏，本次使用 `pdftotext` 提取并逐节核对本地 PDF。
- 本地 PDF 身份：`arXiv:2310.06770v3`，标注已发表于 ICLR 2024；正式会议身份另由 ICLR Proceedings/OpenReview 核验。
- 阅读范围：正文 Sections 1-9，数据构建与测试执行 Appendix A，SWE-Llama 训练 Appendix B，oracle/失败分类/时间分析 Appendix C，推理设置与案例 Appendix D。
- 版本限制：Table 5 中 Claude 3 Opus/GPT-4-turbo 和 SWE-bench Lite 属于 v3 更新；本笔记对这些数字明确标注为会后 arXiv 修订内容。

## 14. 可以支持综述中的结论

- 代码智能体需要在真实仓库快照和可执行测试环境中评估，短函数基准不足以代表软件工程能力；
- 目标修复测试和回归测试必须同时通过，patch 可应用率不能替代任务成功率；
- 文件定位、上下文噪声和代码修复是可分离的失败来源；
- 增加上下文可能提高相关文件召回却降低端到端成功，应测试上下文选择质量而非只扩充窗口；
- Oracle 文件/位置实验适合能力诊断，但因使用答案信息不能作为部署性能；
- 自动测试是强 oracle，但不能覆盖效率、安全、可读性和可维护性；
- 环境、依赖、测试 harness 和仓库 commit 都是智能体测试可复现性的组成部分；
- 原 SWE-bench baseline 没有覆盖多轮 agent 的随机性、循环、恢复、成本和延迟，这些是后续代码智能体评测必须补充的维度。
