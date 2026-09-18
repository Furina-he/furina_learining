---
title: "自建家宽节点+中转站教程：从0到1搭建家宽节点并部署简易中转站（DMIT+VIRCS）"
source: "https://linux.do/t/topic/2086346"
author:
  - "[[xiaowanzi]]"
published:
created: 2026-09-18
description: "因为自己一直想尝试搭一个家宽节点用来部署CPA，但是感觉VPS的价格太贵了，花自己的钱有点心疼，于是用了点话术给领导申请了下，没想到通过了 :laughing: image705×234 88.8 KB 我用的线路机（DMIT的EB系列）、落地机（VIRCS），应该算是目前中转+"
tags:
  - "clippings"
---
因为自己一直想尝试搭一个家宽节点用来部署CPA，但是感觉VPS的价格太贵了，花自己的钱有点心疼，于是用了点话术给领导申请了下，没想到通过了 :laughing:

[![image](https://cdn3.ldstatic.com/optimized/4X/9/7/8/9789832cc3fe3ebfaccbfcc5acb3a055a2b33f72_2_517x171.png)

image705×234 88.8 KB

](https://cdn3.ldstatic.com/original/4X/9/7/8/9789832cc3fe3ebfaccbfcc5acb3a055a2b33f72.png "image")

  
我用的线路机（DMIT的EB系列）、落地机（VIRCS），应该算是目前中转+家宽的毕业搭配；折腾了一天半跑通了整个流程，以下就是整个部署过程，欢迎各位佬提出宝贵意见~

***感谢：[@STALK   ![bookmark](https://cdn.ldstatic.com/images/emoji/twemoji/bookmark.png?v=15)](https://linux.do/u/stalk)   、[@wabulae](https://linux.do/u/wabulae)、[@deer](https://linux.do/u/deer)、[@abbb](https://linux.do/u/abbb) 等大佬的VPS、CPA等相关文章，从他们的帖子中真的学到了很多知识***

---

# 线路机（DMIT）

## 一、登录VPS

### 1\. 连接VPS

1. 工具推荐FinalShell
2. 新建连接：输入VPS的IP，端口22，使用公钥方式登录，用户名root，选择DMIT提供的私钥

### 2\. 更新系统

```bash
apt update -y && apt upgrade -y && apt install sudo curl -y
```

---

## 二、VPS加固

### 1\. 创建普通用户并授权

```Bash
# 创建用户
useradd -m -s /bin/bash wahaha

# 设置密码
passwd wahaha

# 复制 root 的 ssh 密钥以允许新用户登录
cp -r /root/.ssh /home/wahaha/
chown -R wahaha:wahaha /home/wahaha/.ssh

# 允许 wahaha 用户免密执行 sudo
echo 'wahaha ALL=(ALL) NOPASSWD: ALL' | tee /etc/sudoers.d/wahaha-nopasswd
chmod 0440 /etc/sudoers.d/wahaha-nopasswd
```

新开本地终端

```bash
ssh wahaha@你的服务器IP
sudo whoami # 输出 root，无需输入密码
```

### 2\. 修改SSH端口号并配置 UFW 防火墙

```bash
# 修改 SSH 端口（此处以 8866 为例）
sudo sed -i 's/^#Port 22/Port 8866/' /etc/ssh/sshd_config
sudo sed -i 's/^Port 22/Port 8866/' /etc/ssh/sshd_config

# 验证配置语法是否正确
sudo sshd -t

# 安装并重置 UFW 防火墙
sudo apt update && sudo apt install -y ufw
sudo ufw reset # 输入 y 确认

# 设置默认进出站规则
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 放行新的 SSH 端口
sudo ufw allow 8866/tcp
# 放行 80 与 443 端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 重启 SSH 服务
sudo systemctl restart ssh

# 启用防火墙
sudo ufw enable # 输入 y 确认

# 检查状态（确保只能看到 8866/tcp 被允许）
sudo ufw status
```

**注意**：此时**不要关闭**当前的终端窗口！新开一个本地终端测试连接：

`ssh wahaha@你的服务器IP -p 8866`

验证连接成功后，再继续后续步骤

**如果连接不成功：**

```bash
# 按顺序执行
sudo sshd -t
sudo systemctl restart ssh
sudo ss -tlnp | grep ssh

# 如果还是显示:22，继续执行
sudo systemctl status ssh.socket

# 如果看到active，继续
sudo systemctl disable --now ssh.socket
sudo systemctl restart ssh
sudo ss -tlnp | grep ssh

# 再次尝试连接
ssh wahaha@你的服务器IP -p 8866\`
```

### 3\. 禁用 Root 登录

确认新用户和新端口登录成功后，彻底关闭 Root 远程权限：

```bash
# 修改 SSH 配置，禁止 root 登录
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config

# 禁止密码登录
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# 检查配置语法并重启 SSH 服务
sudo sshd -t
sudo systemctl restart ssh
```

新开终端测试 `ssh root@你的服务器IP -p 8866`，提示：`Permission denied (publickey).`

---

## 三、网络测试

```bash
# 切换到 root 环境
sudo -i
# 运行融合怪脚本
bash <(curl -sL https://run.NodeQuality.com)
```

[![image](https://cdn3.ldstatic.com/optimized/4X/4/0/7/4076a9c4fb0ddf598c72be7621cb25d57c4792b6_2_435x500.png)

image852×978 190 KB

](https://cdn3.ldstatic.com/original/4X/4/0/7/4076a9c4fb0ddf598c72be7621cb25d57c4792b6.png "image")

  

[![image](https://cdn3.ldstatic.com/optimized/4X/c/c/0/cc0c589b28dfe15e3e6f0ed8d5aaaa66e941b430_2_474x500.png)

image939×990 294 KB

](https://cdn3.ldstatic.com/original/4X/c/c/0/cc0c589b28dfe15e3e6f0ed8d5aaaa66e941b430.png "image")

脚本跑完大概10几分钟，可以看到IP质量、网络质量等信息，该说不说大妈的三网优化真的不错

**IP质量检测：**

- [https://ping0.cc/](https://ping0.cc/)：看ASN+原生/广播IP，纯净度纯娱乐
- [https://ippure.com/](https://ippure.com/)：看IP纯净度
- [https://ipdata.co/](https://ipdata.co/)：看滥用标记
- [https://scamalytics.com/](https://scamalytics.com/)：看欺诈得分
- [https://radar.cloudflare.com/](https://radar.cloudflare.com/)：跳盾检测，看机器人与人类流量占比，主要看**Traffic**中的**Bot vs. Human**即可
- [https://chatgpt.com/](https://chatgpt.com/)：是否无人机验证、无需登录即可对话
- [https://claude.ai/login](https://claude.ai/login)：是否跳验证码，注册是否可以跳过接码直接注册
- [https://ip.net.coffee/dns/](https://ip.net.coffee/dns/)：DNS泄漏测试
- [https://ip.net.coffee/claude/](https://ip.net.coffee/claude/)：Claude风险监测

---

## 四、 安装 3x-ui 面板

```bash
# 安装/更新 3x-ui
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

一路回车，安装完成后会输出以下信息，保存下来：

```yaml
Username:    Tgsk3EESA
Password:    FDS9WwCsa
Port:        56545
WebBasePath: 4b54asSDH2asHSad9Rw
Access URL:  https:xxxxxxxxxxxxx:56545/4b54asSDH2asHSad9Rw
```

输入：`x-ui`，回车，会看到

[![image](https://cdn3.ldstatic.com/original/4X/9/c/4/9c47cbd5d52bcc380452ca1906e96b1afa330ee8.png)

image372×549 22.9 KB

](https://cdn3.ldstatic.com/original/4X/9/c/4/9c47cbd5d52bcc380452ca1906e96b1afa330ee8.png "image")

  

[![image](https://cdn3.ldstatic.com/optimized/4X/d/b/e/dbeded62d932687543d248476dec1977a335aa8c_2_399x500.jpeg)

image830×1038 156 KB

](https://cdn3.ldstatic.com/original/4X/d/b/e/dbeded62d932687543d248476dec1977a335aa8c.jpeg "image")

开启BBR加速：输入：`24`，回车，`1`，回车，不需要知道它是干啥的，反正它能让节点的网速变快

使用 `ufw allow 上面的Port/tcp` 放行面板的端口

---

## 五、配置 3x-ui 面板

1. 访问`Access URL`，输入刚才保存的用户名和密码，登录

[![image](https://cdn3.ldstatic.com/optimized/4X/7/0/6/70659f3e5e8dcf1080d4335ac166006475e9379e_2_690x353.png)

image2241×1148 138 KB

](https://cdn3.ldstatic.com/original/4X/7/0/6/70659f3e5e8dcf1080d4335ac166006475e9379e.png "image")

2. 入站列表：添加入站
	- 协议：vless
		- 传输：TCP
		- 安全：Reality
		- Target：[samsung.com:443](http://samsung.com:443/)
		- SNI：[samsung.com](http://samsung.com/),[www.samsung.com](http://www.samsung.com/)
		- Get New Cert
		- 创建

[![image](https://cdn3.ldstatic.com/optimized/4X/5/5/1/551625c081253b09956cc06f9f45ebda1ea77c45_2_690x45.png)

image1650×108 7.92 KB

](https://cdn3.ldstatic.com/original/4X/5/5/1/551625c081253b09956cc06f9f45ebda1ea77c45.png "image")

3. 到这里一个订阅节点就创建完成了

[![image](https://cdn3.ldstatic.com/optimized/4X/d/7/e/d7e2b7b4ebf905e6f3ae0c57071534aac77dbd81_2_690x382.png)

image1062×588 31.1 KB

](https://cdn3.ldstatic.com/original/4X/d/7/e/d7e2b7b4ebf905e6f3ae0c57071534aac77dbd81.png "image")

点击二维码就会得到订阅链接

```perl
vless://4f150654-4fba-44fxxxxxxxx@xxxx.com:43465?type=tcp&encryption=none&security=reality&pbk=XhDS2133rSiqpyNj0GgGjhkjvrTvacE1tuV72jA&fp=chrome&sni=www.samsung.com&sid=47744bxxxxx151&spx=%2F#AI-l7amr6wm
```
4. 使用 `ufw allow 节点的端口` 放行节点的端口
5. 如有需要，可以点击添加客户端，设置流量、到期日期，就可以开车了

---

## 六、Cloudflare添加DNS（没有邮箱可以忽略）

1. 进入Cloudflare，点击域名，DNS-添加记录
2. 填写名称、VPS的IP地址、关闭代理状态
3. 保存，等待5分钟解析生效

[![image](https://cdn3.ldstatic.com/optimized/4X/3/2/7/3271462e3c7c7053198f0ee8ee73832a708f4ae2_2_690x298.png)

image1677×726 36.5 KB

](https://cdn3.ldstatic.com/original/4X/3/2/7/3271462e3c7c7053198f0ee8ee73832a708f4ae2.png "image")

4. 进入命令行，ping 刚设置的名称.域名，有回应，说明解析成功

---

## 七、SSL 证书申请与自动续期（没有邮箱可以忽略）

1. 使用 `acme.sh` 申请证书，并将其安装到 x-ui 指定目录，同时设置证书更新后自动重启面板。
2. x-ui面板本身自带SSL证书申请，但是不知道什么原因我这台VPS无法生成pem，所以手动生成证书

### 1\. 申请证书

> **注意**：申请前请确保域名已解析到服务器 IP，且 80 端口未被占用。

```bash
# 申请 ECC 证书
~/.acme.sh/acme.sh --issue -d 名称.域名 --standalone -k ec-256
```

### 2\. 安装证书到指定目录

```bash
# 创建证书存放目录
mkdir -p /etc/x-ui/ssl

# 安装证书并配置重载命令
~/.acme.sh/acme.sh --install-cert -d 名称.域名 --ecc \
--key-file /etc/x-ui/ssl/privkey.key \
--fullchain-file /etc/x-ui/ssl/fullchain.pem \
--reloadcmd "systemctl restart x-ui"
```

### 3\. 修改面板默认的证书路径

面板设置-证书，修改公钥文件路径：/etc/x-ui/ssl/fullchain.pem，密钥文件路径：/etc/x-ui/ssl/private.key，保存并重启

[![image](https://cdn3.ldstatic.com/optimized/4X/e/f/c/efc01a6c402e7665b3332f3cd890db5efea8c643_2_690x286.png)

image1731×719 29.3 KB

](https://cdn3.ldstatic.com/original/4X/e/f/c/efc01a6c402e7665b3332f3cd890db5efea8c643.png "image")

### 4\. 测试域名登录

将上面的Access URL: https:xxxxxxxxxxxxx:56545/4b54asSDH2asHSad9Rw替换为：https:名称.域名:面板端口/4b54asSDH2asHSad9Rw，访问成功

---

# 落地机（VIRCS）

### 一、配置IP白名单

[![image](https://cdn3.ldstatic.com/optimized/4X/6/5/2/652d6905362274653b4bf13b1960ed0843bdbef0_2_682x500.png)

image1020×747 73.8 KB

](https://cdn3.ldstatic.com/original/4X/6/5/2/652d6905362274653b4bf13b1960ed0843bdbef0.png "image")

将线路机的IP加入到白名单，保证只有线路机IP才能登录

### 二、登录VPS

同线路机

### 三、VPS加固

同线路机

### 四、网络测试

[![image](https://cdn3.ldstatic.com/optimized/4X/8/4/5/845bde6eef18a492a569f65ae2f6787f5a8553f0_2_393x500.jpeg)

image510×648 150 KB

](https://cdn3.ldstatic.com/original/4X/8/4/5/845bde6eef18a492a569f65ae2f6787f5a8553f0.jpeg "image")

  

[![image](https://cdn3.ldstatic.com/original/4X/0/a/b/0ab3affb41abd5a2d4b25452553fa644c19b2ebc.png)

image477×623 12.6 KB

](https://cdn3.ldstatic.com/original/4X/0/a/b/0ab3affb41abd5a2d4b25452553fa644c19b2ebc.png "image")

VIRCS家的家宽IP质量毋庸置疑，贵有贵的道理

---

### 五、sing-box脚本一键生成订阅

```bash
# 切换到 root 用户
sudo -i
# 运行安装脚本
bash <(wget -qO- -o- https://github.com/233boy/sing-box/raw/main/install.sh)
```

得到以下内容：

```bash
使用协议: VLESS-REALITY
-------------- VLESS-REALITY-7599.json -------------
协议 (protocol)         = vless
地址 (address)          = 家宽IP
端口 (port)             = 7599
用户ID (id)             = xxxxxxxxxxxxxx-b5c2-97b1228d1a432
流控 (flow)             = xtls-rprx-vision
传输协议 (network)      = tcp
传输层安全 (TLS)        = reality
SNI (serverName)        = www.paypal.com
指纹 (Fingerprint)      = chrome
公钥 (Public key)       = xxxxxxxxxxxxxxxiVElGhW-b2qsm20UXI

------------- 链接 (URL) -------------
vless://xxxxxxxxxxxxxx-b5c2-97b1228d1a432@家宽IP:7599?encryption=none&security=reality&flow=xtls-rprx-vision&type=tcp&sni=www.paypal.com&pbk=xxxxxxxxxxxxxxxiVElGhW-b2qsm20UXI&fp=chrome#233boy-reality-家宽IP
```

默认生成的是协议是VLESS-REALITY，但是落地机作为出口节点，主要追求速度和稳定性，不承担入口伪装职责，所以改为Shadowsocks，配置更简单、开销更低、速度更快。

```bash
sb
```

出现sing-box的面板  

[![image](https://cdn3.ldstatic.com/original/4X/d/c/d/dcdf2f403665d1d2bae9570ec4cfa38d83a94684.png)

image330×222 9.46 KB

](https://cdn3.ldstatic.com/original/4X/d/c/d/dcdf2f403665d1d2bae9570ec4cfa38d83a94684.png "image")

  
输入`2`回车，`1`回车，`1`回车，`8`回车，回车，输入密码，回车  
这里将得到一个ss链接，保存下来

```perl
-------------- Shadowsocks-7599.json -------------
协议 (protocol)         = shadowsocks
地址 (address)          = xx.xx.xx.xx
端口 (port)             = 7599
密码 (password)         = UXxxxxxxxxxxxxxxVtmrfKJ4=
加密方式 (encryption)   = 2022-blake3-aes-256-gcm
------------- 链接 (URL) -------------
ss://MjAxxxxxxxxxxx206VVhUMUVYQU9xV2tPSxxxxxxxY2wyT0h2RHJWdG1yZktKND0=@xx.xx.xx.xx:7599#233boy-ss-xx.xx.xx.xx
```
```bash
# 放行端口 7599
sudo ufw allow 7599/tcp
```

---

### 六、在线路机的3x-ui面板配置中转

1. Xray设置→出站规则→添加出站→JSON→粘贴落地机的ss链接→添加出站

[![image](https://cdn3.ldstatic.com/optimized/4X/4/c/d/4cd7b4c29a7d312315c9c3f87cb1cefd1fd339b8_2_690x453.png)

image1287×846 45.4 KB

](https://cdn3.ldstatic.com/original/4X/4/c/d/4cd7b4c29a7d312315c9c3f87cb1cefd1fd339b8.png "image")

2. 点击测试按钮

[![image](https://cdn3.ldstatic.com/optimized/4X/4/7/e/47e6a847dec7483d5859118f6add458c96caa737_2_690x191.png)

image1607×447 30.5 KB

](https://cdn3.ldstatic.com/original/4X/4/7/e/47e6a847dec7483d5859118f6add458c96caa737.png "image")

3. 路由规则→添加规则
	- Inbound Tags：选入站节点名称
		- Outbound Tag：选出站节点名称

[![image](https://cdn3.ldstatic.com/original/4X/c/c/a/ccaaf53bbece81696ca2e05739dbb454c9f6383f.png)

image525×627 22.2 KB

](https://cdn3.ldstatic.com/original/4X/c/c/a/ccaaf53bbece81696ca2e05739dbb454c9f6383f.png "image")

4. **保存-重新启动Xray**（别忘了）

---

# 使用节点

工具推荐Clash Verge（[https://github.com/clash-verge-rev/clash-verge-rev/releases/tag/v2.4.7](https://github.com/clash-verge-rev/clash-verge-rev/releases/tag/v2.4.7)）

### 1\. 节点转换

说明：3x-ui生成的vless订阅链接无法直接在clash中使用，所以需要转换工具用于支持clash

1. 推荐猫佬的[https://linuxdo.icmpmiao.cc/](https://linuxdo.icmpmiao.cc/)
2. 将线路机的vless订阅链接转换为clash链接，将转换后的链接导入到订阅中
3. 选择对应的节点，进入[https://ping0.cc/](https://ping0.cc/)测试，发现显示的是家宽节点而不是中转节点

[![image](https://cdn3.ldstatic.com/optimized/4X/b/4/5/b45f9488729aaef2f24cce3599d2be0691e3df78_2_300x500.png)

image417×693 18.7 KB

](https://cdn3.ldstatic.com/original/4X/b/4/5/b45f9488729aaef2f24cce3599d2be0691e3df78.png "image")

### 2\. 已经有机场了，想把家宽节点加入到机场中（可选）

目的：不想把自建节点作为一个独立的订阅，可以通过全局扩展脚本，将自建节点加入到现有机场的节点组中，这样就可以灵活切换机场/自建节点

[![image](https://cdn3.ldstatic.com/optimized/4X/7/6/e/76e4868c8f61c986ddb8e0cdbf5c68aca151e530_2_672x500.png)

image939×698 29.8 KB

](https://cdn3.ldstatic.com/original/4X/7/6/e/76e4868c8f61c986ddb8e0cdbf5c68aca151e530.png "image")

将线路机的vless链接中的信息补充到下面的脚本中，直接把这个模板和你的链接扔给AI，输出一个完整的

```javascript
function main(config) {
  const homeNodeName = "🏠 美国家宽"; // 节点名称
  const targetGroupName = "🤖 Claude"; // 机场订阅组
  
  const homeNode = {
    name: "🏠 美国家宽", // 节点名称
    type: "vless", // 协议名称
    server: "xxxx.com", // 节点域名
    port: 43465, // 节点端口
    uuid: "xxxxxxxxxxa-44f6-xxx-9d53607192eb", // uuid
    network: "tcp",
    tls: true,
    udp: true,
    servername: "www.samsung.com",
    "client-fingerprint": "chrome",
    "reality-opts": {
      "public-key": "XhDSg9ggcxxxxxxxCfvrTvacE1tuV72jA",
      "short-id": "4712312151"
    }
  };
  
  config.proxies = config.proxies || [];
  config["proxy-groups"] = config["proxy-groups"] || [];
  
  config.proxies = config.proxies.filter(p => p.name !== homeNodeName);
  config.proxies.unshift(homeNode);
  
  const group = config["proxy-groups"].find(g => g.name === targetGroupName);
  if (group) {
    group.proxies = group.proxies || [];
    group.proxies = group.proxies.filter(p => p !== homeNodeName);
    group.proxies.unshift(homeNodeName);
  }
  
  return config;
}
```

可以看到在机场订阅组中会出现我们添加的家宽节点，点击测试，出现延迟就代表这个家宽节点可以使用了

[![image](https://cdn3.ldstatic.com/original/4X/e/8/3/e832cb4f8478fa579215eb7ab3742c4480bf03ba.png)

image723×306 18 KB

](https://cdn3.ldstatic.com/original/4X/e/8/3/e832cb4f8478fa579215eb7ab3742c4480bf03ba.png "image")

Claude+ChatGPT 分流规则:

```markdown
# Claude 全量规则
- DOMAIN,claude.com,🤖 AI
- DOMAIN,cdn.usefathom.com,🤖 AI
- DOMAIN-SUFFIX,anthropic.com,🤖 AI
- DOMAIN-SUFFIX,claude.ai,🤖 AI
- DOMAIN,clau.de,🤖 AI
- DOMAIN,claudemcpclient.com,🤖 AI
- DOMAIN,claudemcpcontent.com,🤖 AI
- DOMAIN,claudeusercontent.com,🤖 AI
- DOMAIN,servd-anthropic-website.b-cdn.net,🤖 AI
- DOMAIN,sentry.io,🤖 AI
- DOMAIN,statsigapi.net,🤖 AI
- DOMAIN,cdn.anthropic.com,🤖 AI
- DOMAIN,mcp.anthropic.com,🤖 AI
- DOMAIN,console.anthropic.com,🤖 AI
- DOMAIN,workbench.anthropic.com,🤖 AI
- DOMAIN,anthropic.auth0.com,🤖 AI
- DOMAIN,anthropic-com.ghost.io,🤖 AI
- DOMAIN,anthropic.com.cdn.cloudflare.net,🤖 AI
# OpenAI / ChatGPT / Codex 全量规则
- DOMAIN-SUFFIX,openai.com,🤖 AI
- DOMAIN-SUFFIX,chatgpt.com,🤖 AI
- DOMAIN-SUFFIX,ai.com,🤖 AI
- DOMAIN,chat.openai.com,🤖 AI
- DOMAIN,platform.openai.com,🤖 AI
- DOMAIN,api.openai.com,🤖 AI
- DOMAIN,status.openai.com,🤖 AI
- DOMAIN,help.openai.com,🤖 AI
- DOMAIN,codex.openai.com,🤖 AI
- DOMAIN,chat.openai.com.cdn.cloudflare.net,🤖 AI
- DOMAIN,openai.com.cdn.cloudflare.net,🤖 AI
- DOMAIN,openaiapi-site.azureedge.net,🤖 AI
- DOMAIN,openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net,🤖 AI
- DOMAIN,openaicomproductionae4b.blob.core.windows.net,🤖 AI
- DOMAIN,production-openaicom-storage.azureedge.net,🤖 AI
- DOMAIN,cdn.openai.com,🤖 AI
- DOMAIN,files.openai.com,🤖 AI
- DOMAIN,metrics.openai.com,🤖 AI
```

**PS：可以将风控较高的网站单独做一个策略组，将家宽节点配置到这个策略组中，这样就可以实现访问其他网站走机场节点，访问高风控网站走家宽节点，就像我配置的：所有Claude相关的都走家宽节点**

---

# 安装CPA

**线路机部署Nginx，落地机部署CPA，线路机作为入口，反向代理到落地机**

## 一、落地机

### 1\. 安装docker

1. 卸载系统原有冲突 Docker 相关包
```bash
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-doc podman-docker containerd runc | cut -f1)
```
2. 官方一键脚本安装 Docker
```bash
curl -fsSL https://get.docker.com | sh
```
3. 把当前用户加入 docker 用户组
```bash
sudo usermod -aG docker $USER
```
4. 立即生效不用重启服务器
```bash
newgrp docker
```
6. 安装测试
```bash
docker run hello-world
```

### 2\. 部署CPA

1. 创建config.yaml和生成高强度随机key
```bash
mkdir -p ~/cpa && cd ~/cpa
```
```bash
cat <<EOF > config.yaml
# CPA 配置
host: "0.0.0.1"
port: 8317
auth-dir: "~/.cli-proxy-api"
request-retry: 3
quota-exceeded:
  switch-project: true
  switch-preview-model: true
# 自动生成高强度随机密钥
api-keys:
  - "sk-cpa-$(tr -dc 'a-z0-9' </dev/urandom | head -c 32)"
remote-management:
  allow-remote: true
  # 后台管理密钥
  secret-key: "mgt-cpa-$(tr -dc 'a-z0-9' </dev/urandom | head -c 32)"
  disable-control-panel: false
logging-to-file: true
usage-statistics-enabled: true
logs-max-total-size-mb: 100
EOF

echo "*** --config.yaml-- *** 已生成"
echo "*** --仅显示一次,请记录你的明文密钥-- ***"
grep -E '(sk-cpa-|mgt-cpa-)' config.yaml
```

**将密钥记录下来，将密钥记录下来，将密钥记录下来**

2. 创建 docker-compose.yml
```bash
cat <<'EOF' > docker-compose.yml
services:
  cli-proxy-api:
    image: eceasy/cli-proxy-api:latest
    pull_policy: always
    container_name: cli-proxy-api
    network_mode: host
    volumes:
      - ./config.yaml:/CLIProxyAPI/config.yaml
      - ./auths:/root/.cli-proxy-api
      - ./logs:/CLIProxyAPI/logs
    restart: unless-stopped
EOF
```
3. 启动
```bash
docker compose up -d
```
4. 登录线路机，测试
```bash
curl http://落地机IP:8317
```

成功输出：`{"endpoints":["POST /v1/chat/completions","POST /v1/completions","GET /v1/models"],"message":"CLI Proxy API Server"}`

## 二、线路机

### 1\. 安装Nginx

```bash
sudo apt update
sudo apt install -y nginx
```

### 2\. 确保防火墙放行 80/443 端口

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
sudo ufw status
```

### 3\. 写入 Nginx 配置

```bash
sudo tee /etc/nginx/sites-available/cpa >/dev/null <<'EOF'
server {
    listen 80;
    server_name 你的域名;

    location / {
        proxy_pass http://落地机IP:8317;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
EOF
```

### 4\. 写入 Nginx 配置

```bash
sudo ln -sf /etc/nginx/sites-available/cpa /etc/nginx/sites-enabled/cpa
```

### 5\. 重启 Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 6\. 访问测试

```bash
http://你的域名/management.html
```

### 7\. 加HTTPS

```BASH
sudo apt install -y certbot python3-certbot-nginx # 1.输入你的邮箱用于接收证书到期通知 2.y 3.n
sudo certbot --nginx -d 你的域名
```

打开nginx的配置文件/etc/nginx/sites-available/cpa，会发现配置自动修改成了如下格式：

```swift
server {
    listen 443 ssl;
    server_name 你的域名;

    ssl_certificate /etc/letsencrypt/live/你的域名/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/你的域名/privkey.pem;

    location / {
        proxy_pass http://落地机IP:8317;
        ...
    }
}

server {
    listen 80;
    server_name 你的域名;

    return 301 https://$host$request_uri;
}
```

访问：`https://你的域名/management.html`，成功进入管理登录页

### 8\. 登录CPA

[![image](https://cdn3.ldstatic.com/optimized/4X/0/9/a/09aa97096558bc88bd404edb9b88ae2794376c82_2_547x500.png)

image1251×1143 66 KB

](https://cdn3.ldstatic.com/original/4X/0/9/a/09aa97096558bc88bd404edb9b88ae2794376c82.png "image")

输入部署CPA时生成的mgt-cpa-密钥，登录

[![image](https://cdn3.ldstatic.com/optimized/4X/1/4/3/1432c6dd5939d8c04794998aea632697151ad924_2_690x392.jpeg)

image1989×1131 124 KB

](https://cdn3.ldstatic.com/original/4X/1/4/3/1432c6dd5939d8c04794998aea632697151ad924.jpeg "image")

**到这里，整个过程就结束了，最终获得了一个家宽节点订阅和CPA，后续如有需要，可以再加一个new-api来管理额度，我这里就不再做演示了**

---

## 持续优化

复用443端口，偷自己证书，降低IP送中概率：

![](https://cdn.ldstatic.com/user_avatar/linux.do/xiaowanzi/48/1941669_2.png)

[自建节点（vless+reality），复用443端口+偷自己域名证书教程](https://linux.do/t/topic/2117408) [开发调优, Lv1](https://linux.do/c/develop/develop-lv1/20)

> 前段时间我写了一篇家宽节点搭建教程： 其中有些需要优化的地方，比较重要的就是vless使用高位端口和reality偷大厂证书，本次使用偷自己域名证书的方式降低IP被摁住的概率 主要内容： Vless订阅节点复用443端口 3x-ui入站规则SNI使用自己域名 Nginx本地监听127.0.0.1:8443 做回落伪装页 一、Nginx配置 添加静态页面作为伪装页 vibe一个htm…

## 问题回复

1. **直接用家宽落地不行吗，为什么要再加一个线路机？**  
	答：因为家宽机器几乎都不能直连，所以需要一个能直连且有线路优化的机器中转，所谓的线路机也可以理解为中转机，这样访问线路机就跟访问家宽机是一样的。
2. **这套配置一个月的费用是多少？**  
	答：dmit(12.98$)+vircs(35.99$)，约合人民币343，注意：目前dmit没货了（幸亏买得早）。