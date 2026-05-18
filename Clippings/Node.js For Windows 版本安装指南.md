---
title: "Node.js For Windows 版本安装指南"
source: "https://linux.do/t/topic/845846"
author:
  - "[[lanyan2011790949]]"
published:
created: 2026-05-19
description: "Node.js Windows 版本安装指南 一、安装步骤 下载安装包 访问 Node.js 官网 选择 LTS 版本（长期支持版，推荐稳定使用）或 Current 版本（最新功能版） 下载 .msi 安装程序（32位或64位根据系统选择） 运行安装程序 双击下载的"
tags:
  - "clippings"
---
### Node.js Windows 版本安装指南

#### 一、安装步骤

1. **下载安装包**
- 访问 [Node.js 官网](https://nodejs.org/)
- 选择 **LTS 版本**（长期支持版，推荐稳定使用）或 **Current 版本**（最新功能版）
- 下载 `.msi` 安装程序（32位或64位根据系统选择）
2. **运行安装程序**
- 双击下载的 `.msi` 文件启动安装向导
- 点击 **Next** 同意许可协议
- **关键步骤**：勾选以下选项（默认已勾选）：
	- `Add to PATH`（自动添加环境变量）
		- `Automatically install the necessary tools`（安装编译工具）
- 点击 **Next** 使用默认安装路径（`C:\Program Files\nodejs\`）
- 点击 **Install** 开始安装
3. **验证安装**
- 按 `Win + R` 输入 `cmd` 打开命令提示符
- 执行以下命令：
	```
	node -v   # 检查 Node.js 版本
	npm -v    # 检查 npm 版本
	```
- 显示版本号即安装成功

---

#### 二、环境配置（如未自动添加 PATH）

1. **手动添加环境变量**
- 右键“此电脑” → 属性 → 高级系统设置 → 环境变量
- 在“系统变量”中找到 `Path` → 编辑
- 添加两条路径：
	```
	C:\Program Files\nodejs\
	%USERPROFILE%\AppData\Roaming\npm
	```
- 重启命令提示符使配置生效
2. **配置 npm 全局路径**
	npm config set prefix “D:\\nodejs\_global” # 自定义全局包安装路径  
	npm config set cache “D:\\nodejs\_cache” # 自定义缓存路径
- 将自定义路径（如 `D:\nodejs_global`）添加到系统 `Path` 变量

---

#### 三、常见问题解决

1. **权限问题**
- 安装全局包时出现 `EACCES` 错误：
	```
	npm config set prefix %APPDATA%\npm  # 使用用户目录
	```
- 或以管理员身份运行命令提示符
2. **旧版本残留**
- 完全卸载旧版：
	- 控制面板 → 程序和功能 → 卸载 Node.js
		- 删除残留文件夹：
		```
		C:\Program Files\nodejs\
		%APPDATA%\npm
		%APPDATA%\npm-cache
		```

---

#### 四、进阶配置

1. **安装多版本管理工具（nvm-windows）**
- 下载 [nvm-windows](https://github.com/coreybutler/nvm-windows)
- 安装后使用命令：
	```
	nvm install 18.17.0  # 安装指定版本
	nvm use 18.17.0      # 切换版本
	```
2. **安装开发工具**
	npm install -g yarn # 替代 npm 的包管理器  
	npm install -g nodemon # 自动重启服务

---

好久没发过帖子了等级都掉了，发个帖子水一下社区，看到的佬友求助点点赞谢谢