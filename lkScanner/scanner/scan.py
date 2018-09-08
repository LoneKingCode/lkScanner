from scapy.all import *
import netaddr

ip = ['176.31.180.38']
port = [21,22]

ipArray = []
portArray = []
for i in ip: ipArray.extend([str(i) for i in  netaddr.IPNetwork(i).subnet(24)])
portArray = [port[i:i+3] for i in range(0, len(port), 3)]

for i in ip:
    for j in portArray:
        #send函数verbose参数为False避免输出很多东西
        send(IP(dst=i)/TCP(dport=j, flags=2), verbose=False)
        print(i,j)