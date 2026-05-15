2026 年 1 月，Google 将 Gemini 深度整合进 Chrome

# 核心功能

- 侧边栏常驻 - 边浏览边用 AI，跨标签页比较产品
    
- Auto Browse - 真正的 Agent，自动帮你查酒店、填表单、订行程
    
- Context Groups - 理解你整个研究会话的上下文，不只是当前页面
    
- Google 生态整合 - 直接在页面里操作 YouTube、日历、地图
    
- Personal Intelligence - 记住你的对话历史，越用越懂你
    

# 首先修改google账号的地区和语言

### 1. 把你的 Google 账号地区改成美国

参考 [Google 账号修改国家地区方法（为了反重力升天）](https://linux.do/t/topic/1186531) 这个教程

### 2. 把 Google 账号语言设置成英文

[accounts.google.com](https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Fgeneral-light&dsh=S-30397874%3A1769741268841338&followup=https%3A%2F%2Fmyaccount.google.com%2Fgeneral-light&ifkv=AXbMIuDyFZWH5-lN-G-V_tAHcQ9oW5A8srVC6sDRVsvh6gumZn8d0vSuVVsE4SGDCmIQOXi2S44A&osid=1&passive=1209600&flowName=WebLiteSignIn&flowEntry=ServiceLogin)

### [登录 - Google 账号](https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Fgeneral-light&dsh=S-30397874%3A1769741268841338&followup=https%3A%2F%2Fmyaccount.google.com%2Fgeneral-light&ifkv=AXbMIuDyFZWH5-lN-G-V_tAHcQ9oW5A8srVC6sDRVsvh6gumZn8d0vSuVVsE4SGDCmIQOXi2S44A&osid=1&passive=1209600&flowName=WebLiteSignIn&flowEntry=ServiceLogin)

设置语言为英文，地址为美国地址

[https://linux.do/uploads/default/optimized/4X/2/5/d/25d1c319236701f33c0b3086f88b9df08eb58b38_2_690x374.png](https://linux.do/uploads/default/optimized/4X/2/5/d/25d1c319236701f33c0b3086f88b9df08eb58b38_2_690x374.png)



  

### 3. chrome浏览器的语言也需要改成英文

macos的可以按照如下设置：系统设置->语言与地区->最下面为Chrome自定义语言

[https://linux.do/uploads/default/optimized/4X/4/6/3/46329fd4f8595a53c55f51b5fe789e1096c7c747_2_482x500.jpeg](https://linux.do/uploads/default/optimized/4X/4/6/3/46329fd4f8595a53c55f51b5fe789e1096c7c747_2_482x500.jpeg)


  

windows如何改程序的语言环境可以自己去搜 这里不提供了

### 4.执行脚本

进到 `chrome://settings/help` 检查下 chrome版本 要更新到最新版本，确保更新到最新版本，**关闭chrome浏览器**,

MacOS执行：

```Shell
curl -fsSL https://raw.githubusercontent.com/appsail/Gemini-in-Chrome/main/install.sh | bash
```

Windows 使用poweshell执行

```Shell
irm https://raw.githubusercontent.com/appsail/Gemini-in-Chrome/main/install.ps1 | iex
```

脚本会修改 Chrome 的本地配置文件（Local State），设置三个关键参数：

- is_glic_eligible - 启用 Gemini 功能资格，改成 true
    
- variations_country - 国家设置，改成 us
    
- variations_permanent_consistency_country - 永久一致性国家设置，改成 us
    

然后就打开Chrome可以看到右上角多了一个

[https://linux.do/uploads/default/original/4X/f/9/7/f97302029885474aea366e402ec563e30aab31b3.png](https://linux.do/uploads/default/original/4X/f/9/7/f97302029885474aea366e402ec563e30aab31b3.png)


  

按钮。

对了如果你要使用 auto browser 功能 需要你有订阅 Google AI Pro 套餐。