# dmrentals-preview
雕马 HTML 原型预览库：集中保存、公开访问并持续更新多个 HTML 页面

- [在线预览目录](https://jieqiqiu987-cmyk.github.io/dmrentals-preview/)
- [新增、更新、删除指令模板](./指令模板.md)
- [发布 Skill](./skills/dmrentals-preview/SKILL.md)

每个原型存放在 `previews/<根据内容自动命名的slug>/index.html`。
`sites.json` 保存页面目录；首页同步展示。更新默认保留原链接。

在其他电脑安装 Skill：把 `skills/dmrentals-preview` 复制到 Codex skills 目录，默认 `~/.codex/skills/`。
发布需要仓库写入权限及 GitHub 认证；访问公开页面不需要登录。

现有 GitHub Pages 配置继续使用；新建仓库时在 Settings → Pages 选择 main 分支根目录发布。
