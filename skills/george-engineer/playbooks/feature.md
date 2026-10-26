# 功能与接口开发

进入条件：明确要新增或改变行为。纯解释请求转调查；已选定设计直接接着做。
1. 读取 [结构调查](../../george-design/workflows/how-why.md)，沿真实调用路径确定调用者、输入、状态、边界和现有约束。先写数据形状与不变量，后写逻辑。
2. 有实质架构选择时读 [设计竞争](../../george-design/workflows/architect-arena.md)。至少比较结构上不同的方案；普通局部修改无需比赛。重要产品/架构取舍关联 george-decide 的事前依据。
3. 为非平凡多步任务留下四项吞吐检查：阻塞前置、独立产物流、共享可变对象、最小安全拆分。不能适用的项说明原因。共享类型先定，之后才并行。
4. 用 [编排合同](../../george-orchestrate/SKILL.md) 分配实现与独立审查。每个工作单元给出文件所有权、调用者例子、数据形状、禁改区、验收证据。跨模块耦合功能由一个 owner 统筹；不让几个代理同时写共享接口。
5. 先完成一条可运行的纵向路径，再铺开独立分支。每个单元完成即核验；共享原语变更遍查所有消费者。发现反证撤掉它支持的无效改动。
6. 运行 [项目验证](../../george-verify/workflows/project-verification.md)，覆盖真实正常路径、关键失败路径、持久化/重启或权限边界。错误表面、无法观测、inconclusive 都不能记通过。
7. 有争议或高后果变更走 [对抗审查](../../george-design/workflows/interrogate.md)。按可验证顺序组织交付：基础、功能、集成。需要 PR 时进入 [PR交付](opening-a-pr.md)。
交付：用户行为变化、选择及理由、验证证据、实际未完成项。

来源：pstack `skills/poteto-mode/playbooks/feature.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；改造依据见 [接入合同](../../george-mode/references/integration.md)。
