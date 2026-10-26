# 依赖变更堆栈

用于有前置依赖、用户要先审或保留合并权的队列。复用autopilot-full的实现和独立验证，替换拓扑及合并规则。

1. 按DAG排序；依赖项从父分支精确tip建立，不从trunk并行造不相干分支。owner只维护自己的slice，报告tip与父分支。
2. 根协调者独自rebase/retarget链；owner不得重排、合并、关闭PR或开auto-merge。每次根更新后owner先核对新base与写入租约。冲突由相应slice owner解决再统一整合。
3. 根PR指向trunk，孩子指向父分支；逐链检查trunk漂移与patch变化，变化即更新head证据。不要依赖Graphite或特定平台插件。
4. 交付线性、逐项有verdict的链，给root/tip链接及每层目的。用户授权开始落地后进入Shipping，停止其他写者；落地中的问题先停并重新协调，不能边合并边重写链。
产物：当前依赖图、唯一拓扑写者、每层版本/证据、可审堆栈。
来源：pstack `skills/poteto-mode/playbooks/autopilot-stack.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；适配 [George接入合同](../../george-mode/references/integration.md)。
