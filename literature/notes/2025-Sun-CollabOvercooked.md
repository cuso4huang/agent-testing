# Collab-Overcooked 阅读笔记

- 论文：*Collab-Overcooked: Benchmarking and Evaluating Large Language Models as Collaborative Agents*
- 年份/版本：EMNLP 2025；DOI `10.18653/v1/2025.emnlp-main.249`。
- 方法：在交互式 Overcooked 环境设置 30 个开放任务，以任务结果和过程指标测主动协作、分工、适应与沟通。
- 主要结论：理解目标不代表会持续协作；注意偏置、沟通与适应问题会随复杂度放大。
- 测试启示：多 agent 测试应同时保存个体轨迹、消息、共享状态和团队终态，并对 topology/agent 数做受控实验。
- 局限：虚拟厨房的协作模式不覆盖组织工作流；模型和提示更新会改变数值。
- 开源：https://github.com/YusaeMeow/Collab-Overcooked
- 证据：全文阅读，环境、指标、实验、因果分析与局限已检查。
