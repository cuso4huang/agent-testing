# MobileSafetyBench：真实交互环境中的安全预言机

**论文**：Juyong Lee, Dongyoon Hahm, June Suk Choi, W. Bradley Knox, Kimin Lee. *MobileSafetyBench: Evaluating Safety of Autonomous Agents in Mobile Device Control*. arXiv:2410.17520（扩展版）。

**核心价值**：安全不是让模型回答“这件事危险吗”，而是把 Agent 放进 Android 模拟器，让它真的观察 UI、调用动作、改变消息/文件/账户/设置，再依据环境最终状态和完整动作历史判断是否造成危害。

## 环境与任务

- 共 250 个任务，覆盖消息、浏览、社交、日历、金融交易等应用。
- 200 个日常场景：100 个低风险、100 个高风险。
- 50 个间接 prompt injection 高风险场景，恶意指令嵌入短信、社交内容或其他 UI 观察中。
- 每一步 Agent 观察屏幕并选择动作；episode 有最大步数。
- 环境评分器同时读取最终状态 `s_T` 和动作历史 `a_1:T`。

## 为什么预言机必须是状态 + 轨迹

只看最终文本会漏掉：

- Agent 已经点了发送/转账，只是在回复里声称谨慎。
- Agent 拒绝高风险任务但之前已泄露或改变状态。
- Agent 完成低风险任务的同时产生负面副作用。
- 同一个最终 UI 状态可能由安全路径或危险路径到达。

因此“真实交互安全预言机”至少需要：

- **Goal achievement**：低风险任务是否成功完成（helpfulness）。
- **Refusal / harm prevention**：高风险任务是否避免危险动作（safety）。
- **环境断言**：敏感文件、账户余额、消息收件人、设置等是否发生不允许的变化。
- **动作序列断言**：是否查看、复制、上传、确认或执行了禁止步骤。

## 主要发现

- 各模型存在明显 safety–helpfulness trade-off：有的积极完成任务但高风险拒绝率低，有的拒绝较多但低风险任务也几乎做不成。
- 某些 workflow Agent 在高、低风险任务上都接近 80% goal achievement，说明“能力强”可能同时放大危害。
- 间接 prompt injection 场景中，Agent 常把 UI 内文本误当成新指令并执行金融等无关动作。
- 模型在静态 QA 中往往能识别风险，但进入 agentic setting 后仍会做出危险动作，说明安全认知不等于执行安全。
- Safety Chain-of-Thought（SCoT）先要求列安全考虑再规划动作，可提升 GPT-4o 的高风险拒绝率，同时维持较高低风险完成率，但仍不充分。

## 测试框架应怎样借鉴

- 每个 task 必须有可执行的环境 setup、成功断言、危害断言和清理脚本。
- 分开报告 helpfulness 与 safety，不要合成一个会掩盖 trade-off 的分数。
- 给危害分级；高风险动作可要求人工确认或硬策略阻断。
- prompt injection 测试要将载荷放进 Agent 会自然读取的环境数据，而非只放在用户输入。
- 每次运行保存屏幕、动作、工具参数、环境 diff 和终止原因，确保可重放。

## 局限

- Android 模拟器和有限应用仍是受控世界，不能覆盖真实设备全部权限、网络和用户行为。
- “拒绝”并不总是最佳安全行为；更成熟的 Agent 应澄清、降权执行或请求确认。
- 环境断言需要大量人工任务工程，且应用/UI 更新会造成 benchmark 漂移。

