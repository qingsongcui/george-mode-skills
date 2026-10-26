# 角色与预算配置

Codex、Cursor、OMP、Grok CLI 与 Antigravity 在用户启用 George 后按每个任务自主调度：Codex优先 [Codex适配器](../adapters/codex.md)，Cursor优先 [Cursor适配器](../adapters/cursor.md)；本机 oh-my-pi（`omp`）优先 [OMP适配器](../adapters/omp.md)；Grok Build / `grok` CLI 优先 [Grok适配器](../adapters/grok.md)；Google Antigravity 优先 [Antigravity适配器](../adapters/antigravity.md)。各宿主的会话级模型与推理强度选择取代下文默认继承规则，不互相套用参数。下文继续适用于尚未适配的其他宿主及持久配置变更。

仅在用户要求调整角色模型或预算时执行。平常沿用当前宿主设置，默认inherit-parent；本技能不读取Poteto模型文件作为George授权。

1. 从当前宿主实际工具枚举可调用模型、角色、推理强度、并发数与费用限制；OMP指 oh-my-pi 的 omp 命令，不混同OpenCode或oh-my-opencode。模型列表存在不等于一次请求成功。
2. 读取用户指定的现行配置；区分调研、设计候选、实现、审查、独立验证、综合、长任务协调角色。用相同简报做候选、不同视角做审查，模型品牌不是角色职责。
3. 按本轮预算和风险给具体角色表；panel列表长度决定代理数。用户未要求改模型就继承，不擅自用固定“最强”或付费品牌。受宿主角色锁定的不能偷偷覆盖。
4. 用户已明确授权配置改动时备份对应文件，验证真实slug/字段，最小修改；不要覆盖其他应用配置或总规则。缺目标偏好时先给可审表，缺失授权不靠默认补。
5. 配置解析后运行获准的真实最小请求，分别验证发现、服务返回和任务能力；失败保留准确错误与恢复路径。只通过help/列表不能声称可用。
6. 保留更新/撤销说明。George默认按需启用，不因角色配置创建always-on模式。
