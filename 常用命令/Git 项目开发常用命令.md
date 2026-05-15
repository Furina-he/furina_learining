---
tags:
  - git
  - 常用命令
  - 版本控制
created: 2026-05-15
---

# Git 项目开发常用命令

> 适用场景：日常项目开发、多人协作、分支管理、问题回滚
> 💡 推荐配合 SSH key 使用，避免反复输入账号密码
> ⚠️ 涉及 `--force`、`reset --hard`、`clean -fd` 的命令均为**破坏性操作**，执行前请三思

---

## 一、初始化与配置

### 1. 全局配置（一次性）

```bash
# 设置用户名和邮箱（提交记录会用到）
git config --global user.name "your-name"
git config --global user.email "your-email@example.com"

# 设置默认分支名为 main
git config --global init.defaultBranch main

# 让 git 输出带颜色
git config --global color.ui auto

# 设置默认编辑器（可选）
git config --global core.editor "code --wait"   # VS Code
git config --global core.editor "vim"           # Vim

# 查看所有配置
git config --list
git config --global --list
```

### 2. 仓库初始化

```bash
# 在当前目录初始化一个新仓库
git init

# 克隆远程仓库
git clone <repo-url>
git clone <repo-url> <target-dir>      # 克隆到指定目录
git clone -b <branch> <repo-url>       # 克隆指定分支
git clone --depth=1 <repo-url>         # 浅克隆（只拉最近一次提交，节省流量）
```

---

## 二、日常开发四件套

最高频的使用场景：**改文件 → 暂存 → 提交 → 推送**。

```bash
# 1. 查看当前工作区状态（最常用！）
git status
git status -s                # 简洁模式

# 2. 把改动加入暂存区
git add <file>               # 指定文件
git add .                    # 当前目录所有改动（含新增）
git add -u                   # 仅已跟踪文件的改动（不含新增）
git add -p                   # 交互式选择 hunk，精细暂存

# 3. 提交
git commit -m "feat: add login page"
git commit -am "fix: typo"   # add + commit（仅对已跟踪文件）
git commit --amend           # 修改最近一次提交（未推送时使用）
git commit --amend --no-edit # 修改但不改 commit message

# 4. 推送到远程
git push                     # 推送到默认上游分支
git push origin <branch>     # 显式推送
git push -u origin <branch>  # 首次推送并绑定上游
```

### Conventional Commits 提交规范

```text
<type>(<scope>): <subject>

feat:     新功能
fix:      修复 bug
docs:     文档变更
style:    格式调整（不影响代码运行）
refactor: 重构（非新增功能也非修复 bug）
perf:     性能优化
test:     增加/修改测试
chore:    构建/工具变更
revert:   回滚某次提交
```

---

## 三、查看历史与差异

```bash
# 提交日志
git log
git log --oneline                       # 一行一条，简洁
git log --oneline --graph --all         # 带分支图（推荐！）
git log -n 5                            # 最近 5 条
git log --author="zhang"                # 按作者过滤
git log --since="2 weeks ago"           # 按时间过滤
git log -p <file>                       # 查看某文件的修改历史
git log --stat                          # 显示每次提交的统计信息

# 差异对比
git diff                                # 工作区 vs 暂存区
git diff --cached                       # 暂存区 vs 最近一次提交
git diff HEAD                           # 工作区 vs 最近一次提交
git diff <branch1> <branch2>            # 分支间差异
git diff <commit1> <commit2> -- <file>  # 两次提交间某文件的差异

# 查看某次提交的详细内容
git show <commit-hash>
git show HEAD                            # 最近一次提交
git show HEAD~1                          # 上一次提交
```

---

## 四、分支管理（项目开发核心）

### 1. 分支基本操作

```bash
# 查看分支
git branch                       # 本地分支
git branch -r                    # 远程分支
git branch -a                    # 全部分支
git branch -vv                   # 包含上游绑定信息

# 创建 & 切换
git branch <name>                # 创建分支但不切换
git checkout <name>              # 切换分支（旧语法）
git switch <name>                # 切换分支（推荐，git 2.23+）
git checkout -b <name>           # 创建并切换
git switch -c <name>             # 创建并切换（推荐）

# 基于远程分支创建本地分支
git switch -c <local> origin/<remote>

# 重命名分支
git branch -m <new-name>         # 当前分支
git branch -m <old> <new>        # 指定分支

# 删除分支
git branch -d <name>             # 安全删除（未合并会提示）
git branch -D <name>             # 强制删除
git push origin --delete <name>  # 删除远程分支
```

