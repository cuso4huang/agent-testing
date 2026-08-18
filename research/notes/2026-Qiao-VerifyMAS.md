# VerifyMAS: Hypothesis Verification for Failure Attribution in LLM Multi-Agent Systems

## 1. 基本信息

- 作者：Hezhe Qiao; Hanghang Tong; Ee-Peng Lim; Bing Liu; Guansong Pang
- 年份/版本：2026，arXiv:2605.17467v1，预印本，无正式 DOI
- 身份核验：arXiv 与 OpenAlex 精确匹配；Crossref 返回他文，未采纳。

## 2. 研究问题

如何避免先逐个审查 Agent 所产生的局部行为偏差，并对跨 Agent、跨步骤才显现的 global/hybrid error 进行归因（§1、§3）。

## 3. 被测试的智能体类型

带完整交互日志和预定义错误 taxonomy 的 LLM 多智能体系统。

## 4. 测试或评估方法

VerifyMAS 采用 error-first 两阶段方法：先把每个错误类型写成自然语言 hypothesis，对完整轨迹判定 entail/neutral/contradict；仅对 entail 的错误继续定位责任 Agent。SFT 版本用正例、缺失错误和附近负样本构造 trajectory–hypothesis 训练对（§3、图2）。

## 5. 数据集、环境或基准

Aegis-Bench 和 Who&When；前者含 agent-error pair，后者提供 Agent 与步骤层标注（§4）。

## 6. 评价指标

Micro-F1 与 class-wise F1，分别考察 agent、error type 和 agent-error pair；论文特别分解 global、local、hybrid error（§4）。

## 7. 实验设计

同时评价 zero-shot 和 SFT；比较 direct prediction、agent-first CoT 与 VerifyMAS，并在多个开源/闭源模型及分布内、分布外轨迹上测试（§4）。

## 8. 主要发现

论文报告 error-first 验证对 global/hybrid error 的收益最明显，同时保持 local error 能力；SFT 提升分布内诊断并保持较好的分布外泛化（摘要、§4）。

## 9. 局限性

依赖预定义错误 taxonomy，无法直接覆盖未知类别；全轨迹长度、hypothesis 数量和模型上下文会带来成本。SFT 仍依赖人工 agent-error 标签，neutral 类也可能混合真正未知与证据不足（§3、结论中的 Limitation and Future Work）。

## 10. 可复现性信息

正文和附录给出 zero-shot/SFT 提示、负样本构造与训练设置；作者承诺发布数据，但正文未发现可访问代码仓库。

## 11. 与“智能体测试”研究的关系

提供一种 taxonomy 驱动的轨迹 oracle：先验证故障类型是否受全局轨迹支持，再把责任映射到 Agent，适用于协调错误测试。

## 12. 可借鉴的工程实现

三值 hypothesis oracle、global/local/hybrid 分层报告、空 Agent 标签处理、hard negative 和错误类型—责任组件二阶段诊断。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `research/papers/2026-Qiao-VerifyMAS.pdf`，22 页。

## 14. 可支持的综述结论

故障归因的顺序会影响 oracle：agent-first 方法容易被局部可见错误吸引，error-first 全轨迹验证更适合跨组件协调故障，但受 taxonomy 覆盖限制。
