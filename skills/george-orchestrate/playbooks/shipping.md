# 授权交付与实际落地

进入条件：实现可审、任务要求发布/合并；完成本地准备和可审证据后，再处理任何缺失授权。已有授权不重复请求。

1. 对每个PR核对非作者独立verdict、精确head、真实产物证据、当前CI、未决评论、目标base、forge可合并条件。green/READY/退出0均不单独通过。
2. 只允许从根开始连续通过的一段交付；下层未通过，上层即使已绿也不能跳过。记录队列和当前授权。
3. 版本变化默认使旧verdict失效。patch-id相同只支持“补丁内容相同”，还要核对base、依赖、环境和运行契约；不确定时补验并对新head记录，不能抄旧SHA记录。
4. 每次只落地最低一项。合并命令成功、排队成功均不是完成，重新读取MERGED和目标提交。父层合并后由唯一拓扑owner检查孩子的新base/差异、必要时retarget/rebase并重验。
5. 落地期间其他owner不得写链。异常先停该项、保存可恢复状态并核对是否已发生外部写入；不盲目重试。
6. 完成后按真实入口验交付产物并保留证据。停止只属于本任务的watcher；不能把合并当业务采用或收入效果。
产物：实际落地记录、逐项证据、未落地原因及恢复点。
来源：pstack `skills/poteto-mode/playbooks/shipping.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；适配 [George接入合同](../../george-mode/references/integration.md)。
