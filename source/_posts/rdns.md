---
title: 基于 DNS 协议收集全球 IPv6 地址数据集
date: 2023-02-06 19:11:58
tags: 网络扫描
---

# Something From Nothing: Collecting Global IPv6 Datasets from DNS

本研究主要有三个工作：

1. 提出了一种新的方法枚举已分配的 IPv6 地址，无需访问网络中特定的有利位置。
2. 记录了使用上述技术进行的一次全球扫描，在该扫描中收集了更大、更多样的 IPv6 地址数据集。
3. 提供了一个研究案例，展示如何利用上述技术探测运营商的网络。

## 基于 DNS 查询的通用扫描方法

{% asset_img fig1.png 图1 IPv6 PTR 树示例 %}

图 1 展示了一个 DNS 服务器的 IPv6 PTR 树，一个深度为 32 的正 16 叉树。以 ip6.arpa 为根，每个节点有 16 个分支，对应半字节 0-f，靠近根的一端为前缀。图 1 所示的 PTR 树包含一个前缀为 f0f0::/12 的 IPv6 地址。

查询 PTR 树中不同的节点的响应不同：查询 0-e.ip6.arpa 时响应 NXDOMAIN，表示本域名和所有子域名都没有记录；查询 f.ip6.arpa 时响应 NOERROR，表示本域名没有记录，但是子域名可能有记录；遍历该树时可以针对 NXDOMAIN 响应进行减枝。

上述方法不仅可以应用到对普通 DNS 服务器的非递归查询遍历，还可以应用到对代理了一个区域的反向域名解析的权威 DNS 服务器的递归查询遍历，但是如果一个区域的权威 DNS 服务器不符合 RFC8020 规范则无法枚举该区域。作者从公开的数据集：Routeviews 和 RIPE RIS 中收集了一些区域（全球 BGP 通告的前缀）作为全球扫描的起点。

在实现上述全球扫描方法的过程中出现了一些问题：

1. 广度优先 VS 深度优先：本研究采用局部深度优先的广度优先遍历，用广度遍历分别遍历出 32 位、48 位、64 位前缀和 128 位完整的 IPv6 地址，而每一步遍历的过程是深度优先的。
2. 道德考量和性能：应考虑流量限制、负载均衡和并行化，均衡地探测所有区域，避免对一个区域的权威 DNS 服务器造成 DOS 攻击。 3. 动态生成区域检测：有些 DNS 服务器根据 IPv6 地址、域名映射动态地生成 DNS 记录，此时该区域内的任何 IPv6 地址都是存在的，不会进行减枝，因此应检测动态生成区域。本研究根据反向查询一些不常见的地址的响应数检测动态生成区域。
4. 黑名单：根据某些运营商要求，或者检测到动态生成区域，应将这些前缀加入黑名单。
5. 空终端：本研究发现了一些 IPv6 地址的路径上未响应 NXDOMAIN，但 PTR 记录不存在的情况，深入研究后发现可能存在 CNAME 记录，因此探测中如果 PTR 记录不存在就尝试查询 CNAME 记录。

## 全球扫描实验

{%asset_img fig2.png 表1 全球扫描实验结果 %}

表 1：Runtime 时间（分钟）| Records Found 记录数 | Address 地址数 | Dynamic Zones 动态生成区域

本研究进行了三次扫描，结果见表 1。第一次扫描未使用内置区域数据集；第二次扫描与第一次扫描相比使用了内置的区域数据集；第三次扫描与第二次扫描相比使用了更多线程。

设置第一次扫描的目的是比较内置的区域数据集的影响：第一次扫描因不使用内置的区域数据集而枚举到的记录数远少于第二次扫描。造成该结果的可能原因是从根域名开始遍历可能会导致前缀长度过短，根域名服务器无法决定权威 DNS 服务器而错误剪枝。

第二次扫描使用内置的区域数据集聚合的 32 位前缀记录，不实际枚举。数据集中超过 32 位的区域添加其本身和 32 位截取两个前缀记录，因此 Records Found 中 Seed 到 32 增加了 1k；收到了大量 42 位前缀记录，但大部分是动态生成区域；发现了未在任何通告的前缀中的地址。

第三次扫描与第二次扫描相比线程数从 80 增加到 400，扫描的时间大幅减少；枚举到更多的 64 位前缀记录，经过分析发现是因为丢包造成动态生成区域检测失败；枚举到的地址数更少，可以看出线程增加造成的丢包率提升对扫描的影响。

## 研究案例：分析一个运营商的网络

{% asset_img fig3.png 图4 运营商网络地址分布概览 %}

该研究案例先获取了一个运营商的三个网络前缀，分别对应三个区域。用上述技术对这三个区域进行了两次扫描，结果见图 4。

图 4.a 展示了枚举出的地址的半字节分布。前 32 位可以看出有三个前缀； 32-48 位可以看到网络被拆分；48-64 位，第一个半字节以 0 或 8 区分网络基础设施和普通节点，后三个半字节用于线性分配 /64；64-128 位可以看到 /64 内的主机的地址也是线性分配。

图 4.b 是 /64 内的主机数的箱线图。观察到只有两个 /64 内的主机数超过 250，深入研究后发现这两个 /64 与跨多个接入点的骨干网络和防火墙有关；本研究还观察到 IPv6 PTR记录是网络人员手工分配的，因为存在拼写错误。