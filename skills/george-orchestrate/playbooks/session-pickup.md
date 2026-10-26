# 从正确节点恢复

1. 定位本任务已有检查点/会话/分支，先读元信息、最近消息与关键决定；原目标和后续修正全部保留。默认只查当前任务范围。
2. 核对现场工作区、head/base、diff、已落地内容、未提交修改、进程、平台状态及活跃owner。历史报告是线索，真实证据决定是否已完成。
3. 比较done与pending，复用仍有效的证据；只对漂移、失败或缺失补验，不从头重做，更不重复未知外部操作。
4. 恢复inbox未ack消息、gate、frontier和当前verdict；进程终止不等于产物不存在，先找产物再决定是否重派。
5. 明确续接点并进入对应剧本；恢复不是独立的无限审计。收尾说继承了什么、补验了什么、完成了什么。

来源：pstack `skills/poteto-mode/playbooks/session-pickup.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；适配 [George接入合同](../../george-mode/references/integration.md)。
