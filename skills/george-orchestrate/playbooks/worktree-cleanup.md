# 工作区与运行资源清理

此流程仅在用户要求清理对应资源时执行，普通任务收尾只处理自己创建的临时资源。

1. 用git worktree list实际清单、磁盘占用、分支和dirty状态做候选审计。查active/pinned任务、运行进程、未提交及未推送内容、PR/base与合并证据；最近聊天未知时继续查对应记录。
2. 分类建议不是删除授权。共享/主工作树、活跃任务、用户pin、未归档改动保留；未跟踪文件也可能有价值。不能仅凭名字、merge状态或scratch分类删除。
3. 优先使用宿主提供的可恢复archive工具。确需删除则列出精确对象、占用、使用和恢复状态；在已授权范围外先准备可审候选。
4. 清理前再次读取现场防止竞态，禁止对未知状态force-remove/reset。模拟器/应用数据/缓存另有对象和使用审计，不能随工作树顺手清。
5. 完成后复查实际列表、磁盘空间和保留的恢复证据，报告实际释放而不是预计值。

来源：pstack `skills/poteto-mode/playbooks/worktree-cleanup.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；适配 [George接入合同](../../george-mode/references/integration.md)。
