from scapy.all import *
def prn(pkt):
    print(pkt.sprintf("%IP.src%:%IP.sport%  %TCP.flags%"))

#sniff(filter='tcp and dst %s and tcp[13:1] & 18==18'%userIP, prn=prn)
#至于tcp[13:1] & 18==18是怎么来的，因为在syn扫描中，我们向目标端口发送SYN，
#如果它开放的话会回复SYN＋ACK，也就是SYN ACK位均为1，在上面tcp首部的图中，ACK为高位，
#SYN为低位，2(SYN) + 16(ACK) = 18。
#此外tcp[13:1]是tcpdump里的一个高级语法，意为取tcp数据包的下标为13的字节(也就是第14个字节)开始的1个字节，
#也就是上面图中flags所在的字节，这样用其值与18与一下，就过滤掉了别的包。
sniff(filter="tcp[13:1] & 18==18", prn=prn)