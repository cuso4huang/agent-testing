# 2026 Python Agent / 后端实习作品集：技术选型与能力信号

> 核验日期：2026-08-10（Asia/Shanghai）  
> 范围：只使用项目官方文档或规范核验技术事实；“作品集建议”是基于这些事实的工程判断，不代表招聘市场统计。

## 结论先行

Python 是合适的主语言。建议做一个**可评测、可追踪、可恢复的 Agent 后端服务**，而不是只做聊天页面或串联框架 Demo。最有说服力的主栈是：

- FastAPI + Pydantic：HTTP/SSE API、类型边界、结构化工具输入输出；
- PostgreSQL：用户、会话、任务、工具调用、评测结果等事实数据；
- Redis + Celery（或先用 Celery/Redis 做唯一队列方案）：缓存、限流、耗时任务与重试；
- OpenTelemetry：贯穿 HTTP 请求、模型调用、工具调用、队列任务的 trace，并补充延迟、错误率、token/成本等指标；
- Docker Compose：一条命令启动 API、worker、PostgreSQL、Redis 与观测组件；
- pytest + 一套可复现 eval 数据集：用结果证明正确性、可靠性和迭代能力。

技术名本身不是亮点。真正的简历信号是：边界清楚、失败可恢复、行为可测量、风险有约束、别人能复现。

## 技术逐项核验与作品集用法

### 1. FastAPI：作为服务边界，而不是作品主体

