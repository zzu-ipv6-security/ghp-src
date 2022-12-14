---
title: 一种在OpenFlow网络中防御IPv6分片攻击的机制
date: 2023-01-06 21:36:42
tags: 安全防护
---

# 01 背景介绍

## OpenFlow结构：

OpenFlow是一种网络通信协议，应用于SDN架构中控制器和转发器之间的通信。软件定义网络SDN的一个核心思想就是“转发、控制分离”，要实现转、控分离，就需要在控制器与转发器之间建立一个通信接口标准，允许控制器直接访问和控制转发器的转发平面。整个OpenFlow协议架构由控制器（Controller）、OpenFlow交换机（OpenFlow Switch）、以及安全通道（Secure Channel）组成。其中控制器对网络进行集中控制，实现控制层的功能；OpenFlow交换机负责数据层的转发，与控制器之间通过安全通道进行消息交互，实现表项下发、状态上报等功能。OpenFlow交换机是整个OpenFlow网络的核心部件，主要负责数据层的转发。它依赖于流表（FlowTable），流表是OpenFlow交换机进行数据转发的策略表项集合，指示交换机如何处理流量，所有进入交换机的报文都按照流表进行转发，OpenFlow架构如下图1所示。

{% asset_img fig1.png 图1 OpenFlow架构 %}

## OpenFlow的工作流程：

OpenFlow网络的基本工作流是当交换机接收到数据包时，它检查流表以将数据包报头与流条目相匹配。如果数据包报头与某个流条目匹配，交换机将根据流条目的指示采取行动。否则，交换机向控制器发送分组报头。控制器向交换机提供如何通过使用OpenFlow流条目来处理分组。随后，交换机基于控制器指令转发分组，并且保存该指令以转发其他类似分组。

## OpenFlow的流表项：

OpenFlow流表的每个流表项(Flow Entry)都由匹配域（Match Fields）、处理指令（Instructions）等部分组成。流表项中最为重要的部分就是匹配域和指令，当OpenFlow交换机收到一个数据包，将包头解析后与流表中流表项的匹配域进行匹配，匹配成功则执行动作指令(actions)。

## OpenFlow对IPv6的支持：

OpenFlow 1.3增加了字段OXM_OF_IPV6_EXTHDR，它可以匹配标准IPv6扩展报头的存在和IPv6扩展报头中的一些例外情况，该字段如图2所示。

{% asset_img fig2.png 图2 OpenFlow对IPv6的支持 %}

# 02 IPv6绕过检测攻击

首先安全设备需要分析IPv6报头链来确定传入数据包是否符合其配置的策略，其次对于分片数据包，安全设备都只查看第一个分片数据。

利用上述特性，攻击者通过将攻击数据包的IPv6报头链分片成若干个分片，使得第一个分片的数据包不包含上层协议（如TCP和UDP）的必要信息。这样就导致了典型的绕过检测攻击。本文将绕过检测攻击分成了以下两类：已知上层协议的绕过检测攻击和隐藏上层协议的绕过检测攻击。
 第一类已知上层协议的绕过检测攻击的原理是第一个分片的最后一个报头的下一个报头(nh)字段点明了上层协议的类型，如下图3所示的分片数据包，第一个分片的最后一个报头是目标选项报头(DOH),它的NH=6，也就是说本数据包的上层协议是TCP协议。

{% asset_img fig3.png 图3 已知上层协议的绕过检测攻击 %}

第二类隐藏上层协议的绕过检测攻击的原理是根据第一个分片的最后一个报头无法得知上层协议的类型，下图4所示的分片数据包的第一个分片的最后一个报头的nh字段是60，也就是目标选项报头，这并非上层协议类型。

{% asset_img fig4.png 图4 隐藏上层协议的绕过检测攻击 %}

# 03 防御机制

针对以上两种类型，作者在OXM_OF_IPV6_EXTHDR匹配域增加了两个新的匹配域字段：OFPIEH_UNDLH和OFPIEH_UNDLNH，这两个字段分别对应于以上两种类型的绕过检测攻击，增加新字段后的OXM_OF_IPV6_EXTHDR匹配域如图5所示：

