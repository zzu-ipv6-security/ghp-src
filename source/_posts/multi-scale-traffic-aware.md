---
title: Multi-scale Traffic Aware Cybersecurity Situational Awareness Online Model for Intelligent Power Substation Communication Network
date: 2023-06-07 11:36:37
tags: 态势感知
---

### 文献信息

![image-20230531155417086](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230531155417086.png)

**【作者. 题目[J]. 期刊, 刊登时间, 卷号(期号)： 开始页码-结束页码.】**

Hao W, Yang Q, Li Z, et al. Multi-scale Traffic Aware Cybersecurity Situational Awareness Online Model for Intelligent Power Substation Communication Network[J]. IEEE Internet of Things Journal, 2022.

（中文翻译：智能变电站通信网络的多尺度流量感知网络安全态势感知在线模型）

### 摘要

变电站通信网络（SCN）为先进的监测和控制功能提供实时、高速和可靠的数据传输，这些功能正面临越来越多的网络空间威胁和攻击。高效的威胁感知和网络态势感知对于加强安全和可靠的SCN运行至关重要。本文探讨了多尺度的SCN流量模式特征，包括整体网络流量、包含设备（尤其是物联网设备）的分离网络流量和某些类型协议的分离网络流量。提出的面向流量的在线SCN流量异常检测和网络态势感知模型是针对可能导致网络流量模式变化的网络异常和网络攻击而设计的。我们利用基于分数自回归积分移动平均线（FARIMA）的动态阈值模型来检测异常流量模式，而不需要复杂的计算或深度数据包检查。通过与SCN拓扑结构和协议联盟的统计方法，及时量化了SCN的实时运行状况。网络态势感知模型进一步开展，利用Grubbs测试评估SCN中各种设备受影响最大的协议和安全风险。实验结果是在一个真实的110kV智能变电站的基础上进行的。数值结果证实，在预测整体网络流量和分离网络流量时，在线流量表征的均方误差（MSE）相对较低，复杂度也较低。此外，基于不同规模的SCN流量进行了及时和量化的网络安全风险分析，以检测网络空间威胁并确定高风险的SCN设备和最受影响的协议。

### 关键词

异常检测；网络安全；风险分析；变电站通信网络（SCN）；流量模式分析

### 研究思路

我们利用基于分数自回归积分移动平均数（FARIMA）的动态阈值模型来检测异常流量模式，无需复杂的计算或深度数据包检查。结合SCN拓扑和协议，通过统计方法对SCN实时运行状况进行及时量化。利用Grubbs测试，进一步建立网络态势感知模型，评估SCN中受影响最大的协议和各种设备的安全风险。

### 相关知识

<font color=FFA500 size=4>变电站通信网络(SCN)</font>

智能变电站通信网络采用了IEC61850标准，可以在逻辑上分为变电站层、间隔层和过程层，同时还有明确定义的通信接口。变电站层主要执行数据刷新、收集、监督控制和管理任务；间隔层管理数据控制和电力设备保护；过程层将**二次设备**和**一次设备**与**现场设备**上的数据交换联系起来。

+ 一次设备：一次设备是指发、输、配电的主系统上所使用的设备。如发电机、变压器、断路器、隔离开关、母线、电力电缆和输电线路等。

+ 二次设备：二次设备是指对一次设备的工作进行控制、保护、监察和测量的设备。如测量仪表、继电器、操作开关、按钮、自动控制设备、计算机、信号设备、控制电缆以及提供这些设备能源的一些供电装置(如蓄电池、硅整流器等)。

+ 现场设备：连接到ICS（工业控制系统）现场的设备,现场设备的类型包括远程终端设备（RTU）、可编程逻辑控制器（PLC）、传感器、执行器、人机界面以及相关的通讯设备等。

  ![变电站通信网络结构图](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230519110024092.png)

<font color=FFA500 size=4>SCN流量组成</font>

包括SV（采样测量值：可用于变电站间隔层设备之间的通信）、MMS（制造报文规范：用于装置与后台之间的数据交换）、TCP/IP、GOOSE（用于装置之间的通讯）等。

### 研究方法

首先，通过分析**SCN流量异常为什么可以被认为是网络攻击导致的**和**是否可以对其进行数学描述**

1. 网络异常分析（SCN流量异常为什么可以被认为是网络异常导致的）

