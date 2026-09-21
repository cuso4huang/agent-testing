# OSWorld：结构化阅读笔记

## 1. 基本信息

- **标题**：OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
- **作者**：Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao, Toh Jing Hua, Zhoujun Cheng, Dongchan Shin, Fangyu Lei, Yitao Liu, Yiheng Xu, Shuyan Zhou, Silvio Savarese, Caiming Xiong, Victor Zhong, Tao Yu
- **年份**：2024
- **会议或期刊**：Advances in Neural Information Processing Systems 37，Datasets and Benchmarks Track（NeurIPS 2024）
- **DOI**：10.52202/079017-1650
- **arXiv ID**：2404.07972
- **正式版本和预印本关系**：本地阅读的 arXiv v2 首页仍标注为 under review；其后形成 NeurIPS 2024 Datasets and Benchmarks 正式版本。引用应优先使用正式版本和已核验 DOI，arXiv 作为公开全文入口。
- **项目/代码**：<https://os-world.github.io/>；<https://github.com/xlang-ai/OSWorld>

## 2. 研究问题

OSWorld 研究如何在真实桌面操作系统和常用应用中，端到端测试多模态 agent 对开放式自然语言任务的理解、视觉/可访问性 grounding、跨应用规划和精确 GUI 操作。它试图克服网页或简化 GUI 基准动作空间狭窄、初始状态单一、不能跨应用，以及依赖参考轨迹而非最终业务状态的问题。

## 3. 被测试的智能体类型

- 视觉—语言桌面单智能体，可接收 screenshot、accessibility tree 或二者组合。
- 动作由 `pyautogui` 执行，包括鼠标、键盘和可执行的 Python 控制代码，另有 WAIT、FAIL、DONE 等控制动作。
- 覆盖浏览器、办公软件、邮件、媒体、图像编辑、代码编辑器和操作系统设置，并包含多应用工作流。
- 属于 GUI/具身于数字环境的 agent；不测试物理机器人或多智能体协作。

## 4. 测试或评估方法

第 2–3 节将环境建模为 POMDP `(S,O,A,T,R)`。每个任务配置包含：

- 初始化环境的 setup 动作、文件和系统设置；
- 自然语言 instruction；
- agent 的 screenshot/accessibility observation 与 `pyautogui` 动作；
- post-process/getter/evaluator，通过应用内部文件、配置、数据库、页面/可访问性树或实时爬取结果检查最终状态。

最终奖励通常为成功 1、失败 0，部分任务允许按满足的子条件给小数分；不可完成任务正确返回失败也可得分。主实验最多 15 步。VM 快照提供安全隔离、重置、无头运行和并行执行，因此评测的是实际动作造成的状态，而不是参考动作序列匹配。

## 5. 数据集、环境或基准

- 主 Ubuntu 集包含 **369 个任务**，另有 **43 个 Windows 任务**用于跨系统补充实验。
- 表 3：101 个多应用任务（27.4%）、268 个单应用任务（72.6%）；84 个任务整合自既有数据（22.8%）；30 个不可完成任务（8.1%）；302 种初始状态和 134 个独立 evaluator。
- 应用包括 Chrome、VLC、Thunderbird、VS Code、LibreOffice Calc/Writer/Impress、GIMP 及操作系统原生应用。
- 84 个整合任务来自 NL2Bash、Mind2Web、SheetCopilot、PPTC、GAIA 等；其余根据教程、论坛、视频、课程和博客构造。
- 九位计算机专业学生作者历时三个月、约 1,800 人时构造任务，后续四轮质量检查另投入 400 余小时。每个样本平均约需 1 小时配置、2 小时编写 evaluator。

## 6. 评价指标

- **Overall Success Rate**：最终 evaluator 得分的宏平均。
- **按领域成功率**：OS、Office、Daily、Professional、Workflow。
- **难度、可行性与单/多应用分层**：表 6。
- **观察/动作配置对比**：screenshot、accessibility tree、二者组合、Set-of-Marks（SoM）。
- **鲁棒性**：窗口位置、窗口大小和桌面 clutter 扰动后的成功率。
- **跨操作系统迁移**：同类任务在 Ubuntu/Windows 上的结果及相关性。
- **人类成功率与完成时间**：用于衡量任务可解性和差距。
- 不测安全副作用、过程效率、token/货币成本或延迟分位数。