{% asset_img fig5.png 图5 增加新字段后的OXM_OF_IPV6_EXTHDR匹配域 %}

作者提出的防御机制就是建立在以上两个新字段之上的，比如，OpenFlow网络解析数据包之后，得到OXM_OF_IPV6_EXTHDR的字段值为1000000000，那说明该数据包是第一类饶过检测攻击数据包，接下来就是在流表项中指定针对该类数据包的动作(actions)是丢弃(drop)该类数据包即可。

保护机制的实现流程如图6所示，当一个数据包到达OpenFlow交换机后，首先判断该分片是否是第一个分片，其次判断是否是不包含上层报头的分片，如果是则说明该类数据包是异常数据包，紧接着判断第一个分片的最后一个报头的nh字段，对该类型的数据包进行分类，是前面提到的第一类攻击还是第二类攻击，最后对OXM_OF_IPV6_EXTHDR的字段进行赋值。

{% asset_img fig6.png 图6 保护机制的实现流程 %}

# 04 实验验证

测试环境是基于Mininet创建如图7的拓扑图，其中主机A向主机B发送Ping请求报文，OpenFlow交换机的流表规定收到该数据包后丢弃该类数据包，那么如果B响应了Ping请求，则说明主机A发送的报文成功的绕过了OpenFlow交换机的检测，如果B未作任何响应，则说明OpenFlow交换机丢弃了该数据包且防御机制生效。

{% asset_img fig7.png 图7 测试环境拓扑图 %}

针对本实验，作者设置了如图8所示的三条流表项：

{% asset_img fig8.png 图8 流表项 %}

其中，F1表示它用于丢弃所有ICMPv6 echo请求数据包；F2标志OFPIEH_UNDLH用于过滤攻击类型1的ICMPv6 echo请求分片数据包；F3标志OFPIEH_UNDLNH用于过滤攻击类型2的分片数据包。

本文提出了如图9所示的六种实验场景：

{% asset_img fig9.png 图9 六种实验场景 %}

接下来逐项分析：
 场景1：未分片的ICMPv6 echo请求数据包，流表项F1。B无响应说明F1流表项起作用。
 场景2：类型1的分片的ICMPv6 echo请求数据包，流表项F1。B有响应说明主机A的数据包绕过了交换机检测，成功造成攻击。
 场景3：类型1的分片的ICMPv6 echo请求数据包，流表项F1，F2。B无响应说明增加了流表项F2之后，成功防御了类型1的绕过检测攻击。
 场景4：类型2的分片的ICMPv6 echo请求数据包，流表项F1，F2。B有响应说明流表项F1和F2无法防御类型2的绕过检测攻击。
 场景5：类型2的分片的ICMPv6 echo请求数据包，流表项F1，F2，F3。B无响应说明流表项F1和F2，F3成功防御了类型2的绕过检测攻击。
 场景6：类型1的TCP分片请求包，流表项F1，F2，F3。B有响应说明仅靠F1，F2和F3无法防止TCP分片请求包，因为设置的流表项F1，F2和F3都是针对ICMPv6类型的数据包。

以上实验全面地验证了本文提出的防御机制可以有效防御针对IPv6分片的绕过检测攻击。

# 05 结论

研究表明，目前还没有专门的技术来防止IPv6分片数据包入侵OpenFlow网络，而攻击者可以利用IPv6分片技术规避OpenFlow防火墙检测。滥用IPv6分片也可以与各种攻击结合使用，例如SYN和UDP洪水攻击，以规避OpenFlow转发策略。在典型网络中，网络设备拥有专门的固件处理基于RA和基于DHCPv6服务器的攻击。然而，在OpenFlow网络中，针对这些攻击的保护留给了OpenFlow控制器，这可以通过滥用IPv6分片来逃避。本文所提出的机制为防止此类攻击提供了一种实用且强大的方法。在未来，可以考虑将这个机制延伸至非OpenFlow网络以及其他类型的攻击，如原子分片攻击，重叠分片攻击等。
