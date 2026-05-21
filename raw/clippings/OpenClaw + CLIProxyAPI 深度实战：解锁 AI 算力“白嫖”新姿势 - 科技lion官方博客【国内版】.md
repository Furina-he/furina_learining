---
title: "OpenClaw + CLIProxyAPI 深度实战：解锁 AI 算力“白嫖”新姿势 - 科技lion官方博客【国内版】"
source: "https://blog.kejilion.pro/openclaw-cliproxyapi/"
author:
  - "[[KEJILION]]"
published: 2026-02-10
created: 2026-05-21
description: "前言：别再守着那点免费额度扣扣搜搜了！CLIProxyAPI 才是白嫖的“终极答案” 玩了这么久 AI，我才发 […]"
tags:
  - "clippings"
---
![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-41-22.webp)

## 前言：别再守着那点免费额度扣扣搜搜了！CLIProxyAPI 才是白嫖的“终极答案”

玩了这么久 AI，我才发现自己错过了多少好东西！最近研究的 **CLIProxyAPI** 彻底打开了我的新世界大门。

以前我们要用 Antigravity（反重力） Gemini、Kimi 或者 ChatGPT，得在各种网页和 App 之间反复横跳，额度用完就歇菜。但有了 CLIProxyAPI 这个“神级网关”，情况完全变了：它就像一个万能转换插头，能把所有非标接口一键转换成 OpenAI 规范。最爽的是，你可以把手头所有的账号全部接进去，实现 **全模型自动轮询** 。额度叠满、负载均衡，只要你敢想，全网的免费算力都能成为你的私有资源池。今天，我就带大家把这套“白嫖终极形态”彻底讲透！

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-16-21-1024x436.webp)

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-17-22-1024x528.webp)

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-18-36-1024x486.webp)

## 这就教你“暴力收编”全网算力：一键脚本，开启你的 API 零成本时代！

部署方式，先装CLIProxyAPI 一键搞定。我已经帮大家做成一键脚本了，安装设置登录密钥，自动docker部署。

```
bash <(curl -sL kejilion.sh) app CLIProxyAPI
```

```
bash <(curl -sL kejilion.sh) app CLIProxyAPI
```

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-30-52.webp)

访问默认IP+端口是无法到达控制面板的必须带/management.html，作者可能是为了与API接口避开才这么设计的，但我觉得可以加个分流机制，体验会更好。

访问地址带上management.html，即可进入管理面板，输入你的登录密钥，就可以开始管理了，

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-44-45-1024x485.webp)

记得使用脚本中的添加域名，强烈建议用域名的方式访问API网关，Nginx带缓存优化你的API更快更专业，带HTTPS安全证书加密的。

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-46-59.webp)

CLIProxyAPI 管理面板中，添加Antigravity（反重力） Gemini、Kimi，Qwen 或者 ChatGPT的认证文件，用OAuth登录添加。

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-49-03-1024x500.webp)

点击Antigravity（反重力） 的登录按钮生成认证URL，到官方去登录你的账号。

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-54-37-1024x354.webp)

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-53-03-1024x515.webp)

会返回一个URL，直接复制回来即可，认证完成。

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_21-59-50.webp)

在中心信息里就能看到你加入的反重力的大模型了。多个账户，多搞几个，用都用不完。

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_22-03-20-1024x668.webp)

获取下API密钥，这个不是登录密钥而是对接OpenClaw要用的API key，类似硅基流动，DeepSeek，这种API key。在配置面板选项里找，API key，默认会给我们3个，我们可以生成新的KEY。

可以用科技lion脚本，系统工具，用户信息生成器，随机生成乱码，复制过来。也可以随便填自己的，类似于你的密码。

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_22-12-00-1024x388.webp)

## 终极合体！OpenClaw 一键对接：模型全量导入，瞬间解锁“满血版”私有算力池

接下来将OpenClaw的安装与对接CLIProxyAPI，非常简单，依然是一键脚本，还是熟悉的配方。我优化了这个脚本他可以把你的CLIProxyAPI中的所有模型一次性导入，方便你快速切换模型，可谓是更进一步。

```
bash <(curl -sL kejilion.sh) app OpenClaw
```

```
bash <(curl -sL kejilion.sh) app OpenClaw
```

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_22-28-36.webp)

然后选择换模型，查看可用模型。你的模型全加载进来了。随便玩了。

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_22-31-52.webp)

后续你可以让AI自己写容灾模式，付费的API短时间用尽了，降级到其他模型，如果付费高端模型恢复了再回到高级模型。就是这么玩的，永远不会死。我现在让AI帮我改网页，播报新闻，体验非常舒服。

![](https://blog.kejilion.pro/wp-content/uploads/2026/02/Snipaste_2026-02-10_22-36-48.webp)

## 结语：构建你的“算力永动机”，彻底终结 AI 焦虑

当你完成 **OpenClaw** 与 **CLIProxyAPI** 的合体部署后，你其实已经跳出了“伸手党”的初级阶段，进阶成了真正的\*\* AI 算力架构师\*\*。

这套方案最迷人的地方不在于节省了多少订阅费，而在于它赋予了你极致的\*\*“稳定性”与“自由度”\*\*：

- **算力降级容灾：** 你可以利用 AI 编写简单的监控逻辑，实现自动化的“容灾切换”。当昂贵的付费 API 达到速率限制时，系统自动无缝降级到 CLIProxyAPI 挂载的免费 Gemini 或 Kimi；一旦高端模型额度恢复，立刻切回。
- **全场景丝滑应用：** 无论是让 AI 帮你写网页代码、自动播报新闻，还是挂载到你的个人助理中，你都不再需要担心“额度不足”或“接口断连”。
- **真正属于你的基础设施：** 所有的账号、密钥和调度逻辑都掌握在你自己的服务器上。

这才是“白嫖”的最高境界—— **用技术手段将零散的免费资源，聚合成商业级的稳定服务。** 从此以后，你不再是算力的消费者，而是算力的主宰者。赶紧拿起脚本，去搭建属于你的“算力永动机”吧！

版权声明：  
作者：KEJILION  
链接： [https://blog.kejilion.pro/openclaw-cliproxyapi/](https://blog.kejilion.pro/openclaw-cliproxyapi/)  
来源：科技lion官方博客【国内版】  
文章版权归作者所有，未经允许请勿转载。

THE END

[一年298元！华纳云香港200M独享VPS深度体验报告](https://blog.kejilion.pro/hncloud-hk-2026/)

[< <上一篇](https://blog.kejilion.pro/hncloud-hk-2026/)

[【硬核实战】OpenClaw 助手进化：一句话打造沉浸式盗墓小说广播剧](https://blog.kejilion.pro/openclaw-ai-radio-drama-tutorial/)