## 7. 实验设计

- 主基线在 accessibility tree 上测试 Mixtral-8x7B、Llama-3-70B、GPT-3.5、GPT-4、Gemini、Qwen-Max 等；视觉设置包括 CogAgent、GPT-4V、Gemini Pro Vision/1.5、Claude 3 Opus、GPT-4o。
- 比较 screenshot、accessibility tree、screenshot+tree 和 SoM；原始屏幕为 1920×1080。
- 附录 C.1 给出模型/参数：如 `gpt-3.5-turbo-16k`、`gpt-4-0125-preview`、`gpt-4-vision-preview`、`gemini-pro`/`gemini-pro-vision`；temperature=1.0、top-p=0.9、最大生成 1,500 tokens、最多 15 步、单任务最多 30 分钟。
- 对话保留最近三次观察/动作，超长时从开头截断。论文另分析分辨率、文本/图像历史长度、窗口扰动和 Ubuntu→Windows 迁移。
- 人类基线由不熟悉具体任务的计算机专业学生完成每个样本。

## 8. 主要发现

1. **真实桌面任务远未解决。** 表 5 中最佳主表结果约为 GPT-4 accessibility tree 的 12.24%，而人类为 72.36%。GPT-4 的分领域结果为 OS 20.83、Office 3.58、Daily 25.64、Professional 26.53、Workflow 2.97，跨应用工作流尤其困难。
2. **纯截图基线明显受 grounding 限制。** GPT-4V screenshot 为 5.26%，Gemini-Pro-Vision 为 5.80%；GPT-4V 加 accessibility tree 提升到 12.17%，SoM 为 11.77%。可访问性结构能显著帮助，但质量并不稳定。
3. **复杂度造成明显下降。** 表 6 中 GPT-4V+SoM 在 easy/medium/hard 上为 16.78/13.12/4.59，单应用 13.74、多应用 6.57。不可完成任务 16.67 与可完成任务 13.34 的反常关系提示模型可能有“过早判失败”或 oracle/样本难度差异。
4. **微小界面扰动即可破坏性能。** 在 28 个任务子集上，原布局成功率 50.79；改变窗口位置后为 36.5，改变大小 15.04，加入 clutter 25.39（图 8）。这是 GUI agent 缺乏变形鲁棒性的直接证据。
5. **视觉分辨率与表示方式有交互。** 纯截图分辨率提高通常改善效果；SoM 在下采样比约 0.4（768×432）附近最好，继续增加标记密度/分辨率反而下降（图 5）。
6. **长上下文并非简单“越多越好”。** accessibility tree 的 90 分位长度达 6,343.6 tokens；增加文本历史有帮助，但加入更多图像历史未见同样收益（图 6–7）。
7. **失败主要集中在精确执行与状态感知。** 对 550 个失败案例，超过 75% 涉及鼠标点击不准确；还观察到重复点击、环境噪声、缺少领域知识、误解 instruction 和视觉遗漏。模型可能提出合理高层计划，却不能稳定落到 GUI 控件。
8. **跨系统迁移弱。** 表 7 的配对任务上 Ubuntu 4.88、Windows 2.55，相关系数约 0.7；相同语义任务仍受操作系统界面影响。

## 9. 局限性

论文第 7 节及实验讨论明确显示：

- 评测聚焦任务正确性，没有安全指标；未检查潜在副作用和与目标无关的破坏性操作。
- accessibility tree 在不同应用中可能缺失、冗余或噪声很大，既是现实问题也是不同模型观察不完全等价的混杂因素。
- 高标注成本限制应用覆盖；主平台为 Ubuntu，Windows 仅补充集，因许可原因未覆盖 macOS。
- 当前 agent 仍缺探索、记忆、反思和长图像上下文能力。

进一步的测试边界：

