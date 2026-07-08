---
title: "AI 时代的思维框架"
source: "https://linux.do/t/topic/2538870"
author:
  - "[[Henry_He]]"
published:
created: 2026-07-09
description: "先说背景，某互联网金融大厂，参与预测模型的训练，现负责 FDE 团队，说背景是不想花很多功夫证明自己技术能力（好像也没有啥技术能力） 分享实操过程中我个人基于经验构建的思维框架，不是正经的学术讨论，各位当小说看就好了，也好完善自己的思考体系来指导实际工程架构的搭建，科研佬手下留情"
tags:
  - "clippings"
---
先说背景，某互联网金融大厂，参与预测模型的训练，现负责 FDE 团队，说背景是不想花很多功夫证明自己技术能力（好像也没有啥技术能力）  
分享实操过程中我个人基于经验构建的思维框架，不是正经的学术讨论，各位当小说看就好了，也好完善自己的思考体系来指导实际工程架构的搭建，科研佬手下留情

---

19 世纪中后期麦克斯韦和玻尔兹曼共同提出玻尔兹曼分布，引入概率统计的方法来解释热力学现象，奠定了统计力学基础。  
1985 年 Hinton 引入统计力学的玻尔兹曼分布来构建神经网络概率，发明了玻尔兹曼机。  
1989 年，John Bridle 正式定义 Softmax 函数并将其应用于深度学习解决概率分布。  
Transformer 架构将 Softmax 作为注意力机制核心。

- **Transformer Softmax**：将一个向量（通常是模型输出的未归一化得分/Logits $z\_i$）映射为一个概率分布：
$$
P(z_i) = \frac{e^{\frac{z_i}{T}}}{\sum_j e^{\frac{z_j}{T}}}
$$

𝑃(𝑧𝑖)\=𝑒𝑧𝑖𝑇∑𝑗𝑒𝑧𝑗𝑇

- 与此同时，**玻尔兹曼分布**：描述热力学平衡态下，微观粒子在某个能量状态 
	$$
	E_i
	$$
	𝐸𝑖 的概率：
$$
P(E_i) = \frac{e^{-\frac{E_i}{k_B T}}}{\sum_j e^{-\frac{E_j}{k_B T}}}
$$

𝑃(𝐸𝑖)\=𝑒−𝐸𝑖𝑘𝐵𝑇∑𝑗𝑒−𝐸𝑗𝑘𝐵𝑇

二者在数学形式上完全等价。

玻尔兹曼分布描述的是系统在特定能量约束下、熵最大的最平稳状态； Transformer 内部采用 Softmax 是为了在不引入主观偏见计算出概率权重。

> 统计力学里温度 T 越高，分子运动越混乱；深度学习里温度 T 越高，采样越随机，反映出 AI 越有创造力

---

以上是为了介绍 Transformer 本身具有统计力学基础，下面是正文

单步采样是瞬时的，在前向传播中最终达到静态玻尔兹曼分布。  
多步生成整个序列不再是平衡马尔可夫链，每一个新生成的 token 都将重构并形成新的状态空间，整个多步过程系统始终处于不可逆的动态演化之中。

非平衡统计力学中，通常用朗之万动力学模型来建模动态演化的空间，用地理概念建模（实际模型维度有数千维）：

构建一个俯视的地形图，做了个案例网站方便理解（叠甲，用地形图是因为用朗之万模型容易被骂，也是方便大家理解，二维的框架是有认知瓶颈的，相信各位佬已经有更成熟的思维框架了，不要纠结我的粗糙模型了）