假设SCN的流量异常在变电站层被识别

   >1. SCN数据流量代表了各种类型的集成、覆盖和互动信息的组合。随着网络映射层之间转发数据包行为的改变，流量模式会因通信中断而改变。
   >
   >2. SCN数据流量的消息类型是多样化的。任何网络异常都会对流量模式和相关数据包产生不同影响，从而导致SCN流量模式的改变。
   >
   >3. 综上，SCN的流量模式可以反应正常操作行为和状态，因此，SCN数据流量异常可以有效反应一定程度的网络异常。

即SCN数据流量异常可以反应通信中断（1）和网络异常情况（2），且与其他方法相比，检测异常流量模式更容易。

在本文中，作者主要分析了四种攻击：H-DDoS、L-DDoS、网络风暴和网络屏蔽。

![不同情况下SCN数据流量示意图](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230523110934155.png)

2. SCN流量特点（分析是否可以SCN数据流量进行数学描述）

   > 1. 自相似性和LRD：由Hurst参数H决定的部分形状与整体形状相似；
   > 2. 静止性：统计属性不随时间的变化而变化；
   > 3. 多分形：非均匀和时间变化的流量分布；
   > 4. 周期性：SCN流量采集周期和IED数据刷新频率导致的循环流量模式；
   > 5. 动态：根据变电站不同的实时情况而变化，以及即插即用策略的执行；
   > 6. 不规则性：由随机事件驱动的不规则数据流，难以分析和预测。

   因此，可以根据统计模型对SCN流量进行数学描述。

3. SCN流量特性和风险分析

该部分提出了一个基于FARIMA的SCN网络态势感知模型，以及时量化SCN网络安全风险，并精确定位异常情况引起的设备故障。

<font color=F0000>**首先**</font>，使用ADF检验分析了SCN流量的平稳性，且计算了SCN流量的自相关性。最终得出结论SCN数据流量表现出SRD和LRD的自相似性统计特征，然后将FARIMA与ARIMA相对比，LRD将会影响ARIMA算法，而FARIMA算法则可去除LRD，所以作者认为使用FARIMA将有较好的效果。

<font color=F0000>**接着**</font>，根据阈值间隔大小和处理时间之间的权衡，使用**选择算法**选择执行FARIMA的次数k。预测的值应满足以下要求：
$$
\begin{aligned}
&\begin{cases}0.9\min(X_t)<\hat{y}_{ij}<1.1\max(X_t,), j=1,2,...,l\\ \sum_{j=1}^n\left(\hat{y}_{ij}-\bar{y}\right)^2\geq\sum_{j=\operatorname{randm}}^{\operatorname{randm}+n-1}\left(\hat{y}_{ij}-\bar{y}\right)^2\\ \left|\hat{H}-H_{\operatorname{origin}}\right|<0.1H_{\operatorname{origin}}\end{cases}& (1)  \\
&
\end{aligned}
$$
即，预测值$\hat{y}$~ij~大于0.9倍的测量值X~t~的最小值，小于1.1倍的测量值X~t~的最大值（第一个公式），整体的方差大于局部的方差（第二个公式）。

