---
title: 研究中常用 Python 网络库总结
date: 2023-06-19 12:28:23
tags: 研究工具
---

## python 内置网络工具

官方中文文档：https://docs.python.org/zh-cn/3/library/index.html

### ipaddress

IP 地址解析（字符串、整数）、比较。

```python
import ipaddress

ip1 = ipaddress.IPv6Address(1)
ip2 = ipaddress.IPv6Address('::1')

ip1 == ip2

ip
# => IPv6Address('::1')

str(ip)
# => '::1'

int(ip)
# => 1

net = ipaddress.IPv6Network('2000::/64')

net
# => IPv6Network('2000::/126')

list(net)
# => [IPv6Address('2000::'), IPv6Address('2000::1'), IPv6Address('2000::2'), IPv6Address('2000::3')]

ipaddress.IPv6Network('2000::1/64')
# => raise ValueError

ipaddress.IPv6Network('2000::1/64', strict=False)
# => IPv6Network('2000::/64')

ipaddress.IPv6Address('2000::1') in ipaddress.IPv6Network('2000::/64')
# => True

iface = ipaddress.IPv6Address('2000::1/64')

iface.network
# => IPv6Network('2000::/64')

iface.ip
# => IPv6Address('2000::1')
```

### socket

封装了基本的套接字 API：

- IP 地址解析（字符串、字节）：inet_ntop/pton
- 域名解析：getaddrinfo
- 服务名称端口转换：getservbyname/getservbyport
- socket：
  + sock.setsockopt
  + sock.listen
  + sock.connect
  + sock.close
  + sock.shutdown
  + sock.recv
  + sock.send
  + ...

在实践中经常创建 UDP 套接字和 IP 原始套接字，可以参考 UNP。一般不直接
创建不可移植的 2 层原始套接字，而是使用 pcap 收发 2 层报文。

### threading 和 select

- thraeding：线程操作。
- select：参考 UNP 或 `man select(2)`，可以防止 IO 调用的阻塞。

这两个库常常联合使用创建接受者（receiver），例如：

```python
import socket
import select
import threading

recv_pkts = list()              # save received packets
quit_flag = False               # notice the receiver to quit

def receive(sock):
    while not quit_flag:
        # wait for sock to be readable, at most 0.1 sec
        rlist, _, _ = select.select([sock], [], [], 0.1)
        if rlist:               # sock is readable
            pkt = sock.recv()
            recv_pkts.append(pkt)

sock = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)

# create receiver (receive threading)
receiver = threading.Thread(target=receive, args=(sock, ))

# start receiver
quit_flag = False
receiver.start()

# *SEND PROBE AND CHECK RECV_PKTS*

# quit receiver
quit_flag = True
receiver.join()
```

### 数据处理：json, csv, base64

查看对应的文档。

## scapy

- 官方文档：https://scapy.readthedocs.io/en/latest/
- layers（DHCP、DNS、etc） 文档：https://scapy.readthedocs.io/en/latest/api/scapy.layers.html

scapy 的主要功能包括：抓包、读写 pcap 文件、发包（维护内置的路由表和邻
居表）、生成和解析报文。

```python
import scapy.all as sp
```

- 抓包：sp.sniff
- 读写 pcap 文件：sp.rdpcap/wrpcap
- 发包：sp.send/sendp/sr/srp
- 网络接口：sp.conf.iface/ifaces/get_if_*
- 路由表：sp.conf.route/route6
- 邻居表：sp.getmacbyip/getmacbyip6

生成报文：

```python
pkt = sp.Ether(dst='33:33:00:00:00:01') / \
    sp.IPv6(dst='ff02::1') / \
    sp.ICMPv6EchoRequest(data=b'hello?')
    
pkt
# => <Ether  dst=33:33:00:00:00:01 type=IPv6 |<IPv6  nh=ICMPv6 dst=ff02::1 |<ICMPv6EchoRequest  data='hello?' |>>>

bytes(pkt)
# => b'33\x00\x00...'

sp.IPv6 in pkt
# => True

pkt[sp.IPv6]
# => <IPv6  nh=ICMPv6 dst=ff02::1 |<ICMPv6EchoRequest  data='hello?' |>>

sp.ls(pkt)
# =>
"""
dst        : DestMACField                        = '33:33:00:00:00:01' ('None')
src        : SourceMACField                      = 'XXX' ('None')
type       : XShortEnumField                     = 34525           ('36864')
--
version    : BitField  (4 bits)                  = 6               ('6')
tc         : BitField  (8 bits)                  = 0               ('0')
fl         : BitField  (20 bits)                 = 0               ('0')
plen       : ShortField                          = None            ('None')
nh         : ByteEnumField                       = 58              ('59')
hlim       : ByteField                           = 64              ('64')
src        : SourceIP6Field                      = 'XXX' ('None')
dst        : DestIP6Field                        = 'ff02::1'       ('None')
--
type       : ByteEnumField                       = 128             ('128')
code       : ByteField                           = 0               ('0')
cksum      : XShortField                         = None            ('None')
id         : XShortField                         = 0               ('0')
seq        : XShortField                         = 0               ('0')
data       : StrField                            = b'hello?'       ("b''")
"""

sp.ls(sp.IPv6)
# =>
"""
version    : BitField  (4 bits)                  = ('6')
tc         : BitField  (8 bits)                  = ('0')
fl         : BitField  (20 bits)                 = ('0')
plen       : ShortField                          = ('None')
nh         : ByteEnumField                       = ('59')
hlim       : ByteField                           = ('64')
src        : SourceIP6Field                      = ('None')
dst        : DestIP6Field                        = ('None')
"""
```

解析报文：

```python
buf = bytes(pkt)

buf
# => b'33\x00\x00...'

ppkt = sp.Ether(buf)

ppkt
# => <Ether dst=33:33:00:00:00:01 src=...>
```

### pypcap

pypcap 封装了 libpcap，可以实现 2 层报文收发、读写 pcap 文件。

- Q：为什么不用 scapy 收发包？
- A：sp.sniff 不够灵活：阻塞到报文到达或硬超时时才能进行其它操作（可能
  一直阻塞无法退出），不能预编译 bpf 代码（等调用外部命令编译好 bpf 代
  码后报文造就到达然后被丢弃了）。
  
```python
import pcap

p = pcap.pcap(name='ens33')
```
  
发包：

```python
p.sendpacket(b'...')
```

收包：

```python
p.setfilter('ip6')

def cb(ts, pkt):
    print(f'capture {len(pkt)} bytes')
    
while True:
    # dont block python signal handler
    rlist, _, _ = select([p.fd], [], [], 0.1)
    if rlist:
        p.dispatch(1, cb)
```

## dnspython

官方文档：https://dnspython.readthedocs.io/en/stable/

dnspython 与 scapy 的 layers.DNS 结合 sr 相比更加提供了更多的功能，例
如解析 resolve.conf 文件，tcp 查询，多报文查询结果整合等等。


```python
import dns.reversename
import dns.message

name = dns.reversename.from_address('2000::1')

str(name)
# => '1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.ip6.arpa.'

query = dns.message.make_query(name, 'PTR')
# query = dns.message.make_query('www.baidu.com', 'AAAA')

query.to_wire()
# => b'\xd9f\x01...'

print(query.to_text())
# => id 55654\nopcode QUERY\n...

res = dns.query.udp(query, '240c::6666')  # dns.query.tcp to query via tcp
```
