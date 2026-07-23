# AI 智能体测试与质量保障：检索日志

## 研究范围

- 研究问题：如何系统测试与保障基于大语言模型的自主智能体质量，覆盖单/多智能体、工具调用、Web/浏览器、编程和具身智能体。
- 时间范围：2020-01-01 至 2026-07-23；重点关注 2023 年以后。
- 语言：英文为主，必要时补充可核验的高质量中文研究。
- 文献类型：优先同行评审会议/期刊；保留有明确技术贡献的重要 arXiv 预印本、基准和工程研究。
- 数据源：Semantic Scholar、arXiv；Crossref 与 OpenAlex 用于元数据交叉核验。
- 检索日期：2026-07-23（Asia/Shanghai）。

## 概念边界

本调研把“智能体测试”定义为：对具有目标驱动、多步决策、环境交互、工具调用、状态/记忆维护或多主体协作能力的 AI 系统，实施离线评测、场景/轨迹测试、对抗与安全测试、故障注入、回归测试及线上监控，以评估其功能正确性和可靠性、安全性、稳定性、可复现性、成本与延迟等非功能质量。仅测试无环境行动闭环的普通聊天模型，不属于核心范围；但 LLM-as-a-Judge、提示注入与生成质量研究在直接支撑智能体测试方法时可作为方法学文献纳入。

## 纳入与排除标准

### 纳入

1. 直接研究 LLM/AI agent 或 agentic system 的测试、评估、基准、可靠性或安全性；
2. 针对规划、推理、记忆、工具使用、轨迹、错误恢复、多智能体协作等智能体能力提供可复现实验；
3. 提供 Web、编程、具身、工具调用或企业工作流智能体的环境、数据集、指标或测试框架；
4. 基本元数据可由论文原文、arXiv、Crossref、OpenAlex 或出版方核验。

### 排除或降级

1. 仅评测普通对话/问答模型，和自主行动闭环无直接关系；
2. 无技术方法或实验的产品宣传、博客或观点文章；
3. 基本身份无法核验；
4. 与已纳入正式版本内容重复的旧预印本（保留版本关系但不重复计数）；
5. 仅作宽泛综述且不能为本研究问题提供独立实证证据。

## 初始检索式

以下检索式按数据库语法作必要调整，不声称各数据库支持相同布尔语法。

### 英文核心检索式

1. `"LLM agent" AND (evaluation OR testing OR benchmark)`
2. `("AI agent" OR "agentic system") AND ("software testing" OR reliability OR robustness)`
3. `("tool use" OR "tool-using agent" OR "function calling") AND (evaluation OR benchmark OR testing)`
4. `("web agent" OR "browser agent") AND (benchmark OR evaluation OR safety)`
5. `("coding agent" OR "software engineering agent") AND (benchmark OR evaluation OR testing)`
6. `("multi-agent" OR "multiagent") AND ("LLM" OR "language model") AND (evaluation OR benchmark OR failure)`
7. `("embodied agent" OR "language agent") AND (evaluation OR benchmark) AND LLM`
8. `("agent safety" OR "agent security") AND (benchmark OR evaluation OR testing)`
9. `("prompt injection" OR "indirect prompt injection") AND (agent OR tool)`
10. `("agent trajectory" OR "trajectory evaluation") AND (LLM OR agent)`
11. `("runtime monitoring" OR observability) AND ("LLM agent" OR "agentic system")`
12. `("fault injection" OR fuzzing OR "metamorphic testing" OR "property-based testing") AND ("LLM agent" OR "AI agent")`
13. `("LLM-as-a-judge" OR "language model as a judge") AND (agent OR trajectory OR evaluation)`
14. `("agent benchmark" OR "agent evaluation") AND (cost OR latency OR reproducibility OR stability)`
15. `(loop OR "state drift" OR cascading OR recovery) AND ("LLM agent" OR "agentic workflow") AND evaluation`

### 中文补充检索式

1. `大语言模型 智能体 测试 评测 基准`
2. `AI 智能体 可靠性 鲁棒性 安全测试`
3. `工具调用 智能体 评测`
4. `多智能体 协作 评测 故障`
5. `浏览器智能体 基准 提示注入`
6. `智能体 轨迹评估 故障注入 变形测试`

## 检索与筛选流程

1. 用 Semantic Scholar 宽搜并以高相关种子论文扩展引用、参考文献与相似论文；
2. 用 arXiv 补充近期预印本和可访问全文；
3. 按规范化 DOI、arXiv ID、规范化标题+年份、模糊标题+重叠作者依次去重；
4. 记录预印本、会议、期刊扩展及修订版本关系，引用优先采用正式版本；
5. 使用 Crossref 与 OpenAlex 核验 DOI、作者、年份、venue 和文献类型；
6. 先以题名/摘要筛选，再对高相关文献全文筛选与结构化精读；
7. 所有纳入/排除决定写入 `evidence/screening-log.csv`，所有证据等级写入证据表。

## 执行记录

- 2026-07-23：初始化研究目录、范围、检索式、纳排标准及证据字段。

