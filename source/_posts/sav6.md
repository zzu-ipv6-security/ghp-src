---
title: SAV6 A Novel Inter-AS Source Address Validation Protocol for IPv6 Internet
date: 2022-12-21 18:06:32
tags: 地址溯源
---

利用IPv6地址长特性，设计一种包含自治系统编号（Autonomous System Bumber，ASN）的AGA地址（ASN Generated Addresses），通过检查AGA地址中包括的ASN是否与前缀对应的ASN1一致，来验证自治系统间IPv6地址的真实性。

# 研究背景：

Internet最初的设计假设所有主机都是可信的。然而，随着互联网的发展，这一假设不再成立。在当今的互联网环境中，会遇到多种安全问题，包括源地址欺骗和分布式拒绝服务（DDoS）攻击，这些攻击会造成巨大的破坏和损失。源地址欺骗是攻击者用来发动DDoS攻击的主要工具之一，NEUSTAR报告显示，超过80%的DDoS攻击基于反射洪泛和IP地址欺骗。

为了防止源地址欺骗，IETF提出了ingress filtering，并在RFC 3704中列举了ingress filtering技术在多宿主网络中实现的挑战。源地址验证架构（SAVA）是一种更全面的解决源地址欺骗问题的方案，从接入网络、自治系统内和自治系统间进行地址检验。目前，AS间的源验证方法有两种：基于路由和基于标签。前者利用路由信息建立过滤规则来验证源地址。然而，由于自治系统间非对称路由或部分部署使得该方法不能有效地工作。后者引入了与流量源相关的标签。然而，这种类型的现有方法需要在分组中插入额外的标签，这对于有限带宽的网络来说代价较大。对于数据包非常小的网络，这个问题会进一步恶化。

{% asset_img fig1.png 图1 %}

1. 秘钥交换：协调器与其他自治系统协商对称秘钥，然后分配给边界路由器，**秘钥用于加密或验证源地址**。具体的交换过程是：首先获得其他自治系统的公钥，然后使用Diffie-Hellman密钥交换协商对称密钥，保存**<ASNAj , KAiAj>**，秘钥周期性地更改，比如一周。

2. AGA地址分配：自治系统内的AGA分配器为主机节点分配AGA地址，AGA地址用于验证自治系统间源地址验证。AGA地址生成方法是：**IID=ASNs | nonce | time**  ，其中ASNs是源自治系统的编号，nonce是随机值，time是生成地址的时间，操作是级联拼接。 AGA分配器可以是集成了这种地址算法的DHCPv6服务器。

3. 源IID加密：边界路由器接收到出去的流量，使用协商的对称秘钥加密源地址的IID。加密过程是：**根据目的地址的前缀找到ASN，然后找到对应的秘钥KAsAd加密**。加密对象是**源地址的IID、目的地址的后4字节、载荷的前32字节，共计16字节**。

4. 源地址验证：使用协商的对称秘钥解密，并验证其中包含ASN是否与前缀对应的ASN1一致。解密过程是：**根据源地址的前缀找到ASN，然后找到对应的秘钥KAsAd解密**。解密对象是**源地址的IID、目的地址的后4字节、载荷的前32字节**。解密提取IID的ASN，并根据源地址前缀查找到ASN1，比较ASN1与ASN。若两者相同，则将解密后的数据放在数据包中，并进行转发。若两者不同，则认为是源地址是伪造的，丢弃数据包。

{% asset_img fig2.png 图2 %}

此图给出了SAV6的工作流程 ， 源和目的自治系统都升级了SAV6，其运行流程如下：

1. 源和目的自治系统协商使用AES -128在电码本（ Electronic Codebook ，ECB）模式下进行加密，其共享的对称密钥是0 x57c3dd4fea472ddc1047419f2d041047。
2. 源自治系统的HostA与目的自治系统的HostB通信，其中HostA的IPv6地址为1::1:0:7b: 62 bd: 4140,源ASN(123)嵌入在IID的前32位。HostB的IPv6地址为2::2:0:1c8:6294:62c0，其IID前32比特也嵌入了目的ASN (456)。
3. 当边界路由器收到一个来自HostA的外向数据包时，它首先找到与目的自治系统共享的秘钥k。然后,它使用k加密源IID (0:7b: 62 bd: 4140),目的地址的的最后32位 (6294:62c0)，有效载荷的前32位(0 x6ae31fe8)。加密的结果(bcf3d412f42993c2f3131555330aa8e3)用于替换上面的三个部分，即:源IID(bcf3d412f42993c2 )，目的地址IID的后32位(f3131555)、有效载荷的前32位(330aa8e3)。
4. 同样的,当目的自治系统的边界路由器接收到来自源自治系统123的传入数据包,使用对应的秘钥解密三个部分。如果验证通过,即源地址的ASN等于123，则转发数据包;否则,丢弃数据包。

# 实验验证

## 1.地址分配延迟

由于提出一种AGA地址，对DHCP的过程进行了修改，因此需要测试地址分配的延迟是否会受到影响。

{% asset_img fig3.png 图3 %}

测试结果显示，性能几乎未受到影响，这种新型地址的生成给DHCPv6服务器带来的开销很小。

## 2.吞吐率

{%asset_img fig4.png 图4 %}

边界路由器要对数据包进行加密和解密，这可能造成吞吐率的降低，为此，需要测试边界路由器的吞吐量。

测试结果显示，SAV6与对照组的吞吐率相比，并未严重降低。因为边界路由器只需1次加密或解密，还有2次查找操作。用时间衡量加解密的开销的话，每个数据包加密所需时间约167ns，验证时间约166ns。

## 3.有效吞吐量

{%asset_img fig5.png 图5 %}

由于其他基于标签的域间源地址验证方法引入了标签，造成了每个数据包中的有效数据含量降低。

测试结果显示，SPM选项头包括8位选项类型、8位数据长度和32位密钥,报头的总长度为6字节,其有效吞吐量**降低9.1%**。Passport包头开销是24字节，有效吞吐量**降低28.5%**。由于**SAV6将标签嵌入在源地址中，并未引入额外的标签**，所以，其有效吞吐量与对照组一致。

# 4.存储开销

{%asset_img fig6.png 图6 %}

边界路由器需要保存各自治系统的ASN和所协商的对称秘钥，因此需要衡量SAV6的存储开销。

目前ASN长32bits，截止2022年3月24已为边界路由器分配了123901个ASN。因此存储ASN需要约0.47MB（123901\*4B/1024/1024=0.4726MB）,对称秘钥为128bits,因此存储对称秘钥约1.89MB（0.4726*4=1.89MB）
。对于使用其他的加密算法，最多也不超过4.25MB，SAV6的存储开销是轻量的。

# 总结

本文提出了一种基于标签的IPv6互联网自治系统间源地址验证协议SAV6。SAV6定义了一种新的地址生成机制，将ASN嵌入到每个地址中，无需在数据包中插入任何有利于源地址验证的选项头。通过实现SAV6的原型并与其他协议进行了比较分析，评估结果表明，SAV6以轻量级开销为代价验证源地址，并且可以增量部署。

# 启发

(1)IPv6的地址空间大、地址位数多等新特性可以做很多事。如：抵抗地址扫描、提高隐私保护、地址真实性验证、隐蔽认证（地址嵌入认证的信息）、溯源（嵌入身份）等。
(2)实验需要做的充分，多与现有研究做对比。
