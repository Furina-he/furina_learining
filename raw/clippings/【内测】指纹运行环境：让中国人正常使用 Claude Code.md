---
title: "【内测】指纹运行环境：让中国人正常使用 Claude Code"
source: "https://linux.do/t/topic/3137152"
author:
  - "[[sauterne]]"
published:
created: 2026-11-08
description: "参考指纹浏览器的原理和技术栈，基于我自己的需求，我做了一个指纹运行环境。叫 Egress Workbench。它是面向 macOS 的指纹运行环境，以 Claude Code 为主，也内置了 Codex 和共享 Chromium 浏览器。 【它本质上还是一个屏蔽宿主机的信息，同时"
tags:
  - "clippings"
---
参考指纹浏览器的原理和技术栈，基于我自己的需求，我做了一个指纹运行环境。叫 **Egress Workbench**。它是面向 macOS 的**指纹运行环境**，以 Claude Code 为主，也内置了 Codex 和共享 Chromium 浏览器。  
【它本质上还是一个屏蔽宿主机的信息，同时根据节点信息来进行伪装的 Docker】

我自己充了一个 Pro，目前已经使用了半个多月，还没有封号，所以拿出来给大家测试一下，有感兴趣的勇士可以来尝试一下，这次把 0.3.3 放出来开放小范围内测（因为vibe出来的东西不确定有多少bug）。

![](https://cdn.ldstatic.com/user_avatar/linux.do/sauterne/48/691089_2.png)

[【成功存活17天并开放内测】Vibe了一个国内用claudecode的repo，看看多久封号。261022 22:36 开 Claude Pro](https://linux.do/t/topic/3060814/) [开发调优](https://linux.do/c/develop/4)

> 进度： 261107 19:44存活第17天 261103 19:09存活第13天 261029 01:51存活第8天 261027 08:56存活第6天 261024 19:26存活第3天 261023 22:36存活第2天 测试环境： 1.搞了一台全新的 MacBook Air，第一次启动就用的全是美区的配置 2.也选择了美国的节点，不过不是家宽就是普通站内拼车节点 3…

[![connection-zh](https://cdn3.ldstatic.com/optimized/4X/2/8/b/28bd64e37993a168b4542c393c18e81ea679e457_2_590x500.jpeg)

connection-zh1920×1627 194 KB

](https://cdn3.ldstatic.com/original/4X/2/8/b/28bd64e37993a168b4542c393c18e81ea679e457.jpeg "connection-zh")

网络出口、时区、工作空间，在一个界面里集中管理。工具运行在本机 Docker Desktop 的持久化 Linux 环境中，可以读写你在 Mac 上选定的真实项目目录。普通停止或重启后，已安装的软件、本地授权和会话文件都会保留。

完整安装包已经放到 Release，首次使用需要完成节点配置和账号登录。具体用法都写在 GitHub README 里，这里就不展开了。

目前支持 **Apple Silicon Mac、macOS 14 及以上**，需要 Docker Desktop，并自备支持的节点（目前支持了一些常见的，比如说订阅，就是 Clash 那种订阅等）和工具账号。安装包尚未经过 Apple 公证。

仓库 [bbfp/egress-workbench-app](https://github.com/bbfp/egress-workbench-app)

![](https://cdn3.ldstatic.com/optimized/4X/d/0/3/d03a2ea572f45fbefb9b9220ec4c4097a19e7436_2_690x344.png)

### [GitHub - bbfp/egress-workbench-app: Egress Workbench by MOYU — A fingerprint runtime...](https://github.com/bbfp/egress-workbench-app)

Egress Workbench by MOYU — A fingerprint runtime environment for Claude Code, Codex and Chromium on macOS.

(应该不会强行把我这个 repo 给干掉吧？佬友们可以先 fork 一份,或者把 release 先下载一下)  
觉得这个方向有意思，欢迎来试试，也请顺手给个 **Star ![:star:](https://cdn.ldstatic.com/images/emoji/twemoji/star.png?v=16 ":star:")** 。  
遇到 bug 或有什么建议，欢迎提 Issue。

**免责声明**

1. 本项目由我独立开发，与 Anthropic、OpenAI 等服务商无隶属或官方背书关系。**不承诺不封号，也不保证匿名或降低封号风险。** 环境特征仍可能被识别，服务商也可能撤销授权。请遵守相关服务条款；在适用法律允许的范围内，作者不对账号封禁或由此产生的损失负责。
2. **目前属于内测版**，主要经过有限的自用测试，尚未经过大规模用户验证，可能存在各种 bug 和兼容性问题。建议先在非关键项目中试用，并备份重要文件。
3. **自有源码暂未公开，目前仅提供 Release 安装包和文档。** 不代表开源或免费商用，许可范围以仓库 LICENSE 为准。
4. 有部分佬友可能会因为没有完全开源代码，担心它的安全性，可以去监控一下整个软件的数据流向，来保证它不会盗取任何人的任何个人信息。因为它走的都是官方的 API。  
	5.我自己测试的那个账号信息是这样的：  
	5.1. 它是谷歌账号  
	5.2. 已经注册了半年多，但这半年多从来没有使用过，也没有充值过  
	5.3. 我一般都是通过 Codex 去使用，也就是 Codex 调用 Claude Code CLI。在使用过程中，我会尽量让 Codex 跟他说英文  
	5.4 这个软件也在我的旧Mac电脑上使用过，并且登录过，目前也没有封号。  
	而且这个旧电脑之前是封过很多 Claude Code 的。大概是在 4 月份的时候，曾经不同账号买过三次 Max 20，最长是用了一周，但三个号都被封完之后，就没再自己买过了