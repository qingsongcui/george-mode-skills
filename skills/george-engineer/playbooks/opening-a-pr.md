# 工程成果与PR交付

1. 读取当前工作区与用户修改，检查最终diff、行为、依赖和必要文档。不要用reset-hard或无选择git add覆盖别人的工作。隔离需要时使用新worktree，已有合适工作树优先复用。
2. 按 [代码质量](../workflows/code-quality.md) 和 [技术写作](../workflows/writing.md) 清理。复杂/高后果改动独立审查，真实检查先完成；未验证保留标签。
3. 任务需要Git交付时将改动组织为可回放验证单元。已有用户历史不随意改写；只暂存本轮拥有的路径，相关失败测试在修复前可单独展示。
4. 选择当前可用forge/原生PR工具，按仓库模板写标题和描述，解释用户问题、变化、证据、风险及范围。draft/ready按实际完成度和用户要求，不强制所有PR标ready。
5. 依赖PR按base-branch链，一个拓扑写者；独立变更才从trunk分支。PR创建后读取真实链接和状态；宿主要求附件关联时执行。
6. 创建PR不自动启动babysit或合并。用户要求后续推进时路由 [PR推进](../../george-orchestrate/playbooks/babysit.md)；已授权合并则 [Shipping](../../george-orchestrate/playbooks/shipping.md)。
7. 本地成品或只读任务无需强制开PR，直接交付实际产物和验证。

来源：pstack `poteto-mode` 的 opening-a-pr 剧本（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；删除了重置未知工作、强制非draft和一律开PR等不适合George的前提。
