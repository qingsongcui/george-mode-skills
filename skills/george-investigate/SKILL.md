---
name: george-investigate
description: "George mode 的只读调查模块。用于项目摸底、原始证据核查及经授权的 Agent 历史挖掘，产出覆盖范围、证据和未解问题。 / George mode's read-only investigation module. For project surveys, checking raw evidence and authorized mining of agent history; outputs coverage, evidence and open questions."
disable-model-invocation: true
---

> English: [SKILL.en.md](SKILL.en.md) · 中文正文见下方。

# 调查与建模

先列问题与证据对象，找到项目权威入口和原始来源，再提取结论。文件数量、聊天数量和工具成功返回都不是业务结果。

历史挖掘先列来源、时间窗口、会话数、可解析数、实际阅读数和遗漏原因。按宿主、项目、时间分层抽取真实用户发言，排除系统提示、AGENTS 注入、转发文本和子 Agent 提示；同一会话副本去重。保留原文件及行号或数据库键，只存必要短引文，过滤密钥及无关客户资料。

经验分为当前明确要求、重复观察支持的偏好、单次情境偏好和待验证假设。重复支持至少来自独立会话，并核对相反案例。不能因为两个 Agent 重述同一对话就升级置信度。

调查业务时先统一窗口、单位、对象和归因口径；写出机制链和至少一个竞争解释。证据不足时明确未知，不用形容词补足。只读任务交付证据答案，不自动进入开发或外部操作。

输出应能回答：读了什么、发现什么、没读到什么、哪条证据会推翻结论。需要决策时转 [george-decide](../george-decide/SKILL.md)。
