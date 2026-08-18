# REFLECT: Intervention-Supported Error Attribution for Silent Failures in LLM Agent Traces

## 1. 基本信息

- 作者：Xiaofeng Lin; Yingxu Wang; Tung Sum Thomas Kwok; Daniel Guo; Sahil Arun Nale; Charles Fleming; Guang Cheng
- 年份/版本：2026，arXiv:2606.09071v1；ICML 2026 FAGEN workshop 接收稿
- 身份核验：arXiv 与 OpenAlex 精确匹配；无正式 DOI，Crossref 模糊结果未采纳。

## 2. 研究问题

在没有异常、格式错误或工具崩溃的 silent failure 中，怎样通过实际干预验证“某一步导致最终错误”的假设，而不是只让 Judge 给出看似合理的解释（摘要、§1）。

## 3. 被测试的智能体类型

长程推理和工具使用 Agent，覆盖表格问答、多跳推理、chain-of-thought 检查和软件工程轨迹（§4）。

## 4. 测试或评估方法

REFLECT 分三阶段：定位候选最早决定性步骤并生成 repair plan；保持原始前缀，在该步骤注入定向修复并重放；依据 outcome flip 的对比证据重新定位。最终 attribution record 包含步骤、干预和已验证结果变化（§3.1–§3.4）。

## 5. 数据集、环境或基准

WTQ、GAIA、SWE 相关轨迹与 BBM/推理轨迹，共四类 benchmark；包含有 ground truth 的开发期 oracle 模式和无答案 proxy 模式（§4.1、附录）。

## 6. 评价指标

Exact Match、Off-by-1 step、覆盖率、verified/fallback 比例，以及 outcome verification 的 AUROC、Best-F1、error precision 等（§4.2）。

## 7. 实验设计

在相同 auditor 模型下比较 LLM judge、classifier/trajectory 方法、retry/correction 方法与 REFLECT；分析修复成功、无 ground truth 和多轮 replay 的效果，并检查补丁是否造成新路径偏离（§4、附录）。

## 8. 主要发现

论文报告 REFLECT 在四个 benchmark 的 same-auditor 比较中均获得最高定位准确率，结构化工具轨迹收益最大；修复成功时，intervention evidence 显著提高最终归因质量（摘要、§4）。无 ground truth 时仍能返回可操作定位，但证据更弱。

## 9. 局限性

一次成功干预只证明该修复足以改变结果，不证明因果最小性或唯一性（§3.1）。方法需要可重放环境，且 replay 会受到 Agent 随机性、工具变化和补丁质量影响；无 ground truth 时 outcome oracle 只能依赖代理信号（§5、附录 Limitations）。

## 10. 可复现性信息

论文称 `err-loc`、基线、指标和 WTQ 人工标注轨迹随 supplementary material 提供；正文未给出稳定 GitHub URL。实验环境、prompt 和 benchmark 适配细节在附录给出。

## 11. 与“智能体测试”研究的关系

把失败归因转化为可执行的 counterfactual test，明确区分“纠正成功”和“已定位原始根因”。

## 12. 可借鉴的工程实现

前缀保持 replay、诊断特定 patch、outcome flip oracle、verified/fallback 双层标签和无 ground truth 的降级路径。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `research/papers/2026-Lin-REFLECT.pdf`，21 页。

## 14. 可支持的综述结论

高可信轨迹归因应尽可能测试假设；仅靠 narrative Judge 无法确认决定步骤，而独立 retry 成功也不能定位原轨迹错误。
