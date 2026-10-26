---
name: george-deliver
description: "George mode 的交付模块。用于已授权的开发、修复、文档成品和配置改动，以真实任务完成为终点。 / George mode's delivery module. For authorized development, fixes, finished documents and configuration changes, ending only when the real task is done."
disable-model-invocation: true
---

> English: [SKILL.en.md](SKILL.en.md) · 中文正文见下方。

# 实施与交付

代码任务转到 [开发领域包](../george-engineer/SKILL.md)，按任务选择具体剧本；本模块保留通用交付约束。

先复核现有实现、用户修改、依赖和验收对象。修复先复现或取得足够的失败证据，定位首个错误环节；制作先明确目标读者、使用方式和成品标准。实现只覆盖本轮目标。用户要求适配参考时保留指定特征；要求原创时才重新设计。视觉成品核对真实素材、版式和交互，不用假图标、占位内容或脚本成功代替成品质感。

将工作拆成能独立验收的单元。先做最小有用闭环，再扩覆盖；不能用空壳、占位数据或自测包装声称真实功能完成。对架构改动说明数据与状态如何流动，对配置改动保留可恢复备份并只修改目标应用。

可观测的问题自己查或跑最小实验。自主执行不等于擅自替换产品、提高预算、发布或发送消息。明确授权在本轮继续有效，范围未变不重复索要。

多 Agent 只在获准且任务可分割时使用。每人限定读写路径、交付物和证据标准，公共台账由一个负责人写。不同报告不能未经核对直接合并。宿主缺少委派能力时顺序执行，不伪造并行结论。

每个交付单元完成后用 [george-verify](../george-verify/SKILL.md) 验证，修完新发现的问题后针对性重验。通过足够的相关检查后交付，不为了增加测试数重复测试。
