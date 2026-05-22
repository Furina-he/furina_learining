---
title: "CF高级防御规则 看看我的网站如何用防御的 - 科技lion官方博客【国内版】"
source: "https://blog.kejilion.pro/cf-waf/"
author:
  - "[[KEJILION]]"
published: 2024-03-26
created: 2026-05-22
description: "网站趋于稳定，又迎来nginx调优，先和大家分享我CF的WAF规则，因为这个是最有效的防御，能抵御大量脚本小子 […]"
tags:
  - "clippings"
---
![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-35-1024x538.webp)

网站趋于稳定，又迎来nginx调优，先和大家分享我CF的WAF规则，因为这个是最有效的防御，能抵御大量脚本小子的恶意攻击流量，已经被我验证数月。

在海外做独立站电商网站首选CF的CDN服务，因为太强大了，没有之一。中小型需求不多直接免费到爽。接入后网站加速防护全全交给CF了。最稳的选择。

开始吧！

## 进入WAF配置页

进入CF的后台，选择你要防御的站点域名。

[https://dash.cloudflare.com/login/](https://dash.cloudflare.com/login/)

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-4-1024x352.webp)

记得在DNS选项，开启小云朵。这就开启CDN了，后续防御规则才会生效。

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-7.webp)

选择安全性WAF

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-5.webp)

四个WAF规则

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-6-1024x447.webp)

大家就三个规则。放行自己，放行SEO爬虫，质询刻意流量。

添加规则

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-9.webp)

选择正则表达式添加规则，复制规则保存即可。

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-15-1024x547.webp)

## 防御规则配置

以下列出三个规则的正则表达式

**第一个放行自己原站IP**

IPV4和IPV6地址改成自己

`(ip.src eq **==192.168.7.17==**) or (ip.src eq ==**2901:c080:1110:4c91:5400:4ff:feb8:130a**==)`

选择跳过按图设置，随后保存规则

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-18-1024x391.webp)

**第二个放行SEO爬虫**

无脑复制即可，无需修改，

`(cf.client.bot) or (http.user_agent contains "duckduckgo") or (http.user_agent contains "facebookexternalhit") or (http.user_agent contains "Feedfetcher-Google") or (http.user_agent contains "LinkedInBot") or (http.user_agent contains "Mediapartners-Google") or (http.user_agent contains "msnbot") or (http.user_agent contains "Slackbot") or (http.user_agent contains "TwitterBot") or (http.user_agent contains "ia_archive") or (http.user_agent contains "yahoo")`

选择跳过，随后保存

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-17-1024x391.webp)

**第三个规则质询恶意流量**

至关重要。但也很简单。地域限制，HTTP版本限制都十分管用。在之前大佬的基础上进化规则。

`(cf.threat_score ge 5 and not cf.client.bot) or (not http.request.version in {"HTTP/2" "HTTP/3"}) or (not ip.geoip.country in {"AU" "CA" "FR" "DE" "HK" "IR" "JP" "KR" "MY" "SG" "TW" "GB" "US" "CN"})`

这些大写字母是国家或地区的简称，在其中的都是放行的国家。如果你只在香港做业务可以只填写HK，其余的全部会进入质询拦截模式，俗称CF的5秒盾。

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-19-1024x524.webp)

**后续观察**

这一波设置基本就ok了。可以放几天试试，观察放行和拦截情况。

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-20-1024x412.webp)

## 频率限制

对了还有频率限制，也很关键。

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-33-1024x563.webp)

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-22-1024x718.webp)

![](https://blog.kejilion.pro/wp-content/uploads/2024/03/image-34-1024x529.webp)

## 最后

好了，这很管用。快去试试吧。结束了。解散！

版权声明：  
作者：KEJILION  
链接： [https://blog.kejilion.pro/cf-waf/](https://blog.kejilion.pro/cf-waf/)  
来源：科技lion官方博客【国内版】  
文章版权归作者所有，未经允许请勿转载。

THE END

[用python编写的LDNMP自动化建站脚本](https://blog.kejilion.pro/ldnmp-py/)

[< <上一篇](https://blog.kejilion.pro/ldnmp-py/)

[今天压力测试的成果 一天打了1T流量](https://blog.kejilion.pro/cc-1t/)