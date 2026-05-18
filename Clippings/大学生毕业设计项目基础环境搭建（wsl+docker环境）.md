---
title: "大学生毕业设计项目基础环境搭建（wsl+docker环境）"
source: "https://linux.do/t/topic/1630514"
author:
  - "[[furinayyds1]]"
published:
created: 2026-05-18
description: "1. WSL (Windows Subsystem for Linux) 安装 什么是WSL WSL是Windows Subsystem for Linux的缩写，是Windows系统中的一个功能，允许用户在Windows上运行Linux环境，无需虚拟机或双系统启动。 安装前准备"
tags:
  - "clippings"
---
## 1\. WSL (Windows Subsystem for Linux) 安装

### 什么是WSL

WSL是Windows Subsystem for Linux的缩写，是Windows系统中的一个功能，允许用户在Windows上运行Linux环境，无需虚拟机或双系统启动。

### 安装前准备

- 确保使用Windows 10版本2004或更高版本（内部版本19041或更高）
- 或Windows 11（任何版本）

### 安装步骤

1. 点击开始，搜索“启用或关闭Windows功能”  
	[![image](https://cdn3.ldstatic.com/optimized/4X/e/d/7/ed78d60c0915720e84d7850cfcfc53db418f6da4_2_345x124.jpeg)
	image1123×405 45.8 KB
	](https://cdn3.ldstatic.com/original/4X/e/d/7/ed78d60c0915720e84d7850cfcfc53db418f6da4.jpeg "image")
2. 启用“适用于Linux的Windows子系统”以及“虚拟机平台”  
	[![image](https://cdn3.ldstatic.com/optimized/4X/0/d/d/0dd504d39f307cfebcd5af8a4b40fd4a76ec938c_2_273x249.jpeg)
	image627×574 82 KB
	](https://cdn3.ldstatic.com/original/4X/0/d/d/0dd504d39f307cfebcd5af8a4b40fd4a76ec938c.jpeg "image")
3. 保证CPU已开启虚拟化功能  
	[![image](https://cdn3.ldstatic.com/optimized/4X/6/7/f/67f0b78f390adad36fce8ef4eb60c6b560c5866a_2_332x250.jpeg)
	image1123×845 80 KB
	](https://cdn3.ldstatic.com/original/4X/6/7/f/67f0b78f390adad36fce8ef4eb60c6b560c5866a.jpeg "image")
4. 安装wsl，已经为各位找好了链接，使用以下的链接下载安装包双击安装即可

[https://github.com/microsoft/WSL/releases/download/2.5.7/wsl.2.5.7.0.x64.msi](https://github.com/microsoft/WSL/releases/download/2.5.7/wsl.2.5.7.0.x64.msi)

安装完毕后打开终端，将 WSL 默认版本设置为 WSL2

```cpp
wsl --set-default-version 2
```
5. 利用命令安装Ubuntu-22.04，并可以使用 `--location` 指定安装位置
```css
wsl --install Ubuntu-22.04 --location D:\Ubuntu-22.04
```

ps:今天帮朋友装报错，*“–location”该发行版本不支持*，有没有知道的佬友 ![:bili_078:](https://cdn3.ldstatic.com/original/3X/4/b/4bd4ab741137208c6273a6074d68f55c1a54334b.png?v=15 ":bili_078:")

如果上面的方法不行的话，那就只能进行手动迁移了  
输入以下命令导出自己的发行版

```bash
wsl --export <发行版名称> <导出路径>
# 例如
wsl --export Ubuntu-24.04 D:\WSL\Ubuntu-24.04\Ubuntu-24.04.tar
```

然后注销原发行版，同时会删除默认位置的发行版

```css
wsl --unregister <发行版名称>
# 例如
wsl --unregister Ubuntu-24.04
```

将导出的发行版导入到自己选择的位置

```php
wsl --import <自己起的发行版名称> <导入位置> <导出的发行版.tar压缩包所在位置>
# 例如
wsl --import Ubuntu-24.04 D:\WSL\Ubuntu-24.04 D:\WSL\Ubuntu-24.04\Ubuntu-24.04.tar
```

现在就可以删除导出的.tar压缩包了（如果要做备份那可以保留）

6. 安装完毕后会执行下列命令进入系统
```undefined
wsl -d Ubuntu-22.04
```

### 常用WSL命令

- `wsl -l -v` ：查看已安装的Linux发行版及其WSL版本
- `wsl --set-version <发行版名称> 2` ：将指定发行版转换为WSL2
- `wsl --shutdown` ：关闭所有WSL会话
- `wsl --distribution <发行版名称>` ：启动指定的Linux发行版

## 2\. Docker 安装

### 什么是Docker

Docker是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的Linux机器或Windows机器上。

简单来说，Docker可以帮你非常方便的安装软件。比如：

MySQL数据库，Redis缓存，MQ消息队列等等

### docker的安装方式有两种（二选一就行，不要两个都装）

### 1.在 WSL 内安装独立 Docker 引擎

这里给大家推荐脚本安装，如果WSL当前用户不是root用户，需要执行下面的命令

```bash
sudo -i
```

切换到root用户

或者你可以 root 身份执行单条命令：

```bash
sudo <命令>
```

然后再运行下面的脚本，跟着指引就行 ![:rofl:](https://linux.do/images/emoji/twemoji/rofl.png?v=15 ":rofl:")

```bash
wget -qO pi.sh https://cafe.cpolar.cn/wkdaily/zero3/raw/branch/main/zero3/pi.sh && chmod +x pi.sh && ./pi.sh
```

这样安装就完成了  
这里是相关链接

[github.com](https://github.com/wukongdaily/OrangePiShell)

![](https://cdn3.ldstatic.com/optimized/4X/5/e/6/5e6eeec2c8bef0741d5a5fe87598e8f100e31391_2_690x344.png)

### [GitHub - wukongdaily/OrangePiShell: 在Linux上快速部署一些好用的docker项目。起初只是为了香橙派制作。推荐使用1panel面板轻...](https://github.com/wukongdaily/OrangePiShell)

在Linux上快速部署一些好用的docker项目。起初只是为了香橙派制作。推荐使用1panel面板轻松管理docker。

### Docker 在 WSL 中的配置

如果使用 WSL 运行 Docker，需确保当前用户有 Docker 权限：

```bash
sudo usermod -aG docker $USER 
# 重新登录 WSL 使权限生效
```

然后，因为前面的脚本已经配置了镜像源，这里就不配置了

### 2\. 与 Docker Desktop 集成

这里有没有大手子能补充下的，我电脑上没有装 ![:rofl:](https://linux.do/images/emoji/twemoji/rofl.png?v=15 ":rofl:")

### 验证Docker安装

打开PowerShell或命令提示符，执行以下命令：

```undefined
docker -v
```

如果看到了Docker版本信息说明安装成功

下面再给一些Docker常用命令

```go
\`docker ps\` ：查看正在运行的容器
\`docker ps -a\` ：查看所有容器（包括已停止的）
\`docker images\` ：查看本地镜像
\`docker run <镜像名>\` ：运行一个容器
\`docker stop <容器ID>\` ：停止一个容器
\`docker rm <容器ID>\` ：删除一个容器
\`docker rmi <镜像ID>\` ：删除一个镜像
```