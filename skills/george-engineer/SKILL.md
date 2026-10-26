---
name: george-engineer
description: "George 的完整开发领域包，处理功能、故障、重构、性能、取证、视觉等价和工程交付。 / George's complete engineering domain pack: features, bugs, refactors, performance, forensics, visual parity and engineering delivery."
disable-model-invocation: true
---

> English: [SKILL.en.md](SKILL.en.md) · 中文正文见下方。

# 开发领域包

继承George目标、理论、证据与授权边界，先读 [接入合同](../george-mode/references/integration.md)。检查项目规则、当前修改、真实运行/测试入口。仅要求解释或计划时不自动实施。

| 任务 | 剧本 |
|---|---|
| 功能/接口 | [feature](playbooks/feature.md) |
| 故障修复 | [bug-fix](playbooks/bug-fix.md) |
| 行为保持重构 | [refactoring](playbooks/refactoring.md) |
| 一次性能问题 | [perf-issue](playbooks/perf-issue.md) |
| 迭代指标优化 | [hillclimb](playbooks/hillclimb.md) |
| 实时运行取证 | [runtime-forensics](playbooks/runtime-forensics.md) |
| 已有trace分析 | [trace-forensics](playbooks/trace-forensics.md) |
| 视觉等价迁移 | [visual-parity](playbooks/visual-parity.md) |
| 工程/PR交付 | [opening-a-pr](playbooks/opening-a-pr.md) |

[设计竞争与独立审查](../george-design/SKILL.md)、[多阶段编排](../george-orchestrate/SKILL.md)、[行为盲测](../george-evaluate/SKILL.md)作为完整配套，按风险与任务类型接入。

共同执行：数据形状先于逻辑；非平凡工作写阻塞/独立产物/共享状态/最小拆分四项；独立写区、一个owner；实现与高风险审查分离；每个单元结束验证；真实表面证据决定完成。

代码规则见 [行为测试与类型](workflows/code-quality.md)，文档/PR见 [技术写作](workflows/writing.md)。相关原则从 [索引](../george-mode/principles/INDEX.md) 读取完整叶子，避免只复述口号。项目没有Git也能完成本地成品，不强制开PR。