![gif](https://cdn3.ldstatic.com/original/4X/0/b/d/0bd247de5495641ad5e20b88507053476a24d666.webp)

从山顶释放一个小球，它会顺着山坡滑落并停在深谷，如果小球很重，它会对地表或者轨迹造成形变。当下一个小球滚动时，它的轨迹会受到前一个小球留下的压痕影响。  
单步采样时，小球是以跃迁的方式到达低洼位置，定格并指向一个 token；多步推理则是复杂系统，前面序列的小球会对山脉空间产生影响，使得地表变得起伏，进而塑造下一个小球的运动路线。在实际模型推理过程中，山脉空间由模型自身权重以及上下文的 KV Cache 共同塑造。

多步推理过程下：

1. 第一颗小球落在 `学`，地表因为小球发生形变；
2. 第二颗小球在变形后的山坡上滚落，落在 `AI`，地形再次变化；
3. 第三颗小球落在 `上`
4. ···
5. 小球最终滚进 `<EOS>` ，推理结束，并形成完整的话：

`[    学 ai 上 Linuxdo    ](https://linux.do/)`![:distorted_face:](https://cdn.ldstatic.com/images/emoji/twemoji/distorted_face.png?v=15 ":distorted_face:")

将 3 维地势图抽象为高维空间，实际 KV Cache 即键值缓存，代表当前语义空间的地形状态，基于以上构建的微观模型，可以结合物理规律预测模型黑盒的宏观行为特征：

首先需要明确的是，问答过程的上下文引入的 token ，目标都是为了共同塑造一个特定语义地形，设计能让小球滚到正确答案位置的地形

以下是部分性质：

#### 语义漂移

能塑造目标地形的 token 才是有价值的，每轮推理采样会重复成百上千次，一定会采集到噪声 token 形成沟壑，这些沟壑的影响会随着上下文变长而被显化，偏差的增长是非线性的：

[![image](https://cdn3.ldstatic.com/optimized/4X/3/3/e/33ec55c69466f27792df849083a4af082bf257a9_2_655x500.png)

image1494×1140 118 KB

](https://cdn3.ldstatic.com/original/4X/3/3/e/33ec55c69466f27792df849083a4af082bf257a9.png "image")

#### 注意力稀释

地形塑造初期，明确的指令可以造成明显的地形变化，然而当空间的小球数量增加后，地形的张力会被逐渐拉平和稀释，原本的深沟坡度也会逐渐平缓；无意义的小球（修饰词，标点）也会参与平摊坡度。

[![image](https://cdn3.ldstatic.com/original/4X/3/7/d/37da533741754428687668d2f0fb41938e5a2b12.png)

image450×228 1.77 KB

](https://cdn3.ldstatic.com/original/4X/3/7/d/37da533741754428687668d2f0fb41938e5a2b12.png "image")

在长对话中模型会逐渐淡化提示词设定，因此需要反复强调核心指令，比如 `说中文`：

[![image](https://cdn3.ldstatic.com/optimized/4X/3/c/c/3cc72c4c0f86c260292ae5c8028d1cc82410b425_2_689x369.png)

image1206×646 51.5 KB

](https://cdn3.ldstatic.com/original/4X/3/c/c/3cc72c4c0f86c260292ae5c8028d1cc82410b425.png "image")

#### 语义惯性

当对话持续是某一个风格或主题时，已有小球会在地表某个区域形成更深的峡谷，即更深的历史上下文状态，此时如果下一轮对话切换到另一个场景，小球极易受到上文的地形影响

[![image](https://cdn3.ldstatic.com/optimized/4X/7/8/e/78e6d501464f527b2396fbb705b244f9c801e29e_2_436x500.png)

image1296×1482 155 KB

](https://cdn3.ldstatic.com/original/4X/7/8/e/78e6d501464f527b2396fbb705b244f9c801e29e.png "image")

#### 语义壁垒

复杂的逻辑题或多步骤推理，会在语义地形上形成高山阻隔的场景。如果直接推理会缺乏足够的动力，小球会顺着斜坡溜进能量更低的直觉山谷

> 比如 COT 思维链会把模型推理引导到特定区域，claude code/codex 的先规划后推理也是同样道理  
> （BTW，具体 local search 往哪个方向滚就看模型训练的水平了）

[![image](https://cdn3.ldstatic.com/original/4X/d/1/3/d13c3d8a4c56fabd31336a1ce0dd6e3a1d5b6f5d.png)

image612×380 10.5 KB

](https://cdn3.ldstatic.com/original/4X/d/1/3/d13c3d8a4c56fabd31336a1ce0dd6e3a1d5b6f5d.png "image")

> 思维链（Chain of Thought, COT）通过在陡峭的山坡上修筑起“阶梯平台。后续小球每次只需滚向高一点的平台完成接力，并最终翻越山脊

[![image](https://cdn3.ldstatic.com/optimized/4X/5/2/f/52fe45d4c43cd4ba4dd012f98ade60cc54c428cb_2_690x301.png)

image1566×684 71.5 KB

](https://cdn3.ldstatic.com/original/4X/5/2/f/52fe45d4c43cd4ba4dd012f98ade60cc54c428cb.png "image")

#### 相变

前面提到地形变化不是线性发生，可能在临界点引起整个地形的剧烈走向。比如一些看似毫无意义的废话最终在宏观表达上起到决定作用

[![image](https://cdn3.ldstatic.com/optimized/4X/b/6/7/b673ba0344581ae0bef05dfcc0c456f12ff78719_2_548x500.png)

image1332×1216 111 KB

](https://cdn3.ldstatic.com/original/4X/b/6/7/b673ba0344581ae0bef05dfcc0c456f12ff78719.png "image")

> 短程里多说废话或者思考是很有效的，但长程任务里还需要考虑注意力稀释等问题  
> 短 - 长程对上下文和注意力的把控非常考验使用者能力（如果以后对 ai 人才的测试，这种能力可以反映出水平，而不是单纯代码能力）

性质先写到这里了，接下来说说技巧：

#### 引导采样与回滚

很多时候我们不知道如何描述一个复杂场景，只能使用大量冗余、琐碎的词汇描述  
零散的描述虽然也能达到目标，但是对地表会造成冗余的坑洞，如果对话是长程或者及其精准的问答，这些 token 债会造成影响（抱歉又重复一次前面的性质）  
先用冗余的描述引导模型采样到我们需要的关键词后再回滚对话并借助这些关键词重新对话，在长程才用，短程无所谓，模型能力够用

[![image](https://cdn3.ldstatic.com/optimized/4X/1/5/d/15d50430a652ee626861554b234c3beeb3c5565e_2_606x500.png)

image1566×1292 329 KB

](https://cdn3.ldstatic.com/original/4X/1/5/d/15d50430a652ee626861554b234c3beeb3c5565e.png "image")

#### 隐式语义优于显式语义

这个技巧可以延伸很多，比如：

##### 避免知识冗余

[![image](https://cdn3.ldstatic.com/optimized/4X/f/d/e/fde7f9b527980d2c3581f548d4cda6b911255041_2_690x291.png)

image1260×532 35.2 KB

](https://cdn3.ldstatic.com/original/4X/f/d/e/fde7f9b527980d2c3581f548d4cda6b911255041.png "image")

模型通过海量训练数据，底层参数早就涌现出了丰富的原生地貌，冗余的知识会让模型误认为这是强调

##### 注意力劫持

原本模型原生地形存在一些轨道沟壑，在这些沟壑内加入小球反而让这些沟壑更深，推理影响更大

[![image](https://cdn3.ldstatic.com/optimized/4X/6/7/4/67481d3ec8cbdb957e55d6fcc4161f642d078718_2_552x500.png)

image1260×1140 109 KB

](https://cdn3.ldstatic.com/original/4X/6/7/4/67481d3ec8cbdb957e55d6fcc4161f642d078718.png "image")

##### 案例好于说明

很多时候高质量案例能构建强隐式语义场  
比如 ls -al | grep 的单行代码就已经告诉了模型这是 linux 生态，而不用花更多文字去说明

##### 避免认知降维

运用显式的语义一方面会引导模型的注意力，另一方面也会将模型困于使用者的认知上限而失去了寻优能力

[![image](https://cdn3.ldstatic.com/optimized/4X/b/7/c/b7c241904d747d2eb896397d7e1aa8c038007eaf_2_457x500.png)

image1566×1710 381 KB

](https://cdn3.ldstatic.com/original/4X/b/7/c/b7c241904d747d2eb896397d7e1aa8c038007eaf.png "image")

#### 催化剂

催化剂可以降低反应需要的活化能，模型推理时的特殊 token 也能让模型的翻越特殊的山峰

[![image](https://cdn3.ldstatic.com/original/4X/2/4/d/24dc3a14b98b3e6acfe14e8a40c72d436eadb3f9.png)

image342×266 1.42 KB

](https://cdn3.ldstatic.com/original/4X/2/4/d/24dc3a14b98b3e6acfe14e8a40c72d436eadb3f9.png "image")

比如 `通俗易懂`，`奥卡姆剃刀`，`第一性原理`

[![image](https://cdn3.ldstatic.com/optimized/4X/f/5/e/f5e4de27487cbaa8b412427d5adcfed676687aff_2_690x418.png)

image1440×874 129 KB

](https://cdn3.ldstatic.com/original/4X/f/5/e/f5e4de27487cbaa8b412427d5adcfed676687aff.png "image")

#### 语义退火

复杂的工程问题往往需要创新最优解，需要更高能量跨越高耸的地形到达更远的山谷  
常用的技巧有模型内部的动态温度，这是很多模型的工程优化，而对使用者则可以先发散思维，获得足够能量后再用约束条件收敛到创新解法

[![image](https://cdn3.ldstatic.com/optimized/4X/d/0/5/d0551b9a5b34235ffdc90b139e26e3fc01f277ab_2_458x500.jpeg)

image1602×1748 402 KB

](https://cdn3.ldstatic.com/original/4X/d/0/5/d0551b9a5b34235ffdc90b139e26e3fc01f277ab.jpeg "image")

#### 先推理后结论

单独拎出来是因为很多人喜欢让模型先得到结论，但后续的推理都是基于这个结论锚点做采样塑造地形轨道，或者说都是为了圆这个结论而做的辩护

[![image](https://cdn3.ldstatic.com/optimized/4X/3/6/d/36d4317f640042217f77f8c620a209adf99ac6da_2_690x461.png)

image1530×1026 138 KB

](https://cdn3.ldstatic.com/original/4X/3/6/d/36d4317f640042217f77f8c620a209adf99ac6da.png "image")

#### 入戏与共振采样

特定设定引导模型进入某个场景后，多步推理产生的一连串 token 会表现出高度共振，滚雪球式的形成极深的峡谷，在对话轮数越少时效果越好，噪声越少塑造越牢固

[![image](https://cdn3.ldstatic.com/optimized/4X/0/f/7/0f7e00bda5daa3a1cfff1a8b058cb394b466fc4c_2_386x500.png)

image1440×1862 465 KB

](https://cdn3.ldstatic.com/original/4X/0/f/7/0f7e00bda5daa3a1cfff1a8b058cb394b466fc4c.png "image")

#### 轨道弹弓

这个技巧更多会用于越狱测试（写出来不是教大家越狱！而是提供模型安全能力测试的思路，切勿以身试法），安全性高的模型，敏感词区域有更高的壁垒  
通过构建共识性强的能量轨道并引发共振采样，给小球累积足够强烈的动能后再借助惯性突破安全限制

[![image](https://cdn3.ldstatic.com/optimized/4X/e/9/8/e98ee0f4518f100c5fdcfb4ce0fb385e6db082a7_2_296x499.jpeg)

image1440×2432 510 KB

](https://cdn3.ldstatic.com/original/4X/e/9/8/e98ee0f4518f100c5fdcfb4ce0fb385e6db082a7.jpeg "image")

先写到这吧，写太多了也没人看，有时间再进一步整理，佬手下留情，欢迎讨论

> 建立思维框架的帮助在于，能够预测甚至改进模型架构方向；模型能力测试的方法论（比如只通过模型前端能力这个指标判断好坏）；AI 时代人才的标准（很多 AI infra 公司还是用过往思维的代码能力判断水平，行业应该建立更创新的测试，比如长 - 短线程上下文注意力的管理能力）······