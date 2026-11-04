---
name: dmrentals-preview
description: 将 HTML 原型新增、更新或删除到 jieqiqiu987-cmyk/dmrentals-preview，并发布 GitHub Pages 可分享链接。用户要求管理雕马预览库时使用。
---

# 雕马预览库发布

目标仓库：https://github.com/jieqiqiu987-cmyk/dmrentals-preview
预览入口：https://jieqiqiu987-cmyk.github.io/dmrentals-preview/

## 工作流程

1. 使用现有干净 checkout；没有时通过 Git clone 到当前工作目录。确认 origin 是目标仓库，读取最新远端 main，存在他人未提交改动时另建干净 checkout。不要覆盖其他页面。
2. 根据本次用户需求及 HTML 内容自动总结中文标题、一句话简介和简短英文 kebab-case slug，不让用户额外命名。新增时遇到重名，追加日期或递增后缀，禁止覆盖。更新保留原 slug 和访问地址；用户指定重命名时再调整路径。
3. 新增内容位于 previews/<slug>/index.html。保留交互；图片、CSS、JS 等依赖必须一并放入该目录并采用相对路径。不得留下 file://、localhost、127.0.0.1 或本机绝对路径。真实后台能力不能靠静态托管实现，应明确缺失功能。不要把凭据或非公开业务数据一起公开。
4. 通过本 skill 的 scripts/manage.py 同步页面和 sites.json、首页。脚本只修改本地文件；发布步骤仍需执行。文件夹输入须包含 index.html，且仅包含需要发布的素材。更新会整体替换该页面文件夹，因此必须准备完整资源集。
5. 运行脚本后检查 git diff、资源路径和关键交互，确认改动只涉及目标页面、sites.json 和首页。提交本次改动并 git push origin main。用户明确要求新增、更新、删除并部署时已授权相应发布，无需重复确认；目标不明确时先询问具体页面。
6. 使用 GitHub CLI/API 查看仓库 Pages 配置；已有配置保持不变。尚未配置时，启用 main 分支根目录发布。不要在每次普通内容变更时改发布方式。等待对应提交的 Pages 构建成功，再用 HTTP 检查首页和页面（删除检查目标返回 404），返回访问链接及提交号。CDN 可能延迟，不能只凭 push 成功声称已上线。

## 本地命令

脚本路径以当前已加载的 SKILL.md 所在目录解析，不能硬编码其他电脑的用户目录。

```bash
python3 <skill目录>/scripts/manage.py --repo <仓库路径> add --slug <自动slug> --name '<中文标题>' --summary '<简介>' --source <HTML或完整资源文件夹>
python3 <skill目录>/scripts/manage.py --repo <仓库路径> update --slug <已有slug> --name '<中文标题>' --summary '<简介>' --source <HTML或完整资源文件夹>
python3 <skill目录>/scripts/manage.py --repo <仓库路径> delete --slug <已有slug>
```

删除仅移除对应目录和目录项，通过 Git 历史可恢复。未指定 slug 时根据用户链接或标题在 sites.json 中唯一定位；存在歧义先询问。禁止删除整个仓库、历史或其他页面。

## 认证与跨电脑

优先使用可用的 GitHub connector 或已认证 git/gh。缺少写入认证时，完成本地内容后说明未推送，并指导用户 `gh auth login`；不要索要 token 到聊天。没有 gh 时可从官方渠道安装 GitHub CLI。不要把本机密码或令牌打包到 skill。

其他电脑浏览页面无需安装 skill 或 GitHub 登录。其他电脑需要发布时，将仓库的 skills/dmrentals-preview 文件夹安装到该电脑 Codex 的 skills 目录（默认 ~/.codex/skills），并使用对目标仓库有写权限的 GitHub 账号认证。不得声称任意账号都有发布权限。