### 2. 推荐的分支模型

| 分支          | 用途         | 来源          | 合并去向                |
| ----------- | ---------- | ----------- | ------------------- |
| `main`      | 生产环境       | -           | -                   |
| `develop`   | 集成测试       | `main`      | `main`              |
| `feature/*` | 新功能开发      | `develop`   | `develop`           |
| `fix/*`     | bug 修复     | `develop`   | `develop`           |
| `hotfix/*`  | 线上紧急修复     | `main`      | `main` + `develop`  |
| `release/*` | 发布准备       | `develop`   | `main` + `develop`  |

---

## 五、合并与变基

```bash
# 合并：把 feature 合并到当前分支（默认产生 merge commit）
git merge <branch>
git merge --no-ff <branch>       # 强制保留 merge commit（推荐）
git merge --squash <branch>      # 把多次提交压缩成一次

# 变基：把当前分支的提交"嫁接"到目标分支顶端（线性历史）
git rebase <branch>
git rebase -i HEAD~3             # 交互式 rebase（合并、修改、调整最近 3 个提交）

# rebase 中常见冲突处理
git rebase --continue            # 解决冲突后继续
git rebase --skip                # 跳过当前提交
git rebase --abort               # 放弃 rebase，回到原状态

# Cherry-pick：把某个 commit 摘到当前分支
git cherry-pick <commit-hash>
git cherry-pick <c1>^..<c2>      # 一段连续提交
```

### Merge vs Rebase 选择

| 场景         | 推荐操作       | 原因               |
| ---------- | ---------- | ---------------- |
| 公共分支（main） | `merge`    | 保留协作历史，避免改写他人提交  |
| 个人特性分支     | `rebase`   | 历史更整洁，便于 review  |
| 上线前整理提交    | `rebase -i` | 合并/重写消息          |
| 已推送的分支     | `merge`    | 切勿 rebase，否则破坏他人 |

---

## 六、远程仓库

```bash
# 查看远程
git remote -v
git remote show origin

# 添加 / 修改 / 删除远程
git remote add origin <url>
git remote set-url origin <new-url>
git remote remove origin

# 拉取 & 同步
git fetch                        # 拉取但不合并
git fetch --all --prune          # 拉取所有远程，清理已删除的分支
git pull                         # = fetch + merge
git pull --rebase                # = fetch + rebase（推荐）

# 推送
git push                         # 推送当前分支
git push origin <branch>
git push --tags                  # 推送所有 tag
git push --force-with-lease      # 安全的强推（推荐！）
git push --force                 # 暴力强推（危险，仅在确认无他人协作时）
```

---

## 七、撤销与回滚

> ⚠️ 这一节是"救命药"，请仔细分清楚每条命令影响的范围。

```bash
# 1. 撤销工作区改动（未 add）
git restore <file>               # 推荐（git 2.23+）
git checkout -- <file>           # 旧语法

# 2. 撤销已暂存的改动（已 add，未 commit）
git restore --staged <file>      # 推荐
git reset HEAD <file>            # 旧语法

# 3. 撤销已 commit（未 push）
git reset --soft HEAD~1          # 保留改动在暂存区
git reset --mixed HEAD~1         # 保留改动在工作区（默认）
git reset --hard HEAD~1          # ⚠️ 完全丢弃改动！

# 4. 撤销已 push 的提交（推荐用 revert，不改写历史）
git revert <commit-hash>         # 生成一个反向提交
git revert HEAD                  # 撤销最近一次提交

# 5. 紧急救命：误删分支 / 误 reset
git reflog                       # 查看所有 HEAD 变更记录
git reset --hard <reflog-hash>   # 跳转到任意历史点
```

### reset 三种模式对比

| 模式        | 工作区 | 暂存区 | 适用场景            |
| --------- | --- | --- | --------------- |
| `--soft`  | 保留  | 保留  | 撤销 commit 但保留改动 |
| `--mixed` | 保留  | 清空  | 撤销 commit 和 add |
| `--hard`  | 清空  | 清空  | 彻底放弃所有改动（⚠️不可恢复） |

---

## 八、暂存（Stash）

工作进行到一半，又要切分支处理紧急问题时用。

