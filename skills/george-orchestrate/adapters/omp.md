# OMP 自主调度协议 0.3.3

适用宿主是 oh-my-pi 的 `omp` 命令，不是 OpenCode 或 oh-my-opencode。用户在 OMP 显式启用 George 后，本会话后续每个新任务都由主 agent 判断是否委派，并选择职责、模型、推理强度、并发、预算和恢复；不把这些技术选择交回用户。目标、授权、质量或资源发生实质变化时重算。主 agent 负责整合与最终验收。本协议不扩大平台操作、支出、发布或凭据权限。

## 1. 先判断收益，不为调度而调度

比较委派能带来的胜任经济模型、独立产物流、上下文隔离、独立验收收益，与启动、简报传递、合并和预计返工成本。边界明确的小任务主控直接做，一句话说明即可，不枚举全仓或启动 worker。需要隔离上下文或独立验收，即使严格串行也可以委派。不能仅因“能并行”就扩队，也不声称按名字选了模型就已测出节省费用。

需要委派时留下四项简短检查：阻塞前置、独立产物、共享可变对象、最小安全拆分。依赖先完成并由主控验收，才派下游；重叠写区使用独立 checkout 或串行，不能只改 agent 名字就认为隔离。

## 2. 以本轮真实能力为边界

先看当前 `task` schema。按需用只读的 `omp --version`、`omp config get <key>`、`omp models --json`、`omp usage --json` 核查，不整份输出含账号信息的配置或额度。RPC `get_state.dumpTools` 可证明实际工具参数；代理来源与角色定义按本机发行版的 `omp://task-agent-discovery.md` 核对，不能从 Codex/Cursor 补造参数。

- batch 开启时为 `task({context, tasks:[{name?, agent?, task, solutionSpace, ...实际可用字段}]})`。`context` 是共享简报，单元给绝对路径、职责、写区、禁改区、交付与验收；子 agent 不继承完整父会话。`solutionSpace` 描述问题开放度，不写工作量或同伴协调。
- `task` 没有通用的 `model`、`subagent_type` 或 `run_in_background` 字段。默认通用任务省略 `agent`；调查、机械处理、审查按当前目录选胜任类型，不把只读类型派去写文件。
- 当前会话若 `task.enableEffort=false` 或 schema 没有 `effort`，绝不传每任务 `effort`。`solutionSpace` 只在所选代理配置为 `auto` 时参与分类，不能把它当作强度开关。
- schema 真有 `effort` 才可用 OMP 的 `lo/med/hi`。这是按所选模型能力和 `task.maxEffort` 映射、夹顶的相对档位，不等于绝对 low/high/max。
- 模型目录、角色配置、参数被接受、宿主运行元数据、后端实际服务和实收费用是不同证据层。目录存在不证明调用可用；切换父会话模型不证明子 agent 换了模型。
- `tasks[].tools` 绑定的是父 eval kernel 已注册的工具名，不是 `read/write/bash` 原生工具白名单；不需要共享 eval 工具时省略它。原生工具权限写在项目角色 frontmatter 的 `tools`，不能靠猜这个参数来隔离。

模型、角色与参数快照写入本任务目录，不写固定模型品牌/价格到技能正文。只保存版本、工具字段、允许角色、selector、支持的 thinking、当前限制、脱敏额度及发现来源。不能观察的字段保留 `unknown`，不从请求值回填实际值。

## 3. 任务专属职责、模型和推理选择

先定本轮职责和验收，再选胜任的经济组合。明确机械任务优先已验证可胜任的较经济配置；有界实现用足够的中档配置；不确定根因、复杂设计与高后果验收优先更强判断。价格未知时只能称保守选型，不能宣称最便宜或已节省费用。

OMP 可从项目 `.omp/agents/*.md` 在执行期发现新角色。优先用 [本轮角色工具](../tools/omp_roles.py) 为当前任务创建独特 `george-omp-` 名称，将实际已发现的 selector 与受支持 thinking 写入 frontmatter，再通过原生 `task` 的 `agent` 调用。角色简报与工具权限按本轮需要，不创建通用常驻超级角色。准备示例：

```text
python3 <George源>/skills/george-orchestrate/tools/omp_roles.py prepare --project <当前项目> --input <本轮roles.json> --receipt <本轮roles-receipt.json>
```

