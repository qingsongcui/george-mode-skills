---
name: george-evaluate
description: "George 的盲测、性能数字审计和技能更新验收。由总入口或用户明确调用。 / George's blind tests, performance-number audits and acceptance of skill updates. Invoked by the main entry or explicitly by the user."
disable-model-invocation: true
---

> English: [SKILL.en.md](SKILL.en.md) · 中文正文见下方。

# 评价方法与技能改进

先确定要验证的是哪个具体主张：

- 模式/提示/模型/结构是否改变行为：[盲测](playbooks/eval.md)。
- 一个性能或效率数字是否可信：[测量审计](workflows/benchmark.md)。
- 创建或改造技能：[技能编写](playbooks/authoring-a-skill.md)。
- 从个人习惯和失败持续改进：[模式改进](../george-reflect/workflows/improve-mode.md)。

评价必须保存失败、重复和局限。静态结构检查、真实场景检查、跨宿主任务表现、相对Poteto提升是不同主张，需要各自证据；不能从一个推出其他。使用 [工程原则](../george-mode/principles/INDEX.md) 中解释数字、行为测试和真实验证叶子。