```bash
git stash                        # 暂存当前改动
git stash push -m "wip: 登录页"    # 带注释暂存
git stash -u                     # 包含未跟踪文件

git stash list                   # 查看所有暂存
git stash show -p stash@{0}      # 查看暂存内容

git stash pop                    # 恢复并删除最近一次暂存
git stash apply stash@{1}        # 恢复指定暂存（不删除）
git stash drop stash@{0}         # 删除指定暂存
git stash clear                  # 清空所有暂存
```

---

## 九、标签（Tag）

发版必备：给某个 commit 打标记。

```bash
# 创建
git tag v1.0.0                                # 轻量 tag
git tag -a v1.0.0 -m "Release v1.0.0"         # 附注 tag（推荐）
git tag -a v1.0.0 <commit-hash>               # 给历史提交打 tag

# 查看
git tag                          # 所有 tag
git tag -l "v1.*"                # 按模式过滤
git show v1.0.0                  # 查看 tag 详情

# 推送 / 删除
git push origin v1.0.0           # 推送单个 tag
git push origin --tags           # 推送所有 tag
git tag -d v1.0.0                # 删除本地 tag
git push origin --delete v1.0.0  # 删除远程 tag
```

---

## 十、常见场景速查

| 场景                       | 命令                                                          |
| ------------------------ | ----------------------------------------------------------- |
| 拉最新代码                    | `git pull --rebase`                                         |
| 看我改了什么                   | `git status` + `git diff`                                   |
| 提交一段改动                   | `git add . && git commit -m "msg"`                          |
| 修改最近一次 commit message    | `git commit --amend`                                        |
| 误提交了大文件                  | `git reset --soft HEAD~1` 重做                                |
| 错分支提交了代码                 | `git reset --soft HEAD~1` → 切分支 → 重新提交                      |
| 把 main 的最新改动合到 feature   | `git switch feature && git rebase main`                     |
| 紧急切走但改动没提交               | `git stash` → 切分支 → 回来 `git stash pop`                      |
| 想看某行代码是谁写的               | `git blame <file>`                                          |
| 找一段代码是哪个 commit 引入的     | `git log -S "代码片段" --all`                                  |
| 误删了文件                    | `git restore <file>` 或从历史 `git checkout HEAD -- <file>`     |
| 误删了分支                    | `git reflog` → `git switch -c <branch> <hash>`             |
| 强推之前先检查                  | `git push --force-with-lease`                              |

---

## 十一、`.gitignore` 速记

```gitignore
# 依赖
node_modules/
__pycache__/
*.pyc

# 构建产物
dist/
build/
target/
*.class

# IDE
.idea/
.vscode/
*.swp

# 系统
.DS_Store
Thumbs.db

# 环境变量
.env
.env.local

# 日志
*.log
logs/
```

> 💡 若已经把文件提交后才加 `.gitignore`，需要 `git rm --cached <file>` 把它从版本控制中移除。

---

## 十二、进阶技巧

### 1. 二分查找定位 bug

```bash
git bisect start
git bisect bad                   # 标记当前是坏的
git bisect good v1.0.0           # 标记 v1.0.0 是好的
# Git 会自动切到中间 commit，测试后：
git bisect good                  # 或 git bisect bad
# 直到定位到引入 bug 的 commit
git bisect reset                 # 退出二分模式
```

### 2. Git Worktree（多分支并行工作）

```bash
# 在 ../feature-x 目录创建一个工作树，对应 feature/x 分支
git worktree add ../feature-x feature/x

# 查看所有 worktree
git worktree list

# 删除
git worktree remove ../feature-x
```

### 3. 子模块（Submodule）

```bash
git submodule add <repo-url> <path>
git submodule update --init --recursive   # clone 后初始化子模块
git submodule update --remote             # 更新子模块到最新
```

---

## 十三、推荐工作流（个人开发版）

```bash
# 1. 开始新功能
git switch main
git pull --rebase
git switch -c feature/login

# 2. 开发中：小步提交
git add -p
git commit -m "feat(login): add form validation"

# 3. 同步 main 的最新改动
git fetch origin
git rebase origin/main

# 4. 推送
git push -u origin feature/login

# 5. 提交 PR / MR，合并后清理
git switch main
git pull --rebase
git branch -d feature/login
git push origin --delete feature/login
```

---

## 相关笔记

- [[常用命令/Docker 镜像清理指南及常用命令]]
