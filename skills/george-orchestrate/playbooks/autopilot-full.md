# 独立队列自动推进

前提：用户已授权实施该队列；合并仅在本轮授权覆盖时进行。只要计划就输出计划而不执行。相互依赖变更走autopilot-stack。

1. 固定队列边界和完成谓词，每个独立PR一个owner，从实现到获准交付负责；根协调者负责独立验证，不把owner自测当最终verdict。
2. 每个owner独立worktree、分支与brief，先理解/设计/实现。合适时早开PR让CI并行，未完成按仓库规则用draft；不得把早开PR当完成。
3. owner报告code-ready精确SHA、基线、命令和证据，冻结该轮写入。根派未参与作者的verifier按风险矩阵测真实行为，记录版本绑定verdict；负责人核实报告。
4. owner处理冲突、评论和CI，报告每一个后续SHA。行为重大变化重跑对应覆盖矩阵；小改动也由独立者核对受影响行为。旧head绿灯不替新head，旧verdict不自动复用。
5. 合并前核对trunk变更是否影响调用、契约、运行、依赖或集成点。相关变化先rebase/整合再验证；无关漂移写依据。patch-id可帮助判断差异，不单独证明整合安全。
6. 合并前新head CI、独立证据、forge门槛和用户授权同时满足，才进入Shipping；缺授权交付merge-ready。禁止owner自行把不通过改成通过。
7. 用户明确暂停即停止派发，通知所有owner停止新外部动作，保存现场。根最终核对每个实际合并状态与用户目标。
产物：逐PR owner、head、验证结果、CI/交付状态及未完成原因。
来源：pstack `skills/poteto-mode/playbooks/autopilot-full.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；适配 [George接入合同](../../george-mode/references/integration.md)。
