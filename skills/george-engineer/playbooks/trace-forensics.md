# 已有追踪数据取证

1. 识别给定 cpuprofile、JSON/gzip、spindump、heap snapshot 的格式、采样窗口与完整性。分析固定数据，不擅自重新运行改变条件。
2. 大数据先用适合格式的解析器转成可查询表/SQLite，每行一个 sample/frame/node；保留原文件及转换命令。
3. 查热点、调用链、等待线程与等待原因；内存问题追保留链到根。聚合数字必须说明分母和重复采样口径。
4. 通过数据自带符号映射文件/符号/行；缺失符号要补映射或标注无法归因，不凭函数名猜源码。
5. 有配对捕获则按相同口径比较；只有单份数据，结论标成证据支持的假设。给出能区分替代解释的下一观察。
6. 交付可追溯诊断、查询和证据；只有任务已含修复才转 bug/perf。

来源：pstack `skills/poteto-mode/playbooks/trace-forensics.md`（MIT，© 2026 Lauren Tan，见包根 NOTICE.md）；改造依据见 [接入合同](../../george-mode/references/integration.md)。
