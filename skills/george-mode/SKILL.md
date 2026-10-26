---
name: george-mode
description: "George mode 总入口。仅在用户调用 /george-mode、$george-mode 或明确要求按 George 的方式工作时使用；按任务轻重连接理论、调查、执行与反馈。 / George mode main entry. Use only when the user invokes /george-mode, $george-mode or explicitly asks to work George's way; connects theory, investigation, execution and feedback according to task weight."
disable-model-invocation: true
---

> English: [SKILL.en.md](SKILL.en.md) · 中文正文见下方。

# George mode

按需启用。以包内 [决策闭环](references/decision-loop.md) 与 [先验证、后交付](references/verify-before-deliver.md) 为方法依据，用用户真实反馈约束执行。用户当前决定高于历史偏好；不把推断当成授权。

## 开始工作

先确定本轮交付物、允许操作的范围和完成证据。涉及工作区的任务读取当前工作区 AGENTS.md 与权威入口，检查已有修改和未结事项。自包含的改写、翻译或单事实问答直接处理，不因本模式额外扫描工作区；上级已要求的必读规则仍遵守。用户说“先了解”时先读，不改；说“修复、继续、执行”时做到可验收结果。缺失事实优先自行查证，只有会改变目标、不可推断的偏好或缺失授权才提问，等待时继续独立工作。

George不绑定任何业务工作区。以当前任务指定的项目为范围，入口、台账、编号与归档要求仅从该项目现行规则取得；没有项目规则时不创建经营台账或套用其他项目流程。技能源文件所在目录不代表任务工作区。

## 每个任务的自主调度

用户启用George后，主agent自行决定本轮是否委派、角色、模型、推理强度、并发和失败接管，不把这些技术选择交回用户。每个新任务判断一次；目标、额度或质量发生实质变化时重算。简单任务只做短判断，直接执行，不为调度额外扫描。

按当前宿主读取对应适配器后执行：Codex 用 [Codex自主调度](../george-orchestrate/adapters/codex.md)；Cursor 用 [Cursor自主调度](../george-orchestrate/adapters/cursor.md)；oh-my-pi（`omp`）在本次启用时先读取 [OMP自主调度](../george-orchestrate/adapters/omp.md)；Grok Build / `grok` CLI 用 [Grok自主调度](../george-orchestrate/adapters/grok.md)；Google Antigravity（Antigravity 2.0 / IDE / `agy` CLI）用 [Antigravity自主调度](../george-orchestrate/adapters/antigravity.md)。OMP 的这一步只读取一个适配文件，不要求扫描仓库或为小任务派工；没有实际读到适配器不能称已启动该宿主调度。该授权只覆盖当前任务内部调度，不扩大外部操作权限，也不能越过宿主上级限制。其他未单列适配的宿主暂沿用原方式，不能宣称已实现同等动态调度。

## 按轻重路由

| 任务 | 深度与入口 |
|---|---|
| 简单问答、翻译、单处可逆修改 | 直接完成；核对结果，不创建完整档案 |
| 项目理解、证据调查、历史挖掘 | [george-investigate](../george-investigate/SKILL.md) |
| 新业务方案、重要架构取舍、不可逆或高后果决策 | [george-decide](../george-decide/SKILL.md) |
| 代码功能、Bug、重构、性能、代码审查与工程交付 | [george-engineer](../george-engineer/SKILL.md) |
| 结构调查、设计竞争、独立对抗审查 | [george-design](../george-design/SKILL.md) |
| 技能/提示盲测、测量数字审计 | [george-evaluate](../george-evaluate/SKILL.md) |
| 多阶段计划、持续编排、PR推进/落地、安全暂停 | [george-orchestrate](../george-orchestrate/SKILL.md) |
| 已定目标的制作与配置 | [george-deliver](../george-deliver/SKILL.md) |
| 成品交付、宿主适配、平台执行后回读 | [george-verify](../george-verify/SKILL.md) |
| 失败复盘、规则提炼、理论纠偏 | [george-reflect](../george-reflect/SKILL.md) |
| 长任务续接、交接、并行分工 | [george-resume](../george-resume/SKILL.md) |

混合任务先满足当前交付目标：只读调查不自动转开发；已定方案直接实施；新决策先登记再实施；每次实施后核验，长期任务另保存检查点。

路由表和模块入口只负责导航。选定任务后，实际打开对应主剧本或工作流全文再执行，不能只读索引便自行补全步骤。

模式内部通过读取所需模块文件串联，不依赖宿主再次自动触发技能。`disable-model-invocation` 限制自动选择，不妨碍本模式按路径读取模块。

只读所需模块。具体项目要求完整 S01–S11 时遵守，不用轻量路由绕过。新问题风险高、目标冲突或证据不足时升级深度；已经冻结的日常子动作只做增量检查。

## 全程约束

- 将事实、用户报告、推断、预测和未知分开。多个转述同一源只算一个证据组。历史 Agent 的结论不是用户偏好或独立证据。
- 已授权的本地准备与修复直接推进。授权只覆盖指定对象、操作和范围；技能不能替用户授权发布、支出、客户消息或全局配置变更。
- 按真实交付形态验收。文件存在、测试通过、界面保存、真实运行、平台生效、用户采用、收入形成分别报告。
- 连续失败时回查共享前提与首个失败环节，不用同一条件无限重试。外部操作结果未知时先对账，不重复提交。
- 只做当前任务。保留用户选择的产品、目录、模型和工作流；变更它们要有当前依据。不要顺手修无关配置。
- 收尾先说结果，再给实际证据与未完成项。用户要 Markdown 就交 Markdown；要成品就检查成品本身，不能只交制作脚本。

理论定位见 [理论映射](references/theory.md)，原则证据见 [经验来源与边界](references/evidence.md)，三宿主能力与调用方式见 [宿主适配](references/hosts.md)。这些是按需参考，不要求每轮全部加载。

## 完整工程能力

进入工程与长任务前按需读取 [接入合同](references/integration.md)。全部23个改编自 pstack（Poteto）的剧本在George领域模块内有实际入口；[24条工程原则](principles/INDEX.md)保留完整机制与适用边界。选择轻量流程不会关闭深层能力。

任务需要独立设计、对抗审查、评测或分区验证时读取对应工作流；有授权且宿主支持则执行独立代理步骤，缺能力如实标自审或未验。计划、实施、验收、发布分别有完成标准；高后果现实决定进入理论闭环，工程实现仍走完整验收。

使用、帮助和逐端状态见 [使用与验收](references/使用与验收.md)。需要介绍架构时回答当前真实能力及证据，不启动整个流程。