- 15 步上限和最近三轮历史会把控制器设置与模型能力共同计入得分。
- evaluator 通常验证最终工件；若任务规定必须使用某应用，agent 可能通过命令行或其他工具达成结果而绕过过程约束，除非 oracle 明确编码。
- 主结果以单点成功率为主，未提供多次随机运行置信区间、token/经济成本或完整延迟统计。
- 真实软件、闭源 API 和 VM 镜像会版本漂移；高保真同时增加依赖脆弱性。
- 未测试提示注入、恶意文档、权限越界或数据外传。

## 10. 可复现性信息

- **代码/数据**：GitHub 公开 benchmark、环境脚本、任务配置、evaluators 和 baseline agent。
- **虚拟机**：提供 Ubuntu/Windows 运行流程、快照重置、headless/并行基础设施；正文和附录说明屏幕尺寸与 VM 设置。
- **应用版本**：附录提供部分具体信息，例如 Ubuntu 22.04 和 LibreOffice 7.3.7.2；实际复现仍应锁定全部镜像摘要。
- **提示/模型**：附录给出模型名称、action prompt 和 observation 设置；闭源模型具体快照部分可核对。
- **参数**：temperature=1.0、top-p=0.9、max generation 1,500、15 steps、30 分钟超时、最近三轮历史。
- **oracle**：134 个 evaluator 及 setup/getter 配置可检查，任务经过两人交叉验证和多轮复核。
- **缺失项**：未系统报告种子、重复试验分布、每任务 token/费用及所有 API 响应；Windows 许可和闭源模型会限制完全重放。

## 11. 与“智能体测试”研究的关系

OSWorld 把 agent 测试扩展到操作系统级的真实 GUI 状态、跨应用工作流和像素/可访问性双重观察。它说明“规划正确”不等于“执行正确”：多数失败可发生在控件定位、窗口变化或状态更新。窗口位置、大小和 clutter 实验尤其接近软件测试中的变形测试，可直接用于评估环境扰动下的鲁棒性。

## 12. 可借鉴的工程实现

- 用 VM 快照为每个测试建立可复位初态，并限制网络、文件和账号权限。
- 任务配置分离 `setup`、`instruction`、`observation`、`action executor`、`getter` 与 `evaluator`。
- 最终工件用内部状态/API/文件解析验证；同时增加过程约束和禁止动作，避免“结果正确但越权”。
- 构建窗口平移、缩放、主题、分辨率、遮挡和桌面 clutter 的变形测试矩阵。
- 分开统计高层规划、元素 grounding、动作执行、反馈读取和恢复阶段的错误。
- 对重复点击、焦点丢失、无状态变化和危险快捷键设置运行时监视器。
- 保存 VM 镜像摘要、应用版本、屏幕配置、模型 ID 和完整 trajectory，保证回归结果可定位。

## 13. 证据等级和全文访问情况

- **证据等级：已阅读全文。**
- **全文来源**：本地解析文本 `/tmp/agent-review-text/2024-Xie-OSWorld.txt` 及本地 arXiv 2404.07972 全文。
- **阅读范围**：正文第 1–7 节、表 3、5–7、图 5–8，以及附录中的任务构造、环境配置、模型参数、提示、鲁棒性与失败案例。
- **访问限制**：论文全文可读；Windows 镜像许可、软件版本和闭源 API 服务状态仍可能阻碍逐位复现。

## 14. 可以支持综述中哪些结论

- 桌面 agent 的测试对象是模型、视觉/可访问性观察、控制器、操作系统和应用的联合系统。
- 最终态 evaluator、VM 快照与应用内部 getter 是真实 GUI 回归测试的核心设施。
- GUI grounding 和精确点击是当前主要瓶颈，高层计划能力不能替代低层执行可靠性。
- 窗口位置、大小与 clutter 可形成有效的变形测试，并揭示严重脆弱性。
- 多应用、长程和高难度任务产生显著性能下降。
- 现有 GUI 基准尚未充分覆盖安全副作用、权限、恶意内容、成本和重复运行稳定性。
