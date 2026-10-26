# 运行现场取证

本任务交付诊断；未要求修复就不修改生产代码。
1. 捕获匹配现场的 CPU profile、heap snapshot、网络或渲染 trace，记录进程、版本、采样窗口和触发。
2. 用工具或只读代理缩减大型数据，保留热点调用树、泄漏对象到 GC root 的保留链、无输入仍执行的循环与计数。
3. 需要探针时先确认只读还是会改变运行状态。隔离环境中加入临时 instrumentation 或可恢复热补丁检验机制，记录它对系统的影响。生产只读任务不能把“取证”当作注入修改的授权。
4. 将信号映射到文件、符号、代码位置，并保留观察与推断的区别。未能干预验证的写最强支持假设。
5. 交付证据引用和诊断，只有原任务包含修复才续接 bug/perf 剧本；吞吐检查可记只读取证不适用。

来源：pstack `skills/poteto-mode/playbooks/runtime-forensics.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；改造依据见 [接入合同](../../george-mode/references/integration.md)。
