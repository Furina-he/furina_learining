---
来源: https://linux.do/t/topic/2287768
标题: 成功拿下GG卡，很简单有个安卓手机就行，不要root
作者: 二木
分类: 搞七捻三
tags: [linuxdo, 纯水, 教程, giffgaff]
保存时间: 2026-06-09 18:17:51
评论数: 0
---

# 成功拿下GG卡，很简单有个安卓手机就行，不要root

原来就是下载giffgaff软件，激活一张eSIM卡，然后把eSIM写入到小白卡里，然后这个小白卡可以在任何用，相当于实体eSIM卡

第一，PPD搜小白卡，这个很重要，建议买可切卡的，可以写入多个eSIM卡，20左右也不会贵

第二，下载写入小白卡的软件EasyEUICC
https://gitea.angry.im/PeterCxy/OpenEUICC/releases
下载最新版就行

第三，打开EasyEUICC，点击兼容检查，上面显示可以兼容那就是可以

第四，插入小白卡，这个时候你发现EasyEUICC有个+可以写入配置了

第五，打开[这个](https://simonmy.com/posts/giffgaff-esim-mod-apk.html)下载直装版。上面教程写的很清楚，一定要仔细看这个链接的教程

第六，申请完直接写入小白卡就完事了

激活注意这个
![[raw/clippings/images/mFeQaK3WS1baePo4Pmy4VrCPjem.png]]

需要付10英镑，国内visa付就行

核心思路：直接对 Giffgaff 官方 APK 进行改造，使其：
始终认为当前设备支持 eSIM（绕过 App 侧的 eSIM 能力检测）
在下载 eSIM 配置文件时，将激活码通过系统分享面板弹出，而非尝试写入本机 eSIM 芯片

请注意，老的手机可能不支持读取小白卡，一定要把小白卡插入手机，EasyEUICC显示+图标可以写入配置，在去激活gg的eSIM

还有有佬反应，小白卡可能用一段时间没信号，佬们自己斟酌

然后gg的eSIM补卡只能用一个gg实体卡补