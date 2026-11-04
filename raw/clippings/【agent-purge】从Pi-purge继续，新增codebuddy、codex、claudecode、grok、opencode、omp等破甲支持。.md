---
title: "【agent-purge】从Pi-purge继续，新增codebuddy、codex、claudecode、grok、opencode、omp等破甲支持。"
source: "https://linux.do/t/topic/3074069"
author:
  - "[[ZICHUANLAN]]"
published:
created: 2026-11-04
description: "本帖使用社区开源推广，符合推广要求。我申明并遵循社区要求的以下内容： 我的帖子已经打上 开源推广 标签： 是 我的开源项目完整开源，无未开源部分： 是 我的开源项目已链接认可 LINUX DO 社区： 是 我帖子内的项目介绍，AI生成、润色内容部分已截图发出： 是 以上选择我承"
tags:
  - "clippings"
---
#### 本帖使用社区开源推广，符合推广要求。我申明并遵循社区要求的以下内容：

- **我的帖子已经打上 [开源推广](https://linux.do/tag/2234-tag/2234) 标签：** 是
- **我的开源项目完整开源，无未开源部分：** 是
- **我的开源项目已链接认可 LINUX DO 社区：** 是
- **我帖子内的项目介绍，AI生成、润色内容部分已截图发出：** 是
- **以上选择我承诺是永久有效的，接受社区和佬友监督：** 是

*以下为项目介绍正文内容，AI生成、润色内容已使用截图方式发出*

---

从 [Pi-Purge插件，从dsh-purge移植，简化版本，一键破甲，会话独立](https://linux.do/t/topic/3045164) 继续拓展

---

仓库 [ZiChuanLan/agent-purge](https://github.com/ZiChuanLan/agent-purge)

![](https://cdn3.ldstatic.com/optimized/4X/0/9/4/094009a7a348236c9065f28ae3ff9124a3f74133_2_690x344.png)

### [GitHub - ZiChuanLan/agent-purge: One persona, many coding agents. Replace or inject...](https://github.com/ZiChuanLan/agent-purge)

One persona, many coding agents. Replace or inject system prompts across codex, claude, opencode, grok, omp, hermes, pi, zcode - with a local web console.

---

#### 11.3更新

## [\[agent-purge\] 一星期 1K star！更新v0.2.14，优化DSH的提示词注入与破甲。优化UI，支持一键拉取提示词，新增workbuddy、kilo等功能。](https://linux.do/t/topic/3114922)

## 新增magpie插件支持，未严谨测试

[![image](https://cdn3.ldstatic.com/optimized/4X/e/6/7/e677d2fd19c59d2790a689571c9b2b82fe67310d_2_690x432.png)

image2762×1731 416 KB

](https://cdn3.ldstatic.com/original/4X/e/6/7/e677d2fd19c59d2790a689571c9b2b82fe67310d.png "image")

[![image](https://cdn3.ldstatic.com/optimized/4X/4/4/b/44b4ca664c288709d68468b7485bab128b49564e_2_690x458.jpeg)

image1729×1149 123 KB

](https://cdn3.ldstatic.com/original/4X/4/4/b/44b4ca664c288709d68468b7485bab128b49564e.jpeg "image")

[![image](https://cdn3.ldstatic.com/optimized/4X/2/0/a/20a2e4cad4ccf99c986aca98513db92c387bdc9c_2_690x434.jpeg)

image1815×1144 75.3 KB

](https://cdn3.ldstatic.com/original/4X/2/0/a/20a2e4cad4ccf99c986aca98513db92c387bdc9c.jpeg "image")

[![image](https://cdn3.ldstatic.com/optimized/4X/e/2/2/e223341c0cbb11c811180adb1e4a19f21fabd747_2_690x435.jpeg)

image1801×1138 167 KB

](https://cdn3.ldstatic.com/original/4X/e/2/2/e223341c0cbb11c811180adb1e4a19f21fabd747.jpeg "image")

[![image](https://cdn3.ldstatic.com/optimized/4X/8/3/7/8370f7c113c8d8f485b59f78227292e9f57c3566_2_690x449.png)

image1756×1144 88.1 KB

](https://cdn3.ldstatic.com/original/4X/8/3/7/8370f7c113c8d8f485b59f78227292e9f57c3566.png "image")

[![image](https://cdn3.ldstatic.com/optimized/4X/d/7/5/d75694c562c59a05f359d327d89d90bd6d2fea2d_2_345x223.png)

image1755×1136 45.9 KB

](https://cdn3.ldstatic.com/original/4X/d/7/5/d75694c562c59a05f359d327d89d90bd6d2fea2d.png "image")

[![image](https://cdn3.ldstatic.com/optimized/4X/5/f/e/5fe356bdc325f89cbb117b4e5fa757c572eab17e_2_690x453.jpeg)

image1784×1173 185 KB

](https://cdn3.ldstatic.com/original/4X/5/f/e/5fe356bdc325f89cbb117b4e5fa757c572eab17e.jpeg "image")

---

## 注：使用前可先问 `你是？` 来确定system是否成功，不成功可以测试strict模式，再看有无云审。同时Pi推荐在会话最初采用热切换，否则会被上下文影响。

#### 裸命令接管意思为：输入`codex`自动带上提示词，但是不支持会话内切换

#### 默认执行器的意思为输入agent-purge的默认启动harness

---

## 此项目（agent-purge）目的为方便替换多个harness的system提示词，不包含违法内容。仅提供粗略思路，希望对你有帮助。

---

或许这里面的才是精髓？人设提示词请点击这里添加。

[GitHub - ZiChuanLan/some-magic · GitHub](https://github.com/ZiChuanLan/some-magic)