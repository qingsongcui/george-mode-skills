---
name: george-decide
description: "George mode 的理论决策模块。用于重要业务与架构选择，按反身实践闭环登记目标、假设、反证、预测和停止条件。 / George mode's theory-driven decision module. For important business and architecture choices; registers goals, hypotheses, counter-evidence, predictions and stop conditions per the reflexive-practice loop."
disable-model-invocation: true
---

> English: [SKILL.en.md](SKILL.en.md) · 中文正文见下方。

# 决策与事前承诺

先读 [决策闭环](../george-mode/references/decision-loop.md)。重要新问题按其中 11 个分析模块执行，不能只填表代替分析。项目要求全量覆盖时，逐模块说明适用性、未知和理由，不用打勾代替分析。

把价值、目标、治理边界、世界模型和行动方案分开。明确谁决定、争取什么结果、可用时间/现金、不能承担的后果，以及哪些已由用户决定。比较可行路线及维持现状，不把 AI 偏好的路线冒充用户选择。

将机制假设写成能被观察推翻的陈述。登记指标、数据窗口、基线、主概率 p 与基准 p0、到期时间、停止规则、复盘节点。未获用户采纳的方案标为建议。对已定策略的日常子动作引用原登记，只登记真实增量。

在要求事前冻结的项目中先冻结再执行；若已发生，只能记为事后记录，不能伪造事前预测。冻结失败则先解决归档问题，不执行依赖该承诺的动作。

执行转 [george-deliver](../george-deliver/SKILL.md)，到期或触发停止条件转 [george-reflect](../george-reflect/SKILL.md)。
