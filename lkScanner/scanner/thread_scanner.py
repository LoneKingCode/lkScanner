import threading
import time
import socket
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from scanner_param import ScannerParam
from util.nethelper import IpHelper,PortHelper
from util.filehelper import FileHelper

RESULT_PATH = FileHelper.get_save_path()
class ThreadScanner(object):
    def __init__(self,lock):
        self.scancount = 0
        self.lock = lock
    def scan(self,param):
        ip = param['ip']
        port = param['port']
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            #print('{0}:{1} open'.format(ip,port))
            ipinfo = '{0}:{1}\n'.format(ip,port)
            self.lock.acquire()
            FileHelper.append(RESULT_PATH,ipinfo)
            self.lock.release()
            s.close()
        except socket.timeout as e:
            s.close()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                #print('{0}:{1} open'.format(ip,port))
                self.open_ports.add({'ip':ip,'port':port})
                s.close()
            except Exception as e:
                s.close()
        except Exception as e:
            s.close()
        self.scancount = self.scancount + 1
        sys.stdout.write('\r' + '已扫描:{0},剩余{1}'.format(self.scancount, self.taskcount - self.scancount))
        sys.stdout.flush()

    def run(self,scannerparam):
        socket.setdefaulttimeout(scannerparam.timeout)
        time_start = time.time()
        print('开始执行...')
        params = []
        iplist = IpHelper.get_ip_list(scannerparam)
        portlist = PortHelper.get_port_list(scannerparam)
        self.ipcount = len(iplist)
        for ip in iplist:
            for port in portlist:
                params.append({'ip':ip,'port':port})

        self.taskcount = len(params)
        print('线程数:{0},ip总数:{1},待扫描任务总数:{2}'.format(scannerparam.threadnum, len(iplist),self.taskcount))

        with ThreadPoolExecutor(max_workers=scannerparam.threadnum) as executor:
            results = executor.map(self.scan,params)
        time_end = time.time()
        print('执行结束，共花费{0}秒'.format(time_end - time_start))
        for x in self.open_ports:
            print("{0}:{1} open \n".format(x['ip'],x['port']))

if __name__ == '__main__':
    lock = threading.Lock()
    scannerparam = ScannerParam('tcp','t',1000,5,'176.31.0.0/16','3389','','')
    t_scanner = ThreadScanner(lock)
    t_scanner.run(scannerparam)
