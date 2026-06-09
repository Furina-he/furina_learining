---
title: "成功拿下GG卡，很简单有个安卓手机就行，不要root"
source: "https://linux.do/t/topic/2287768"
author:
  - "[[getduanfa]]"
published:
created: 2026-06-09
description: "原来就是下载giffgaff软件，激活一张eSIM卡，然后把eSIM写入到小白卡里，然后这个小白卡可以在任何用，相当于实体eSIM卡 第一，PPD搜小白卡，这个很重要，建议买可切卡的，可以写入多个eSIM卡，20左右也不会贵 第二，下载写入小白卡的软件EasyEUICC"
tags:
  - "clippings"
---
原来就是下载giffgaff软件，激活一张eSIM卡，然后把eSIM写入到小白卡里，然后这个小白卡可以在任何用，相当于实体eSIM卡

第一，PPD搜小白卡，这个很重要，建议买可切卡的，可以写入多个eSIM卡，20左右也不会贵

第二，下载写入小白卡的软件EasyEUICC

![](https://cdn3.ldstatic.com/original/4X/7/3/d/73d30203652514eb1457c5571fe576006b1da788.svg) [Angry.Im Software Forge](https://gitea.angry.im/PeterCxy/OpenEUICC/releases)

![](https://cdn3.ldstatic.com/optimized/4X/1/f/1/1f122f7551c08c179da9bf7eadf9eaea1a9167cc_2_690x345.png)

### [OpenEUICC](https://gitea.angry.im/PeterCxy/OpenEUICC/releases)

eSIM LPA (Local Profile Assistant) implementation for Android. System privilege or ARA-M allowlisting required.

下载最新版就行

第三，打开EasyEUICC，点击兼容检查，上面显示可以兼容那就是可以

第四，插入小白卡，这个时候你发现EasyEUICC有个+可以写入配置了

第五，打开[这个](https://simonmy.com/posts/giffgaff-esim-mod-apk.html)下载直装版。上面教程写的很清楚，一定要仔细看这个链接的教程

第六，申请完直接写入小白卡就完事了

激活注意这个  

[![image](https://cdn3.ldstatic.com/optimized/4X/9/e/d/9ed9397396f7fb25e61952b65a8e7355e597616e_2_690x304.png)

image1186×523 35.9 KB

](https://cdn3.ldstatic.com/original/4X/9/e/d/9ed9397396f7fb25e61952b65a8e7355e597616e.png "image")

需要付10英镑，国内visa付就行

核心思路：直接对 Giffgaff 官方 APK 进行改造，使其：  
始终认为当前设备支持 eSIM（绕过 App 侧的 eSIM 能力检测）  
在下载 eSIM 配置文件时，将激活码通过系统分享面板弹出，而非尝试写入本机 eSIM 芯片

请注意，老的手机可能不支持读取小白卡，一定要把小白卡插入手机，EasyEUICC显示+图标可以写入配置，在去激活gg的eSIM

还有有佬反应，小白卡可能用一段时间没信号，佬们自己斟酌

然后gg的eSIM补卡只能用一个gg实体卡补