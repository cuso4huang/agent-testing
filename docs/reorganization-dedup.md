# 整理中的重复文件记录

本记录只登记已用 SHA-256 确认的逐字节重复，不把题名相似或版本不同的论文判为重复。

## 已处理

下列 4 个 `自己找的论文/` 文件与精选阅读包中的 PDF 完全相同，已保留阅读包对应文件并移除来源副本：

| 原来源副本 | 保留材料 |
| --- | --- |
| `2026.eacl-long.339.pdf` | `literature/papers/2026-Komoravolu-ATA.pdf` |
| `2026.findings-eacl.171.pdf` | `literature/papers/2026-Zhou-SIRAJ.pdf` |
| `sec26_prepub_luo.pdf` | `literature/papers/2026-Luo-AgentDoS.pdf` |
| `2026-f577-paper.pdf` | `literature/papers/2026-Li-LesDissonances.pdf` |

另有一篇不重复的安全综述已规范命名为 `literature/papers/2026-Kim-SecureAgentSoK.pdf`。

阅读包中的 MemoryAgentBench 和 Process Evaluation PDF 与规范论文库中的文件一致，已删除阅读包内副本；阅读包 README 和校验和文件改为链接到 `literature/papers/`。

## 后续复核

- 正式发表版、预印本和带批注版本即使标题相同，也要先确认版本语义后再处理；
- 若阅读包需要离线独立分发，可重新生成副本，但必须在本记录中注明用途；
- 新增 PDF 先运行哈希检查，再决定是否进入规范论文库。