官方文档说明 FastAPI 基于 OpenAPI/JSON Schema，可自动生成交互式 API 文档，并基于 Python 类型声明完成参数处理；对会等待网络或数据库 I/O 的代码，可以使用 `async def`。[FastAPI Features](https://fastapi.tiangolo.com/features/)；[Concurrency and async/await](https://fastapi.tiangolo.com/async/)

作品集应展示：

- REST API 加 SSE 流式事件（Agent 状态、工具调用和最终答案）；
- 鉴权、统一错误模型、request ID、分页、超时与取消；
- 清楚区分异步 I/O 与 CPU/长任务，后者交给 worker，不在请求进程里硬跑。

**能力信号：**会设计生产型 API，而不只是会写路由。

### 2. Pydantic：把不可信输入锁在类型边界

Pydantic 官方文档说明其 schema 通常由 Python type hints 定义，可做验证和序列化、生成 JSON Schema，并提供 strict mode；JSON Schema 与 OpenAPI 3.1 兼容。[Why use Pydantic](https://pydantic.dev/docs/validation/latest/get-started/why/)

作品集应把以下内容建模为 Pydantic 类型：API 请求/响应、工具参数/结果、Agent 事件、队列消息和配置。对工具参数与高风险字段启用严格约束，不要在核心流程传递任意 `dict`。

**能力信号：**理解 LLM 输出和外部输入都不可信，能用 schema 建立契约。

### 3. PostgreSQL：保存“事实”，不要把所有状态塞进向量库

PostgreSQL 官方文档确认其原生支持 SQL/JSON 与事务；`jsonb` 适合存灵活 JSON 数据，同时可用常规关系模型保持约束。PostgreSQL 也内建 `tsvector`/`tsquery` 全文检索类型。[JSON Functions and Operators](https://www.postgresql.org/docs/current/functions-json.html)；[Text Search Types](https://www.postgresql.org/docs/current/datatype-textsearch.html)

作品集应展示：

- 关系表保存用户、会话、任务、运行、评测与权限；`jsonb` 保存模型/工具的可变元数据；
- migration、索引、事务、唯一约束与幂等键；
- 若需要 RAG，可以增加 pgvector，但不要让向量检索取代正常的数据建模。

**能力信号：**具备后端数据建模和一致性意识，而非只会调用模型 API。

### 4. Redis 与任务队列：明确语义，展示失败恢复

Redis 官方文档明确区分 Pub/Sub 与 Streams：Pub/Sub 是 fire-and-forget；Streams 保存历史，consumer group 支持显式确认、pending 记录与接管未处理消息。官方也提示 Streams 默认异步复制，在故障切换时仍可能丢失部分数据，必须按需求评估持久化和语义。[Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)；[Redis Pub/Sub](https://redis.io/docs/latest/develop/pubsub/)

Celery 官方任务文档强调任务最好是幂等的；重试、确认时机、超时等需要显式配置，worker 异常退出时的重投也有具体语义。[Celery Tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)

建议作品集先选 **Celery + Redis broker**，不要同时堆多个队列框架。至少实现：

- 任务状态、超时、指数退避重试、最大重试次数；
- 幂等键、防重复副作用、失败任务记录（或 DLQ）；
- worker 被杀死后的恢复演示；
- 明确声明交付语义：通常按“至少一次”设计业务幂等，而不是声称 exactly-once。

**能力信号：**能讨论并验证故障语义，而不是只会“异步执行”。

### 5. OpenTelemetry：让 Agent 的每一步可解释、可定位

OpenTelemetry 是厂商中立的 traces、metrics、logs 生成/采集/导出框架；Python 当前 traces 和 metrics 为 Stable，logs 仍是 Development。官方提供 Python 自动插桩及 OTLP exporter。[OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)；[Python zero-code instrumentation](https://opentelemetry.io/docs/zero-code/python/)；[OpenTelemetry components](https://opentelemetry.io/docs/concepts/components/)

建议以 trace 为主：一个用户请求为根 span，下挂 Agent run、模型调用、检索、每次工具调用和队列任务；记录模型名、延迟、token、重试次数、错误类别，但不要记录 secret 或完整敏感 prompt。指标至少包括成功率、p50/p95 延迟、工具错误率、token/成本和队列积压。官方也提醒高基数 metric 属性会推高内存成本，因此不要把 user ID、原始 URL 等直接作为指标标签。[OpenTelemetry Metrics](https://opentelemetry.io/docs/concepts/signals/metrics/)

**能力信号：**可以用一次 trace 解释“慢在哪里、错在哪里、花费在哪里”。

### 6. Docker：证明可复现交付

Docker 官方建议使用多阶段构建、可信且较小的基础镜像、`.dockerignore`、不安装无关包、解耦容器，并在服务无需特权时用非 root `USER`；还建议在 CI 中构建并测试镜像。[Docker build best practices](https://docs.docker.com/build/building/best-practices/)；[Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

作品集应有：多阶段 Dockerfile、非 root 用户、healthcheck、环境变量示例、Compose 一键启动、数据库 migration 和 README 演示命令。API、worker、数据库和 Redis 分容器。

**能力信号：**面试官能够在新机器上复现，而不是只能看截图。

## Agent 特有的三个必修主题

### 1. Evals：先定义“好”，再改 prompt

OpenAI 官方 eval 指南把可靠开发描述为：定义任务、用测试输入运行、用 grader 分析结果，并持续扩充数据集；支持字符串检查、文本相似度、模型评分和自定义 Python grader。[Working with evals](https://developers.openai.com/api/docs/guides/evals)

项目至少准备 30–100 条版本化样例，覆盖正常、边界、工具失败、检索无结果和对抗输入。报告任务成功率、工具选择正确率、引用/事实正确性、延迟与成本；CI 可跑小型回归集，完整集按需运行。评测集、grader 规则和失败案例应进仓库。

### 2. 安全：重点是 prompt injection 与工具权限

OpenAI 官方 Agent 安全指南指出 prompt injection 是常见且危险的攻击；建议不要把不可信数据拼进 developer message，使用结构化输出限制数据流，对工具调用保留审批，并用 guardrails 与 evals 覆盖风险。[Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety)

项目应展示：工具 allowlist、参数 schema、最小权限、URL/文件路径校验、敏感操作确认、secret 隔离、输出净化、审计记录，以及至少一组 injection 攻防测试。不要声称“完全防住”；应陈述威胁模型、剩余风险与缓解措施。

### 3. 可靠性：Agent 是分布式工作流，不只是一次 completion

需要显式处理模型超时、限流、工具异常、部分成功、重复投递、用户取消和预算耗尽。为每次 run 保存状态机/事件，设置整体 deadline、单步 timeout、重试条件与最大步数；对有副作用的工具使用幂等键。用故障注入测试证明恢复路径。

**能力信号：**README 中有一张失败路径图和一次可重复的故障演示，比“用了某某 Agent 框架”更有价值。

## 推荐的项目完成度顺序

1. **MVP：**单 Agent、2–3 个真实工具、FastAPI/Pydantic、PostgreSQL、可运行测试。
2. **工程化：**Celery/Redis、幂等/重试/取消、Docker Compose、CI。
3. **可信性：**eval 数据集与报告、prompt injection 测试、工具权限与审计。
4. **可观测：**端到端 trace、核心指标、一次故障定位案例。
5. **展示：**架构图、3 分钟演示、清楚的 trade-off 和未来工作。

不要一开始做多 Agent、Kubernetes、复杂微服务或同时接入多个框架。对实习作品集而言，一个边界清楚、测试扎实、故障可演示的“深项目”，通常比功能很多但不可验证的项目更强。

## 简历上可量化的表述模板

以下数字必须来自自己的 eval/压测，不要预填：

- “构建 Python Agent 服务（FastAPI、PostgreSQL、Celery/Redis），通过幂等键与退避重试将故障注入场景的任务最终成功率从 X% 提升到 Y%。”
- “设计 N 条版本化 Agent eval 集，覆盖工具选择、检索失败与 prompt injection；CI 回归使核心任务通过率保持在 Y%。”
- “接入 OpenTelemetry 端到端 tracing，覆盖 API—模型—工具—worker 链路，将 p95 故障定位时间从 X 降至 Y。”
- “使用多阶段、非 root Docker 镜像与 Compose，实现一条命令复现完整服务；CI 自动执行测试和镜像构建。”

这些表述共同证明四类能力：Python 后端基础、Agent 行为评测、安全边界、生产可靠性。