输入包含 `run_id` 与 `roles`；每角色给 `name, description, model, thinking, tools, brief`。工具只准备角色与归属回执，不派发 agent、不授予模型权限，也不保证请求模型实际生效。先确认项目目录与当前 task 的 cwd 一致；不把另一个子目录里的角色当成本会话已发现。角色名不能覆盖用户已有或固定角色。

动态角色真正生效需要在 `tasks[]` 单元的 `agent` 字段传刚创建的角色名；不能派内置 `task` 再让 worker 读角色 Markdown，就声称已换模型或强度。没有 `task.model/effort` 字段不表示没有角色级路由。当前 schema 的 `agent` 为 string 时，提示中的旧目录不是枚举白名单；执行期会重新发现本项目角色。只有实际 unknown/disabled/depth 拒绝后才降级，并保留这次失败。

`task.agentModelOverrides[agentName]` 优先于 agent frontmatter，再到角色/父会话回退。避开已占用名字，不改五个内置角色的 override 来实现本轮选型。模型别名只按本轮 `modelRoles` 展开；`m1/m2` 仅用户实际打标时可用，不能伪造 composer 标签。frontmatter thinking 和 selector 后缀只选一种明确表达，随后核对运行结果。

开发期原生试跑中，角色请求 `medium`，对应 worker 实际记录为 `low`，角色仍启动并完成。因此不能依赖“不支持的 thinking 必定拒绝派发”；选型前核对支持集合，派发后以同一 worker 的运行记录核对。具体归一化或默认回退机制未证实，不从这一次结果推断所有模型的映射规则。

宿主不允许新角色、角色被禁用或 schema 拒绝时，选最接近且权限胜任的现有角色；没有合格者由主控接管，独立验收缺口仍未满足。不得为选模型反复热切换父会话或改 Codex/Cursor 设置。

本轮角色只写项目 OMP 目录。已有同名路径、被他人修改的角色不得覆盖。worker 停止并读回结果后，用同一工具 `cleanup --receipt <本轮roles-receipt.json>` 仅清理自己且 hash 未变的角色；他人的角色和配置保留。任何必要持久变更必须是 OMP 专属、先备份、可回退，并保留其他 provider 与用户设置。

## 4. 预算、额度和并发

读取本轮实际 `task.maxConcurrency`、`task.maxRecursionDepth`、异步和 provider 限制。宿主上限不是目标并发数；默认从最多 2 个独立 worker 起步，预留主控验收资源。worker 默认不再向下派发，除非确有独立收益且深度允许。

`omp usage --json` 可查询部分 provider 的额度；只白名单投影 provider、窗口、共享组、状态和剩余量，不存邮箱、账户 ID、凭据或原始 provider metadata。百分比是账户窗口，不是本任务 token 或美元预算。相同账户/共享组不能重复相加；不能把池中另一个账户的余额当作本 worker 已绑定余额。没有可靠绑定时标 `unknown`。

未知额度不等于耗尽。对未知资源只做短、有界试跑；起步 1 个 worker，若独立产物确有收益且已有成功回执，可扩到 2 个。已观察到相关硬限额则停止受限资源新派发；额度紧张时减少并发，优先整合与必要验收。模拟低额度必须独立标 `simulated`，不能冒充现场 429，也不能人为耗尽、购买额度、使用 reset 权益或切换未授权账户。

每次派工设可观察的截止、同类重试最多 1 次和总 worker 数/请求数边界。`task.softRequestBudget` 是请求次数软门槛，不是 token/金额硬上限；`task.maxRuntimeMs=0` 表示无限制，不能把一句超时简报当宿主硬限制。需要硬边界时可用本轮 `--config` overlay 或项目级配置，不改全局；仍不可取消其他任务的 worker。

依赖链的主控截止按关键路径累加，不拿单个 worker 的上限套整条串行链。若产物已完成但主控还没收尾，先区分协调截止与 worker 超时；保存检查点后可有界续接一次，不重复派发已验收阶段，也不通过不断扩大预算把失败改成成功。

## 5. 派发、接收与真实验收