定义动态阈值边界如下，以区分SCN数据流量中异常与正常情况：
$$
\left\{\begin{array}{l}{\mathrm{MaxZ}_{j}=\operatorname*{max}(\hat{y}_{i j}), i=1,2,3,\ldots}\\ {\mathrm{MinZ}_{j}=\operatorname*{min}(\hat{y}_{i j}), i=1,2,3,\ldots}\\ \end{array}\right.\quad(2)
$$

<font color=F0000>**然后**</font>，对SCN网络安全进行定量评估。

使用$\lambda$~t~^Det^ 作为异常参数，用于实时量化正常与检测到的SCN数据流量之间的动态偏差，当D~t~$\in$[MinZ~t~ ,MaxZ~t~ ]时，即D~t~为正常情况时，$\lambda$~t~^Det^ = 0。（纵向对比）
$$
\lambda_t^{\operatorname{Det}}=\begin{cases}\frac{D_t-\operatorname{MaxZ}_t}{\operatorname{MaxZ}_t-\operatorname{MinZ}_t},&D_t>\operatorname{MaxZ}_t\\ \frac{D_t-\operatorname{MinZ}_t}{\operatorname{MaxZ}_t-\operatorname{MinZ}_t},&D_t<\operatorname{MinZ}_t.\end{cases}\quad(4)
$$

使用$\lambda$~t~^Ano^反映正常和异常SCN数据流量之间的偏差（横向对比）。
$$
\lambda_t^{\mathrm{Ano}}=\begin{cases}\frac{A_t-\mathrm{Max}Z_t}{\max(X_t)-\min(X_t)},\quad A_t>\mathrm{Max}Z_t\\ \frac{A_t-\mathrm{Min}Z_t}{\max(X_t)-\min(X_t)},\quad A_t<\mathrm{Min}Z_t\end{cases}\quad(5)
$$
构造偏差矩阵$\lambda$~w*n~并对其进行归一化得到矩阵$\tilde{\lambda}$~w*n~，其可以动态跟踪异常情况，并确定SCN数据流量异常的类型。

![image-20230524215053399](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230524215053399.png)

![image-20230524215104226](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230524215104226.png)



使用矩阵ξ~w*n~表示在时刻t，SCN的瞬时异常概率和连续异常概率，其计算方法如下：
$$
\xi_{w,n}=\sigma\left(\tilde{\lambda}_{w,n}\right)^\kappa/\log_2\left(R\left(\tilde{\lambda}_{w\times n}\right)+2\right)\quad(8)
$$

其中，R($\tilde{\lambda}$~w*n~)是$\tilde{\lambda}$~w*n~的秩，σ用于描述变电站的不同控制结构或网络拓扑结构，通常由SCN尺度(即执行器、ied和监控主机的数量)决定。

**提出**了基于ξ~w*n~驱动的脆弱性评价方法，提出了$\gamma$~t~来及时量化SCN在时间t的可靠性程度。进而生成指标矩阵$\gamma$~1*n~表示W类异常对SCN的影响。其中，每个元素表示SCN在某个时间戳的运行可靠性。SCN流量异常的n步测量序列中最危险的时间点风险满足T~risk~=argmin~t∈n~($\gamma$~1*n~)。
$$
\gamma_t=\prod\limits_{\omega=1}^w\bigl(1-\xi_{\omega,t}\bigr)^{\tilde{\alpha}_\omega^{\text{Ano}}}.\quad(10)
$$
以及**提出**了ν~ω~来量化时间间隔n内的异常现象$\omega$的影响。进而生成指标矩阵v~w*1~，其中，每个元素代表某一类型异常的SCN运行脆弱性，SCN数据流量异常中最严重的异常类型为W~risk~=argmax~ω∈w~(v~w*1~)。
$$
v_{\omega}=1-\prod\limits_{t=1}^n\bigl(1-\xi_{\omega,t}\bigr)^{\tilde{\alpha}_\omega^{\mathrm{An}}}.\quad(11)
$$
**提出**了总脆弱性指数v~tot~：
$$
\nu_{\text{tot}}=\left(1-\frac{1}{n}\sum_{t=1}^n\gamma_t+\frac{1}{W}\sum_{\omega=1}^w\nu_\omega\right)/2.\quad(12)
$$
<font color=F0000>**最后**</font>，提出了一个网络态势感知模型。

当v~tot~满足以下公式时，触发报警，使SCN进入防御准备状态。
$$
\nu_{\text{tot}}\geq\left[\hat{P}_k{}^{\sigma/\log_2\left(R\left(\tilde{\lambda}_{\text{wx}n}\right)+2\right)}\right]^{1/c}c=1,\ldots,5\quad(13)
$$
其中c是警报级别。

当SCN处于防御准备状态时，可从分离的网络流量D~t~^ρ^（即过滤后的网络流量，有一定的协议ρ）中推断出最受影响的协议P~risk~：
$$
P_{\mathrm{risk}}=\arg\max_{\rho=1,2,...}\left|\sum_{t=1}^n D_t^\rho-\frac{1}{2}\left(\mathrm{MaxZ}_t^\rho+\mathrm{MinZ}_t^\rho\right)\right|~~(14)
$$
最后采用Grubbs检验（最大归一化残差检验）对某一装置的动态风险进行量化。

### 研究结果

1. 实验数据准备

SCN数据流量测量是在实际运行的110kv变电站中，使用Wireshark软件从站级以太网交换机(Reason S20系列)的镜像端口采集的。实验采集了1440个聚合数据样本（即在时间0:00到24:00之间收集的SCN流量测量值，1分钟AP）

2. 基于FARIMA模型的SCN整体流量分析

通过与其他建模方法的对比展示出了FARIMA的优点：

计算平均均方误差（MSE，由拟合样本的值和相应的真实样本之间的偏差计算得出，用于测量预测值与真实值匹配程度）对各种建模方法的性能进行评估。

![image-20230525200029496](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230525200029496.png)

上表结果表明，LSTM模型致力于大规模数据样本的建模，而FARIMA模型和ARIMA模型则特别致力于小规模数据样本的建模。

最后定义了一个预测时间度量（FTM）的指标来量化每个预测样本的平均处理时间。定义了一个称为预测精度度量(FAM)的指标，用于评估预测与实际的平均偏差。

结果表明FARIMA的FAM优于其他模型；且在不同的AP范围内，FARIMA模型的FTM显著低于LSTM模型，略高于ARIMA模型，但对于电力系统保护是可接受的。

3. 多属性分离SCN流量分析

将分离网络流量分为两类进行分析：

> (1) 不同协议的SCN流量；
>
> (2) 不同包含设备的SCN流量。



   结果分别如图：

![farima模型在不同协议下的有效性](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230525203252289.png)

实验表明，所提出的FARIMA模型可以对不同协议下的SCN网络流量进行表征，预测结果可以接受。SCN中GOOSE流量的预测效果优于其他两种协议的流量，具有很好的特征。当AP的值没有进行很大程度的调整时，AP和所选的持续时间不会对预测效果产生显著影响。

![farima模型在SCN器件中的有效性](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230525203312346.png)

结果显示了当SCN流量被SCN中不同的包含设备(即SCADA服务器、工作站1和工作站2)分开时，FARIMA模型的有效性。当使用不同的ap时，所包含的不同设备的FTM和FAM值几乎相同。在00:00-12:00，AP时间为30-s时，FTM和FAM值最低。

4. SCN定量风险评估

![image-20230525205204245](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230525205204245.png)

采用本文提出的动态阈值模型对不同情况下(即正常和异常情况下)的SCN整体数据交通流进行表征的数值结果，置信水平为90%。在本工作中，FARIMA模型执行10次，得到上界和下界，即k = 10。SCN数据流量以1min的时间间隔聚合，因此最大告警延迟为1min，对于SCN的安全告警和响应是足够的(使用更小粒度的AP可以减少最大告警延迟)。采用每日SCN数据流量测量作为所提出模型的输入，以实时表征接下来40分钟时间段内的正常流量模式。阈值如图9中绿色所示。例如，对于ID为25的样本数据，正常流量区间为[0.7055,0.9780]。

结果：

![image-20230525210255648](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230525210255648.png)

由上图知，SCN漏洞与SCN参数σ(即网络拓扑截面)和κ(即协议自适应)具有较高的相关性。图10分别为正常序列(图10(a))和异常序列(图10(b))在不同σ和κ值下的脆弱性。红色为满足的报警事件，表明SCN状态需要改善，其余蓝色为正常状态(假设最高报警级别)。当两个参数均为不同值时，异常序列的触发告警数要远远多于正常序列。

![image-20230525211337444](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230525211337444.png)

不同异常比例下的漏洞性能。$\tilde{\alpha}$~1~ ~ $\tilde{\alpha}$~4~表示网络风暴、L-DDoS、H-DDoS和网络屏蔽的影响因子。对于σ和κ的所有测试值，结果表明该模型可以有效地检测出SCN数据流量的异常序列。

5. 网络态势感知模型

- 实验环境

  > 采用AP为1 min，以1440个数据样本作为训练集，得到动态阈值模型的参数。提出的FARIMA模型描述了SCN流量的每日基线，并对下一个分析时段的正常流量模式进行了分析。对于未来1小时内的网络态势感知模型，设置仿真步数n为60步(1 min/步)。110千伏变电站共设56个简易爆炸装置和3台监控主机。

  瞬时SCN可靠度和异常概率如下图所示。

  ![image-20230525213122766](https://cdn.jsdelivr.net/gh/CieLeticia/Image@main/pictures/uploadimage-20230525213122766.png)

最危险的时间点T~risk~=57，表明可靠性指标在第57个时间点最低，且W~risk~=1表明网络风暴可视为最严重的异常。因此，SCN有义务拓宽通信带宽，并确保没有额外的非法物联网资产连接到SCN。总脆弱指数v~tot~=0.27<0.5761^1/c^表明，在分析持续时间的下一个1小时内，SCN运行状态稳定，处于正常状态。
