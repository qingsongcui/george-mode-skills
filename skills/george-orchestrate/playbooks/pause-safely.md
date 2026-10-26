# 安全暂停与检查点

明确“暂停/停下”才停止任务；上下文压缩先保存检查点然后继续，用户“继续”不能被当暂停。不要让暂停变成完成。

1. 停止新派工和新外部写入，将暂停传至所有owner与watcher，查实际终态而非只发通知。
2. 当前原子步骤可安全完成就完成到检查点，否则仅撤销本轮可分离改动；未知外部操作先对账。不得reset未知用户工作。
3. 保存未提交diff、分支/worktree、已验证版本、进程、产物、未决gate、原目标、全部用户修正及下一精确动作。遵守项目提交约束，不机械造wip提交或推送。
4. 确认不会有后台孤儿继续写入，证据清理后仍存在。记录恢复所需命令/环境而不记录秘密。
5. 明确报告暂停状态与未完成项。恢复走session-pickup。

来源：pstack `skills/poteto-mode/playbooks/pause-safely.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；适配 [George接入合同](../../george-mode/references/integration.md)。