1. 主控保存本轮调度摘要：task/version、reason、units、depends_on、owner、write_scope、role、requested_model/thinking、selection_reason、quota/price 或 unknown、concurrency、deadline、retry_limit、acceptance。小任务无需数据库或完整档案。
2. 独立单元用同一个 `tasks[]` 批次启动以实际并行；依赖单元分批，主控验收前置后才发下一批。共享写区串行或独立 checkout。无 Git 项目使用明确隔离目录，不盲传 `isolated:true`。
3. 只有原生工具成功返回 ID 才记 running。`async.enabled=true` 时后台 job 返回不等于完成；主控继续独立工作，完成通知自动送达，无事可做才 `wait`，不空转轮询。
4. 按实际宿主使用 `agent://<id>`、`history://<id>`、`proc://<id>` 查看回执/进度，`write agent://<id>` 传修正；不能照抄 Codex 的 spawn/wait/resume API。主控必须自己读取产物、运行验收并记录命令与真实结果，worker 的 PASS 不是验收证据。
5. OMP 返回的 `resolvedModel`、`resolvedThinkingLevel`、`usage/tokens/requests`、lifecycle 和子会话消息可作为宿主观测；RPC 可用 `get_subagents`、`get_subagent_messages` 和会话统计补充。当前已观测的子会话条目是 `model_change.model` 与 `thinking_level_change.thinkingLevel`，不是猜测的 Pi 字段。工具面暂时拿不到就写 unknown，由验收器补取；不要为补一个不可见字段反复扫描、打印完整原始 session 或私有 thinking。后端服务身份与真正账单仍可能不可观察；不可把 catalog 估价当实付。
6. 高后果结果另派无实施历史的验证者；只给需求、产物与验收条件，不给实施者结论。主控整合版本后重验受影响部分，不能把多个相同模型的赞成当独立事实。

## 6. 失败恢复、停止与续接

- 输入缺失：记录原始失败/缺失，能由任务上下文补齐就先补再续派一次，不能虚构输入。
- 环境失败：先修最早前提（目录、依赖、权限、schema），不要把环境错归因于模型能力。
- 能力或质量不足：升级模型/推理一次或主控接管，验收标准不降。模型套餐/401/403/429 单独分类；有已授权可用替代才切换，不能原样循环。
- 超时：核实是否仍有有效进展。需要停止本任务 worker 时使用实际 `write proc://<id>/kill` 或可用的 OMP cancel；确认停写并检查部分产物后才交新 owner。取消 agent 不证明其后台进程已清理，另核查本任务进程。
- OMP 的 idle/parked 按实际消息机制尝试续接，必须取得同一 worker 的新执行证据才算恢复。开发期历史列表出现过 parked，但 RPC registry 为空且未完成 parked→执行的验证，不能把空 registry 当成不存在 parked。硬 aborted/cancel 后不可假称 resume 同一进程：本机试跑取得宿主明确拒绝向 hard-aborted worker 发消息/复活的回执；改用新 worker 与合并后的任务合同。不要唤醒无关历史 agent。
- 运行中目标、额度或质量变化：先通知受影响 worker，隔离共享写状态，再按新目标重排。达到重试边界仍失败则主控处理或保存精确阻塞，不让用户决定技术角色/模型。
- 深度设置存在不等于拒绝路径已验证。角色缺少 task 权限、`spawns:none` 或 worker 自行拒绝尝试，均不能证明宿主执行过递归深度拒绝；需同一子会话的实际嵌套调用及匹配的宿主错误回执。

长任务沿用 [state 工具](../tools/README.md) 的 owner/version/scope、inbox、blocked/failed 和版本绑定验收；状态文件不是原生派发器。恢复先核对产物版本与旧 owner 状态。对话结束、OMP 退出或进程取消后，技能不会自行成为后台守护服务；下次显式启用/有效检查点续接再恢复。

## 7. 接入与回退边界

仅 OMP 读取本文件。保留 Codex 的 `codex.md`、Cursor 的 `cursor.md`、各自配置与历史验收。本协议不向其他宿主注入 task 参数、OMP 角色别名、effort 或账户语义。一次启用的自动范围是当前 George 会话内逐任务判断与本任务生命周期，不是全局 always-on，也不承诺跨进程自行运行。

回退应只移除共享入口的 OMP 分支与本轮新增 OMP 资源；共享文件先合并后续修改，不用备份盲目覆盖其他 agent 的工作。仅按角色清单清理本任务的未改角色，保留历史证据和失败记录。
