# George mode 独立安装包

本包包含11个技能、自包含的决策闭环与验收参考（skills/george-mode/references/decision-loop.md、verify-before-deliver.md）、五个宿主适配器及运行工具。无需作者工作区、业务台账或历史对话。

解压到自己长期保留的目录，从包根目录运行：

```sh
python3 scripts/verify_package.py
python3 scripts/install.py
python3 scripts/install.py --apply
```

需要Python 3。verify_package检查完整性，install不带--apply时预览；安装命令加 --apply 后建立当前用户的技能链接及OMP默认profile命令。已有同名内容会拒绝覆盖。只安装实际使用的宿主时可手动将整套george-*目录放入该宿主技能目录，保留兄弟目录关系。OMP独立profile按宿主说明安装命令别名。宿主与模型服务需自行具备；技能包不携带账号或凭据。

Codex调用 $george-mode，Cursor、Grok CLI 与 Antigravity 调用 /george-mode，OMP调用 /skill:george-mode 或安装后的 /george-mode。Grok 发现已有 ~/.agents/skills 链接，安装器不另写 ~/.grok/skills；Antigravity 链接到 ~/.gemini/config/skills。当前项目规则从该项目读取，不自动继承任何其他项目规则。

安装以链接方式运行：可解压到任意位置，安装后不要直接移动源目录；迁移先从旧位置运行 python3 scripts/install.py --remove --apply，再从新位置安装。卸载只移除指向本包的链接。

GitHub watcher为可选功能，需要Bun与gh；使用前在其pstack目录按锁文件安装依赖。其他Python运行工具使用标准库。环境依赖不等于作者工作区依赖。

发行包不包含原始会话、私人研究、工作簿、账号设置或旧版本验证档案。包内文件hash见 PACKAGE-MANIFEST.json；历史效果不承诺在新环境复现。
