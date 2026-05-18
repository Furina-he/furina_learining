---
来源: https://linux.do/t/topic/1015067
标题: 纯小白 WSL 入门教程（附CC和Codex配置）
作者: W
分类: 文档共建
tags: [linuxdo, 人工智能, 配置优化, Linux]
保存时间: 2026-05-19 00:35:02
评论数: 0
---

# 纯小白 WSL 入门教程（附CC和Codex配置）

<div data-theme-toc="true"> </div>
进 L 站也有一段时间了，白嫖了各位佬的各种资源，发现自己竟然一篇帖子也没发过😣，今天就来发一个关于 WSL 的基础教程来回馈一下社区，本人也不是大手子，如有错误还望各位佬指正修改，也欢迎各位佬来补充。

> [!NOTE]- 碎碎念
> 其实快三级了，来凑一下点赞，随便弄个徽章😋

# 关于 WSL

WSL（Windows Subsystem for Linux）（Windows Linux 子系统）
或许有人会问装 WSL 干嘛，WSL 更轻量，可以用来学习 Linux，做开发，且更方便与 Win 之间切换互通，我第一次了解到它是在 Win 上用 docker 的时候，

还有就是很好玩😋

# 关于终端软件

过程中要一直使用终端，可以直接用 Win 自带的终端，顺便也推荐几款终端：

## [Tabby](https://tabby.sh/)

个人一直在使用，主要是现代美观，还是开源软件，可以配合插件，有中文

## [MobaXterm](https://mobaxterm.mobatek.net/)

有免费和收费两个版本，免费就够用了，听别人说好用，不过不怎么好看（个人感觉）

## [Termius](https://termius.com/)

有手机版和桌面版，这个我多用在手机上连接 SSH，没用过桌面版，主要是 Github 学生包里面有这个，而且我有时需要用手机连 SSH，看起来挺美观，但是没有中文

# 安装 WSL

## 1. 启用 Windows 功能

搜索 “启用或关闭 Windows 功能”

