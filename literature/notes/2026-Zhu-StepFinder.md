# StepFinder: A Temporal Semantic Framework for Failure Attribution in Multi-Agent Systems

## 1. 基本信息

- 作者：Taiyu Zhu; Yifan Wu; Weilin Jin; Ying Li; Gang Huang
- 年份/版本：KDD 2026；arXiv:2606.03467v1
- DOI：10.1145/3770855.3817991（Crossref/OpenAlex 一致核验）
- 代码：https://github.com/taiyu-zhu/StepFinder

## 2. 研究问题

怎样在长多智能体轨迹中以较低 token 和延迟定位根因步骤，避免 LLM 逐步生成式检查的高成本（§1）。

## 3. 被测试的智能体类型

具有不同角色和长交互序列的 LLM 多智能体系统，目标是 step-level failure attribution。

## 4. 测试或评估方法

先用 LLM 编码每一步文本，再由轻量时序模型结合双向时序特征、agent-aware step interaction、agent identity、多尺度差分、位置偏置和 temporal-consistency loss 输出每步异常分数；推理阶段不生成文本（§4）。

## 5. 数据集、环境或基准

Who&When 的 Algorithm-Generated 与 Hand-Crafted 两个子集（§5.1）。

## 6. 评价指标

Acc@1/2/3、MRR@3、带容差的步骤准确率、输入/输出 token 和每样本时间（§5.2、§7、附录 B）。

## 7. 实验设计

比较 all-at-once、step-by-step、binary search 等 LLM 方法与多种序列编码器；做组件消融、超参数敏感性和跨方法效率分析（§5–§7）。

## 8. 主要发现

- StepFinder 在复杂 Hand-Crafted 子集上表现更强；与并发方法比较时，在结构更短的 Algorithm-Generated 子集并非最佳（§5、附录 C）。
- 推理阶段零生成 token，每样本约 0.61 秒（Alg）和 3.56 秒（HC），明显快于 step-by-step（§7、表6）。
- 消融显示 temporal feature extraction 贡献最大，多尺度差分和位置偏置的效果随子集而变化（§6）。

## 9. 局限性

需要带根因步骤标签的训练数据，且仅在 Who&When 上验证；LLM embedding 和时序模型可能学习 benchmark 特定模式。正文也显示其在 Algorithm-Generated 子集不总优于 AgenTracer/CDC-MAS（附录 C）。

## 10. 可复现性信息

公开 GitHub 与 Zenodo artifact（10.5281/zenodo.20432323）；论文提供网络结构、损失、超参数、数据和效率协议（§4–§7）。

## 11. 与“智能体测试”研究的关系

展示生成式 Judge 之外的轨迹 oracle 路线：把定位视为时序异常排序，可降低在线诊断成本。

## 12. 可借鉴的工程实现

离线缓存 step embedding、top-k root-cause 候选、±δ 容差、agent-aware 时序特征和成本感知的轻量在线检测器。

## 13. 证据等级和全文访问情况

已阅读全文；本地 PDF `literature/papers/2026-Zhu-StepFinder.pdf`，12 页。

## 14. 可支持的综述结论

轨迹定位存在准确率—成本权衡；轻量时序模型适合规模化筛查，但跨 benchmark 泛化和标签成本仍需验证。
