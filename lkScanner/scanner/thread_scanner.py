import threading
import time
import socket
import os
import sys
from concurrent import futures
from scanner.scanner_param import ScannerParam
from util.nethelper import IpHelper,PortHelper
from util.filehelper import FileHelper

lock = threading.Lock()
class ThreadScanner(object):
    def __init__(self,scannerparam):
        self.scancount = 0
        self.scannerparam = scannerparam
        self.savepath =  FileHelper.get_save_path()
        if scannerparam.save:
            self.savepath = scannerparam.save
    def scan(self,param):
        ip = param['ip']
        port = param['port']
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            #print('{0}:{1} open'.format(ip,port))
            ipinfo = '{0}:{1}\n'.format(ip,port)
            lock.acquire()
            FileHelper.append(self.savepath,ipinfo)
            lock.release()
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

    def run(self):
        scannerparam = self.scannerparam

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

        with futures.ThreadPoolExecutor(max_workers=scannerparam.threadnum) as executor:
            param_left = len(params)
            param_iter = iter(params)
            jobs = {}
            while(param_left):
                for param in param_iter:
                    job = executor.submit(self.send,param)
                    jobs[job] = param
                    if len(jobs) > scannerparam.threadnum:
                        break
                for job in futures.as_completed(jobs):
                    param_left -= 1
                    #result = job.result()
                    del jobs[job]
                    break

        time_end = time.time()
        print('执行结束，共花费{0}秒'.format(time_end - time_start))
        for x in self.open_ports:
            print("{0}:{1} open \n".format(x['ip'],x['port']))

def run_thread_scanner(scannerparam):
    t_scanner = ThreadScanner(scannerparam)
    t_scanner.run()