![WSL1](https://linux.do/uploads/short-url/ffq4t3lyUKP1ewWjY7b5DpQpKlu.png)

开启下面两项

![WSL2](https://linux.do/uploads/short-url/hFPYnLroZP7HIzJju1NHefqtC8U.png)

## 2. 安装 Linux 并将其移动到其他盘

开启终端 powershell，将 WSL 默认版本设置为 WSL2
``` powershell
wsl --set-default-version 2
```
再输入以下指令列出所有可选的版本
``` powershell
wsl --list --online
```
![WSL3](https://linux.do/uploads/short-url/pLSZ1kGk3K381P3b2skyUD7UXHi.jpeg)

新手推荐使用 Ubuntu，我日常用的是 Ubuntu-24.04，不过我也装了个 archlinux，喜欢折腾的可以试试，按自己的喜好选择即可，下面开始安装

[quote="平衡, post:40, topic:1015067, full:true, username:hengnix"]
补充一下安装 WSL2 的时候可以使用 `--location` 指定安装位置，比如

```
wsl --install archlinux --name Arch --location D:\ArchLinux
```

这样可以省略后续迁移的步骤了
[/quote]

``` powershell
wsl --install <自己选择的发行版的NAME>
# 例如
wsl --install Ubuntu-24.04
```
等待安装，如果下载较慢可以试着开启代理
安装完成后根据引导创建用户设置密码
默认安装的发行版位置在 `C:\Users\你的用户名\AppData\Local\wsl` 如果后期安装的东西多了会很占空间，所以最好做个迁移
输入 `exit` 退回 powershell，输入以下命令导出自己的发行版
``` powershell
wsl --export <发行版名称> <导出路径>
# 例如
wsl --export Ubuntu-24.04 D:\WSL\Ubuntu-24.04\Ubuntu-24.04.tar
```
然后注销原发行版，同时会删除默认位置的发行版
``` powershell
wsl --unregister <发行版名称>
# 例如
wsl --unregister Ubuntu-24.04
```
将导出的发行版导入到自己选择的位置
``` powershell
wsl --import <自己起的发行版名称> <导入位置> <导出的发行版.tar压缩包所在位置>
# 例如
wsl --import Ubuntu-24.04 D:\WSL\Ubuntu-24.04 D:\WSL\Ubuntu-24.04\Ubuntu-24.04.tar
```
现在就可以删除导出的.tar压缩包了（如果要做备份那可以保留）
下面是一些常用的 wsl 命令：
``` powershell
wsl --list --verbose # 或 wsl -l -v 列出所有已安装的发行版及使用的 WSL 版本
wsl --set-default <发行版名称> # 设置默认发行版，例如 wsl --set-default Ubuntu-24.04
wsl --shutdown # 关闭所有启动的发行版
wsl -d <发行版名称> # 进入发行版，例如 wsl -d Ubuntu-24.04
wsl # 进入默认发行版
```

## 3. 配置自己的发行版

### 用户问题

有时进入自己的发行版后可能是 root 用户，可能是你未创建其他用户，自己找教程创建，然后设置默认用户，打开配置文件
``` bash
sudo vim /etc/wsl.conf
```
![WSL4](https://linux.do/uploads/short-url/42KjWKW3TWZ1GqRuCQyXPi5bklO.png)

下方即为设置默认用户，改为你的用户名
然后退出，在 powershell 输入命令重新开启进入
``` powershell
wsl --shutdown
wsl -d Ubuntu-24.04
```

### 详细配置

还有很多其他关于 `wsl.conf`（特定发行版设置，位于每个发行版的 `/etc/wsl.conf`）和 `.wslconfig`（全局设置，位于 Windows `C:\Users\ 你的用户名 \.wslconfig`）的设置，在这里我就不赘述了，具体配置方法参考微软文档 [WSL 中的高级设置配置](https://learn.microsoft.com/zh-cn/windows/wsl/wsl-config)
推荐直接在开始菜单界面的全部应用里找到 `WSL Settings`，在图形化界面里进行全局设置，这样更加方便直观，而且每个设置项下方都有小字介绍

展示一下我的 `.wslconfig` （在 `WSL Settings` 里调整的设置好像不会显示在 `.wslconfig` 文件中）
``` .wslconfig
[wsl2]
memory=4GB # 内存
processors=8 # 处理器数量
defaultVhdSize=30GB # 虚拟硬盘大小

[experimental]
sparseVhd=true # 使发行版虚拟硬盘只占用实际存储的大小，而不是预先分配的最大大小
```
`sparseVhd=true` 我也不太懂，貌似没什么用，警告提示如下：
``` powershell
wsl: 由于潜在的数据损坏，目前已禁用稀疏 VHD 支持。
若要强制分发使用稀疏 vhd，请运行：
wsl.exe --manage  --set-sparse --allow-unsafe
```

### 替换镜像源

默认的源在国内用起来可能卡卡的，这时就需要替换为镜像源了

> 感谢佬友推荐的换源脚本及工具
[quote="Sir. That Way, post:33, topic:1015067, full:true, username:goodchuai"]
换源可以用 https://linuxmirrors.cn/
wsl 下推荐安装 [GitHub - wslutilities/wslu: A collection of utilities for Windows Subsystem for Linux](https://github.com/wslutilities/wslu) 这个可以很方便的进行一些浏览器操作
[/quote]

1. 备份原有源列表（可选）
``` bash
sudo cp /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list.d/ubuntu.sources.bak
```
2. 编辑源列表文件替换为镜像源
``` bash
sudo vim /etc/apt/sources.list.d/ubuntu.sources
```
将文件中的如下部分
```
Types: deb
URIs: http://archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```
替换为
```
Types: deb
URIs: http://cn.archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main universe restricted multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```
这样就好了，可以执行下方命令试试（看谁跟我一样喜欢这大长串命令😋）
``` bash
sudo apt update && sudo apt upgrade -y && sudo apt autoclean && sudo apt clean && sudo apt autoremove
```

> [!note]- 关于网络连接的问题
> 如果下载东西慢（尤其是 github 上的东西），可以尝试开启代理，下面介绍一下开启代理的方法
> 1. 最简单的方法，直接开启 win 上代理应用的虚拟网卡模式（tun模式）
> 2. 稍复杂些的
> 	- 开启代理应用的局域网连接设置，并记住本地 IP 及代理使用的端口
> 	- 进入 WSL 执行如下命令
> 	``` bash
> 	export http_proxy="http://<win的ip>:<代理使用的端口>"
> 	export https_proxy="https://<win的ip>:<代理使用的端口>"
> 	```
> 	- 这是临时的配置，如果想要持久请写进 `~/.bashrc` 或 `~/.zshrc`
> 	- 关闭代理执行如下命令
> 	``` bash
> 	unset http_proxy
> 	unset https_proxy
> 	```
> 	- 持久设置关闭请删除在 `~/.bashrc` 或 `~/.zshrc` 中的命令

# 关于 WSLg

可以在 Windows 系统上运行 WSL 中带图形界面的应用程序，直接在 WSL 中用命令运行带图形界面的应用程序即可，记得确保在 `WSL Settings` 中打开如下设置

![WSLg](https://linux.do/uploads/short-url/avr2DVEu2NB18ikgGSpvTrJuyxi.png)

# Claude Code 和 Codex 配置

说到开发，最近看不少佬都在用 Claude Code 和 Codex（我自己也在用），接下来就来介绍一下怎么配置第三方提供商吧

## 安装方法

### 1. 下载 nodejs

推荐使用 nvm 安装 nodejs（参考官方指导）
``` bash
# 安装 nvm，默认安装位置在～/.nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
# 加载 nvm
\. "$HOME/.nvm/nvm.sh"
# 安装 nodejs 22
nvm install 22
# 验证 nodejs 和 npm 版本
node -v
npm -v
```

### 2. 安装 Claude Code 和 Codex
运行下方命令全局安装
``` bash
# @musistudio/claude-code-router 可选，用来将非 Anthropic 接口接入 claude code
# --registry 参数用来指定镜像源，加速国内下载，-g 参数指的是全局安装而不是项目安装
npm install -g @anthropic-ai/claude-code @openai/codex --registry=https://mirrors.cloud.tencent.com/npm/
# 慢的话也可以用淘宝源：https://registry.npmmirror.com/
```
顺便介绍一点 npm 的常用命令
``` bash
npm cache clean --force # 强制清理缓存
npm outdated -g # 检查全局包是否有新版本
npm update -g <包名> --registry=<镜像源地址> # 更新全局包
npm uninstall -g <包名> # 卸载全局包
```
如果想全局配置 npm 镜像源运行如下命令，以后就不用再挂 `--registry` 参数了
``` bash
# 设置全局镜像源
npm config set registry <镜像源地址>
# 查看目前的镜像源
npm config get registry
```

## Claude Code 配置

先运行一遍 claude 会自动生成 `~/.claude` 文件夹，然后再退出
``` bash
claude
```
进入 `~/.claude` 并创建 `settings.json`
``` bash
cd ~/.claude
touch settings.json
vim settings.json
```
然后编辑 `settings.json` 设置文件，参考如下，详细配置参考 [Claude Docs](https://docs.claude.com/en/docs/claude-code/settings)，这种方法只支持 Anthropic 接口，非 Anthropic 接口请使用 [claude-code-router](https://github.com/musistudio/claude-code-router)
``` json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "你的提供商的 key",
    "ANTHROPIC_BASE_URL": "你的提供商的接口地址"
  },
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```
接下来就可以爽用了😋

## Codex 配置

同样，先运行一遍 codex 自动生成 `~/.codex` 文件夹，然后再退出（退出按两遍 Ctrl+C）
``` bash
codex
```
进入 `~/.codex` 并创建 `config.toml` 和 `auth.json`
``` bash
cd ~/.codex
touch config.toml auth.json
vim config.toml
```
然后编辑 `config.toml` 设置文件，参考如下，详细配置参考 [官方文档](https://github.com/openai/codex/blob/main/docs/config.md)
``` toml
experimental_use_rmcp_client = true
model_provider = "使用的提供商名称"
model = "gpt-5-codex" # 模型自己选
model_reasoning_effort = "high" # 推理强度
disable_response_storage = true # 建议打开

[model_providers. 提供商名称]
name = "随意起的提供商名称"
base_url = "提供商的接口地址"
wire_api = "responses"
requires_openai_auth = true

# mcp 示例
[mcp_servers.sequentialthinking]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-sequential-thinking@latest"]
startup_timeout_sec = 2000 # 可选，默认 10 秒启动超时
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
bearer_token_env_var = "<token>"
startup_timeout_sec = 2000
```

> [!info] MCP 超时问题
> 如遇到类似 `MCP client for sequentialthinking failed to start: request timed out` 的问题，在MCP中设置 `startup_timeout_sec` 参数，尽量调高一般就能避免了，参考 [codex 文档这部分](https://github.com/openai/codex/blob/main/docs/config.md#other-configuration-options)

再编辑 `auth.json` 文件写入 key
``` json
{
  "OPENAI_API_KEY": "提供商 key"
}
```
接下来同样爽用😋

如果想在 WSL 中操作 Win 上的文件可以进入 `/mnt`，里面有 Win 的各个盘符的挂载文件夹，进入对应项目文件夹，然后运行 `claude` 或 `codex` 开始鞭策 AI 吧

## [cc-switch](https://github.com/farion1231/cc-switch)

有佬推荐使用，去看了一下，确实方便，可以快速在各个提供商之间切换，接下来就介绍一下大致使用方法
首先，要去Github仓库下载对应Windows的安装包或便携版压缩包
启动后进行设置，调整各自配置目录，如下图

![cc-switch1](https://linux.do/uploads/short-url/cKTxOXcOQBquHyPzazXJVn82Dnq.png)

找到自己安装 CC 和 Codex 的发行版

![cc-switch2](https://linux.do/uploads/short-url/eD3Aj4s8nJyxsZFuDI2sIflCReT.png)

找到配置文件夹位置，分别选择

![cc-switch3](https://linux.do/uploads/short-url/2jPJfyJZb2cdcQNt6ytF1PuKNIh.png)

最后效果

![cc-switch4](https://linux.do/uploads/short-url/kVwASJKvhKsBP1kUaQr0AtR5eWL.png)

然后就可以自己添加提供商快速替换了，更多信息可以去Github仓库查找

# 在 VS Code 中连接 WSL

可能有人用不惯终端编辑器，接下来简单说一下在 VS Code 中连接 WSL 进行文件编辑开发，要安装如下插件

![VSC-WSL1](https://linux.do/uploads/short-url/amGKdfmVRNDvNSCgpq0BFl8Uolg.png)
![VSC-WSL2](https://linux.do/uploads/short-url/mPPJocYVVsx1SUO4N0ZDEZvC90Y.png)

然后就可以在左侧栏的远程资源管理器中连接 WSL 发行版了

![VSC-WSL3](https://linux.do/uploads/short-url/hJGFXRzXQAQbNqMkzS68J9RnyMY.png)

# 在WSL中使用Docker

> 最好不要同时装 Docker Desktop 和 WSL 内的独立 Docker 引擎，已有佬友有惨痛的代价

## 1. 与 Docker Desktop 集成

先确保在Windows主机中安装了 Docker Desktop，并在设置中开启 `Use the WSL 2 based engine`

![docker1](https://linux.do/uploads/short-url/dDWQLtc2eHfoxAmhtXfCOWJn7Ra.png)

然后在如下位置打开WSL集成，勾选你想要使用docker的发行版，记得应用设置

![docker2](https://linux.do/uploads/short-url/f51lR5NU3xJNja5Fk2U9aQKYVvx.png)

现在你可以直接在WSL中使用docker拉取镜像创建容器了
下面介绍一些常用的docker命令
``` bash
docker images # 列出所有镜像，包括Windows中的镜像，这些全由 Docker Desktop 统一管理
docker container ls # 列出所有容器
docker volume ls # 列出所有卷
docker network ls # 列出所有网络

docker rmi <镜像名/镜像ID> # 删除镜像
docker container rm <容器ID> # 删除容器
docker volume rm <卷名> # 删除卷
docker network rm <网络ID> # 删除网络

docker pull <各种可选项> <容器名:标签> # 拉取镜像
docker ps # 查看运行中的容器
docker logs <容器名/容器ID> # 查看容器日志，可选各种参数，参数问AI

docker system prune # 清理 Docker 中不再使用的资源，慎用
```

## 2. 在 WSL 内安装独立 Docker 引擎

具体安装方法在这里不做介绍了，请参考 [Docker 官方文档](https://docs.docker.com/engine/install/)

# 美化终端界面

嘿，你的终端界面是不是像下面这样单调无趣呢
![WSL5](https://linux.do/uploads/short-url/rTNhxnOcj4XKEbon1XWxPNBXvQJ.png)

想不想要像下面这样美观呢

![WSL6](https://linux.do/uploads/short-url/7eNr1C3v08AP3ekr02m4jAIikeB.png)

![WSL7](https://linux.do/uploads/short-url/9jF1qQBO80aqsIqE6ViZZ3jcSwf.png)

![WSL8](https://linux.do/uploads/short-url/c782xlt32Hj0cvKIPFUrgtG5BMa.png)

接下来就介绍一下终端的美化

## 1. 安装 ZSH
``` bash
sudo apt install zsh
```
然后将其配置为默认shell
``` bash
cat /etc/shells # 列出系统中可用的 shell 列表
chsh -s /bin/zsh # 将 zsh 设置为默认 shell，或使用命令 chsh -s $(which zsh)
```

> [!info] 注意
> 此时设置的只是目前账户的 shell，root或其他账户需要另行设置
> 如果使用 `su` 登录root时发现提示 `su: Authentication failure` 可能是没设置密码的问题，用以下命令设置root密码
> ``` bash
> sudo passwd root
> ```

`exit` 退出重新进入终端，这时就会变为 zsh shell，此时会出现如下图界面

![zsh](https://linux.do/uploads/short-url/ppdmwA4FF5eebJfbEcsipmqOZlm.png)

可以根据说明按 `1` 来个性化配置，也可以直接按 `2` 用推荐配置，或者按 `0` 或 `q` 什么也不设置，下方安装 ohmyzsh 时会自动生成新的 `.zshrc`，以前的 `.zshrc` 将重命名为 `.zshrc.pre-oh-my-zsh`
``` bash
echo $SHELL # 可以查看现在使用的 shell
```

## 2. 安装 [ohmyzsh](https://github.com/ohmyzsh/ohmyzsh)

运行如下命令
``` zsh
sh -c "$(curl -fsSL https://install.ohmyz.sh/)"
# 过程中会从 Github 拉取仓库，慢的话开启代理
```
然后会有个提示，直接按回车就行

> [!info] 注意
> 由于换了 shell，原本在 `~/.bashrc` 中的配置在 zsh 中不会生效，可以自己迁移到 `~/.zshrc`
> 比如安装 nvm 时自动加入 `.bashrc` 中的配置
> ```
> export NVM_DIR="$HOME/.nvm"
> [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
> [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
> ```

## 3. 切换主题

可以自己选择喜欢的主题，ohmyzsh 默认带了一些主题，可以去 [ohmyzsh Themes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes) 中查看
这里我推荐一下我一直在用的主题 [powerlevel10k](https://github.com/romkatv/powerlevel10k) 需要自己安装，下面介绍一下安装方法

### 安装 [Nerd Fonts](https://www.nerdfonts.com/) 字体

到 [Nerd Fonts](https://www.nerdfonts.com/font-downloads) 官网去下载一种自己喜欢的字体（我在用 UbuntuMono Nerd Font 字体），然后直接安装在 Windows 上，解压后选择全部 .ttf 文件，右键点击安装

![nerdfonts](https://linux.do/uploads/short-url/4odTaqMMN7CbyoJWqnaOrgxjLMK.png)

然后切换终端字体，以 Tabby 为例

![tabby1](https://linux.do/uploads/short-url/tTomnKnBHMJ71JQ024rXIDjgZY.jpeg)

一般有三种可选，具体在字符宽度、间距等显示样式细节上有些区别，可以分别试试然后在下方的预览处选出自己最喜欢的

![tabby2](https://linux.do/uploads/short-url/cYlBUpes2CZgl398wA9gYwi0Nql.png)

### 安装 powerlevel10k

运行如下命令
``` zsh
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"
# 可以使用 gitee 上的官方镜像加速下载
git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"
```
然后编辑 `~/.zshrc` 将 `ZSH_THEME` 的值设置为 `powerlevel10k/powerlevel10k`，然后重新进入终端，此时会弹出 powerlevel10k 的初始配置，按照引导设置便可

## 4. 安装插件

ohmyzsh 默认会有很多插件，可以自己启用，参考 [ohmyzsh Plugins](https://github.com/ohmyzsh/ohmyzsh?tab=readme-ov-file#plugins)
下面推荐一些插件

### [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)

对输入的命令进行语法高亮显示，使用如下命令安装
``` zsh
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```
然后在 `~/.zshrc` 中的 `plugins` 项中加入 `zsh-syntax-highlighting`

### [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)

根据用户之前输入过的命令，对当前正在输入的命令进行智能提示，使用如下命令安装
``` zsh
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```
然后在 `~/.zshrc` 中的 `plugins` 项中加入 `zsh-autosuggestions`

### [zsh-completions](https://github.com/zsh-users/zsh-completions)

增强命令补全功能，提供更丰富、智能的命令和参数补全建议，使用如下命令安装（这个插件启用与前面略微不同，参照 [zsh-completions 安装说明](https://github.com/zsh-users/zsh-completions?tab=readme-ov-file#oh-my-zsh)）
``` zsh
git clone https://github.com/zsh-users/zsh-completions.git \
  ${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions
```
然后在 `~/.zshrc` 中的 `source "$ZSH/oh-my-zsh.sh"` 行前加入如下的配置
```
fpath+=${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions/src
autoload -U compinit && compinit
source "$ZSH/oh-my-zsh.sh"
```
刷新 zsh 补全缓存
``` zsh
rm -f ~/.zcompdump # 删除旧缓存
compinit # 重新初始化补全
```

最后我的 `.zshrc` 配置如下

![zshrc](https://linux.do/uploads/short-url/hliAqYdHsVDT1gLdEKTHX7SIFzO.jpeg)

顺便告诉大家一个收集了各种 ZSH 框架、插件、主题和教程的 Github 仓库 [awesome-zsh-plugins](https://github.com/unixorn/awesome-zsh-plugins)

## 5. 关于 fastfetch

fastfetch 是一个用于获取系统信息并以美观的形式显示它的工具，好用又好玩，下面来介绍一下安装配置方法

安装可以参考 [fastfetch installation](https://github.com/fastfetch-cli/fastfetch?tab=readme-ov-file#installation)
在 Ubuntu 上用 apt 安装的要落后好几个版本，想用最新版本要自己去 Github 仓库安装，示例如下
``` zsh
# 自己找到适合自己电脑架构的最新版下载链接替换掉下方命令的链接，链接前面的是文件保存名称
curl -L -o fastfetch-linux-amd64.deb https://github.com/fastfetch-cli/fastfetch/releases/download/2.53.0/fastfetch-linux-amd64.deb
# 用 dpkg 安装
sudo dpkg -i fastfetch-linux-amd64.deb
# 如果想要卸载如下
sudo dpkg -r fastfetch
```
其配置文件位于 `~/.config/fastfetch/config.jsonc`，如果没有文件夹或文件需要自己创建
``` zsh
mkdir -p ~/.config/fastfetch
cd ~/.config/fastfetch
touch config.jsonc
```
然后就要自己编辑配置，可以参考 [fastfetch官方预设](https://github.com/fastfetch-cli/fastfetch/tree/dev/presets/examples) 和 [fastfetch配置Wiki](https://github.com/fastfetch-cli/fastfetch/wiki/Configuration)
最后当然就是 `fastfetch` 了（可以回复留下你的 `fastfetch` 哦，有IP的话注意打码）

当然，WSL 的可玩性不止这些，自己去寻找更多好用的东西来 DIY 自己的发行版吧！