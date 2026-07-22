---
title: "Typora 离线许可证激活工具（Windows EXE，开箱即用）"
source: "https://linux.do/t/topic/2237895"
author:
  - "[[Aliesz]]"
published:
created: 2026-07-22
description: "Typora 离线许可证激活工具（Windows EXE，开箱即用）【截至 2026-05-24 v1.13.6 有效】 站在前人肩膀上，感谢两位佬友的思路与原始脚本： 原始方案：Typora 安装与激活教程 脚本优化版（解决日志、DevTools、进程残留问题）：关于 Ty"
tags:
  - "clippings"
---
> 站在前人肩膀上，感谢两位佬友的思路与原始脚本：
> 
> - 原始方案：[Typora 安装与激活教程](https://linux.do/t/topic/1518535)
> - 脚本优化版（解决日志、DevTools、进程残留问题）：[关于 Typora 最新激活脚本-优化版](https://linux.do/t/topic/2223997)

---

## 背景

两篇文章的思路已经很完整，但对非技术用户门槛仍然存在：

- 需要手动配置 Node.js 环境并 `npm install`
- Typora 安装路径需要手动修改脚本
- 运行出错时窗口直接消失，看不到任何提示
- 多次操作可能出现重复注入，导致 Typora 无法启动

于是基于 [b1ac3 佬的优化版](https://linux.do/t/topic/2223997)，用 AI 重新设计交互流程，打包成单个 EXE，降低使用门槛。

---

## 技术实现原理（来自上述两篇文章）

Typora 基于 Electron，许可证校验逻辑打包在 `app.asar` 中，工具分三层处理：

1. **绕过完整性校验**：解包 `app.asar` → 复制到 `app.bak/` → 修改 Typora.exe 的 Electron Fuse 配置，允许加载未打包的 `app/` 目录代替 asar 包
2. **Hook 许可证校验**：在 `launch.dist.js` 开头注入 JS，劫持 `crypto.publicDecrypt`，返回构造好的许可证 JSON，绕过 RSA 签名验证
3. **拦截联网续签**：劫持 `electron.protocol.handle("https")`，对 `store.typora.io/api/client/renew` 返回构造好的成功响应
4. **注册表写入**：写入 `SLicense`、`IDate`，使 Typora 启动时读取到有效许可证

相比原始脚本的改进：

- ![:prohibited:](https://cdn.ldstatic.com/images/emoji/twemoji/prohibited.png?v=15 ":prohibited:") **彻底去除日志文件**：原脚本 `fsHook` 无论调试开关状态如何，都会在打开文件的目录下生成 `Typora_Hook_Log.txt`，本工具注入代码中无任何日志逻辑
- ![:prohibited:](https://cdn.ldstatic.com/images/emoji/twemoji/prohibited.png?v=15 ":prohibited:") **去除 DevTools 自动弹出**
- ![:white_check_mark:](https://cdn.ldstatic.com/images/emoji/twemoji/white_check_mark.png?v=15 ":white_check_mark:") **防重复注入**：工具始终从未修改的 `app.bak/` 副本读取源文件进行注入，检测到已有注入标记时会提示先还原再重新注入

---

## 使用步骤

**前置条件：**

- Windows 系统（Win10 / Win11）
- 官方版 Typora（推荐 v1.13.6）
- **以管理员身份运行**（Typora 默认安装在 `C:\Program Files`，需要写入权限）
- **如果之前使用过其他脚本建议把软件卸载干净重装后再重新激活**，否则会因为之前注入过脚本出现问题

### Step 1：获取机器码

打开 Typora → **帮助 → 我的许可证 → 输入序列号 → 离线激活**，复制弹窗中的机器码（Base64 字符串）

### Step 2：运行工具

**右键 `TyporaCrack.exe` → 以管理员身份运行**

```yaml
Typora 许可证工具 v1.0
  ──────────────────────────────
  ✓ 检测到 Typora: C:\Program Files\Typora
  使用此路径？(Y/N，默认Y):

  当前状态: 干净（未激活）

  请选择操作:
    [1] 激活
    [2] 还原原始文件
  选择 (默认1): 1

  [提示] 机器码：Typora → 帮助 → 我的许可证 → 输入序列号 → 离线激活 中复制
  机器码: <粘贴机器码>
    deviceId: xxx  fingerprint: xxx  version: win|1.13.6
  邮箱 (回车默认 licensed@typora.io):

  ✓ 解包 app.asar
  ✓ 备份原始文件
  ✓ 修改 Electron Fuse 配置
  ✓ 写入许可证校验 Hook
  ✓ 写入注册表
  ──────────────────────────────
  ✓ 完成！直接打开 Typora 即可使用。
  提示: 建议关闭【自动检查更新】和【使用国内服务器】选项
```

### Step 3：打开 Typora

直接启动，无需输入任何序列号，已处于已授权状态。

---

## 还原功能

工具会自动备份所有修改（`app.asar.bak`、`Typora.exe.bak`），随时可以选择 `[2] 还原原始文件` 一键恢复，同时清除注册表中写入的字段。

---

## 关于 EXE 与 Node.js

**不需要安装 Node.js。** 使用 [pkg](https://github.com/vercel/pkg) 将 Node.js 运行时与依赖一同打包进 EXE（约 38MB），双击即可运行。

---

## 注意事项

1. **关闭自动更新**：Typora 自动更新会覆盖修改的文件
2. **关闭国内服务器选项**：`偏好设置 → 通用 → 使用国内服务器` 建议关闭，否则可能绕过网络验证失败
3. **换设备或重装后需重新操作**：机器码与设备绑定，重装后会变化

**版本变更记录（Changelog）** ：

- **v1.3**：当注册表实际写入失败时，Typora 查询 SLicense/IDate 仍能获得有效数据
- **v1.2**：记录了对全称 `HKEY_CURRENT_USER` 的切换、自动写入失败时的**手动序列号激活兜底指引**以及高消耗磁盘操作下的加载进度提示。
- **v1.1**：记录了抛弃 `readline-sync` 升级为 Node.js 原生异步 `readline`（彻底解决输入卡死与终端乱码）、抛弃 `winreg` 切换为系统原生 `reg.exe` 写入（解决远程地址解析超时）的过程。
- **v1.0**：记录了项目的初始基本功能

下载地址：

**[https://wwbkr.lanzoul.com/b0syp9v9c](https://wwbkr.lanzoul.com/b0syp9v9c)**  
**密码:81q2**

---

感谢 [horrah 佬](https://linux.do/t/topic/1518535) 和 [b1ac3 佬](https://linux.do/t/topic/2223997) 的原始思路，本工具是在其基础上的工程化封装与体验优化。