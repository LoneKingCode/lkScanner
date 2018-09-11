from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor
from scapy.all import *
import netaddr
from scanner.scanner_param import ScannerParam
from util.nethelper import IpHelper,PortHelper
from util.filehelper import FileHelper
from util.sqlhelper import SqlHelper
import sys
import time
import datetime
lock = threading.Lock()
class SynScanner(object):
    def __init__(self,scannerparam):
        #self.ifacestr = "Intel(R) Dual Band Wireless-AC 3160"
        self.sendcount = 0
        self.scannerparam = scannerparam
        self.savepath =  FileHelper.get_save_path()
        self.data_flag = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if scannerparam.save:
            self.savepath = scannerparam.save
    def prn(self,pkt):
        ipinfo = pkt.sprintf("%IP.src%:%IP.sport%\n")
        ip = pkt.sprintf('%IP.src%')
        port = int(pkt.sprintf('%IP.sport%'))
        if port in self.portlist:
            lock.acquire()
            FileHelper.append(self.savepath,ipinfo)
            model = dict(ip=ip,port=port,flag=self.data_flag,createdatetime= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            SqlHelper.add(model)
            lock.release()
            #self.open_ports.add({'ip':ip,'port':port})

    def listen(self,portlist):
        self.portlist = portlist
        #sniff(filter='tcp and dst %s and tcp[13:1] & 18==18'%userIP, prn=prn)
        #至于tcp[13:1] & 18==18是怎么来的，因为在syn扫描中，我们向目标端口发送SYN，
        #如果它开放的话会回复SYN＋ACK，也就是SYN ACK位均为1，在上面tcp首部的图中，ACK为高位，
        #SYN为低位，2(SYN) + 16(ACK) = 18。
        #此外tcp[13:1]是tcpdump里的一个高级语法，意为取tcp数据包的下标为13的字节(也就是第14个字节)开始的1个字节，
        #也就是上面图中flags所在的字节，这样用其值与18与一下，就过滤掉了别的包。
        sniff(filter="tcp[13:1] & 18==18", prn=self.prn) #iface=self.ifacestr


    def send(self,param):
        ip = param['ip']
        port = param['port']
        send(IP(dst=ip) / TCP(dport=port, flags=2), verbose=False)

        self.sendcount = self.sendcount + 1

        sys.stdout.write('\r' + '已扫描:{0},剩余{1}'.format(self.sendcount, self.taskcount - self.sendcount))
        sys.stdout.flush()


    def run(self):
        time_start = time.time()
        print('开始执行...')
        scannerparam = self.scannerparam
        if scannerparam.save:
            RESULT_PATH = scannerparam.save
        params = []
        iplist = IpHelper.get_ip_list(scannerparam)
        portlist = PortHelper.get_port_list(scannerparam)

        p_listen = Process(target=self.listen,args=(portlist,))
        p_listen.start()

        for ip in iplist:
            for port in portlist:
                params.append({'ip':ip,'port':port})
        self.taskcount = len(params)
        print('ip总数:{0},待扫描任务总数:{1}'.format(len(iplist),self.taskcount))

        with ThreadPoolExecutor(max_workers=scannerparam.threadnum) as executor:
            results = executor.map(self.send,params)

        time_end = time.time()
        print('\n发送数据包结束，共花费{0}秒'.format(time_end - time_start))
        #for x in self.open_ports:
        #    print("{0}:{1} open \n".format(x['ip'],x['port']))

        print('等待20秒结束监听进程')
        time.sleep(20)
        print('执行结束')
        p_listen.terminate()

        if scannerparam.func:
            print('开始执行{0}'.format(scannerparam.func))
            validate(scannerparam)

    def validate(self,scannerparam):
        if 'proxy' in scannerparam.func:
            proxy_validator = ProxyValidator(self.data_flag)
            p_proxy = Process(target=proxy_validator.run)
            p_proxy.start()
            p_proxy.join()


def run_syn_scanner(scannerparam):
    syn_scanner = SynScanner(scannerparam)
    syn_scanner.run()