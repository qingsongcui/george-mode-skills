# 可运行工具

所有路径指本技能目录。工具不自动派发Agent、修改模型、发布或合并。Python工具只依赖标准库；GitHub watcher另需Bun与gh。

## 持久编排

`python3 tools/state.py --store /绝对路径/task.sqlite init` 创建任务工作台。其他操作通过 `--input /绝对路径/request.json` 接收JSON，不把用户内容插入shell。

| 操作 | 输入 |
|---|---|
| unit.put | id、owner、version（head或内容hash）、scope、state（pending/running/code-ready/blocked）；换owner额外handoff=previous-owner-stopped |
| verdict.record | unit、version、verifier、level、evidence（真实绝对文件）、observed_at |
| verdict.check | unit，可选required_level；缺少当前版本且文件哈希完整的指定层证据时退出1 |
| inbox.push | 唯一id、unit、sender、report；相同id重试幂等，冲突内容拒绝 |
| inbox.read | 无；只读未ack消息，崩溃后可再读取 |
| inbox.ack | id、evidence（处理后回执）；归档保留原消息，不删除 |
| gate.put | id、question，可选suggested_default；默认值不能关闭gate |
| gate.resolve | id、answer、source（实际用户决定位置） |
| frontier.set | items依次含id、parent（根为null）、version、source、observed_at；父先子后，无重复 |
| standing.add | id、instruction、source |
| status | 无；完整事实与内容hash，不用分类计数代表内容变化 |

level为static、unit、real-surface、independent-real-surface、blocked、failed。每个unit+version+scope保留当前裁决，历史变化追加至事件表；后续失败覆盖旧成功。独立者不能是owner，证据必须存在并保存hash；工具不能认证真实身份或证据语义，负责人仍要查内容。

SQLite事务防并发覆盖。frontier仅拓扑或版本改变增加generation，更新观察时间不增；远端head须来自forge读回，不能拿本地旧ref冒充。工具不自动推断安全或授权。

## 计划检查

`python3 tools/check_plan.py templates/plan.json` 检查DAG、所有权冲突、每单元验收及unit/live/perf适用性。project_root必须是绝对路径，文件按此根解析并规范化路径/符号链接；使用明确路径，不支持glob展开；工具不运行任务，也不判定理由是否正确。

## GitHub状态监视

`tools/pstack/watch-pr/` 保留Poteto的读取、状态机及测试。改造为无自动安装，外围加进程组硬时限。首次依赖安装在 `tools/pstack/` 显式运行 `bun install --frozen-lockfile`。

单次状态：`python3 tools/watch_pr.py --deadline 55 --pr 123 --status-only`。

固定队列：`python3 tools/watch_pr.py --deadline 55 --queued-stack --stack-prs 123,124 --interval 10 --timeout 45`。先独立核对PR base链，脚本不证明列表顺序正确。长期监控使用已获准的宿主自动化。

读取JSON/NDJSON的kind、terminal、observedAt、head和blocker。STATUS/exit0不是通过；READY不是独立验收或forge最终允许合并；WAITING merge-queue不是合并；COMPLETE表示范围内PR实际已合并。wrapper超时退出5并杀该进程组，保留未知状态。

watcher只读GitHub，不支持Origin/其他forge，不创建/回复/合并PR。其他forge用实际原生工具按同语义读取，不声称本脚本已适配。

## 来源与改造

state.py重做原始orch持久机制，补可恢复消息、全文内容变化、稳定generation和证据hash。原始源码快照在研究目录，不是活动执行入口。固定十lane计划检查改为风险可裁剪结构合同；工作树清理使用可恢复归档与现场审计，不按旧工具safe分类自动删除。

工具源码：[状态工作台](state.py)、[计划检查](check_plan.py)、[有界监视入口](watch_pr.py)、[监视器实现](pstack/watch-pr/cli.ts)。

只读查询使用SQLite只读事务，不获取写锁；范围变化与版本变化都会使旧裁决失效。

[监视状态机](pstack/watch-pr/policy.ts)。

## OMP 本轮角色

仅 oh-my-pi（`omp`）使用 `omp_roles.py`；Codex/Cursor 不读取这些角色。

```text
python3 tools/omp_roles.py prepare --project /当前项目 --input /本轮/roles.json --receipt /本轮/roles-receipt.json
python3 tools/omp_roles.py cleanup --receipt /本轮/roles-receipt.json
```

输入形状为 `run_id` 与 `roles[]`；每项包含 `name, description, model, thinking, tools, brief`。名称必须以 `george-omp-` 开头且本轮唯一。模型与thinking先从宿主当前目录核实，不在本工具固定品牌或价目表。创建冲突拒绝整批，清理仅操作该项目对应角色且内容hash未变的本轮文件。

工具只准备项目 `.omp/agents` 文件，不启动推理、不改全局模型或其他宿主角色。回执中的 requested 字段不是实际执行证据；主控通过原生 `task.tasks[].agent` 传角色名后，再从子会话核对实际模型、thinking、状态和usage。原生工具白名单放角色frontmatter，不把 eval 专用的 `tasks[].tools` 当作同一字段。

协议与边界见 [OMP适配器](../adapters/omp.md)。包根 `scripts/probe_omp_autonomy.py` 提供有界原生试跑、已停止检查点恢复、独立质量失败接管及证据回放；失败保留，不把目录存在或worker自述当验收。
