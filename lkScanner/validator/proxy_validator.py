import json
import threading
import time
import requests
from concurrent import futures
from datetime import datetime
import config
import os
from util.sqlhelper import SqlHelper
from util.loghelper import LogHelper
from util.filehelper import FileHelper

lock = threading.Lock()

class ProxyValidator(object):
    def __init__(self,data_flag):
        self.data_flag = data_flag
        self.proxies = set()
        self.savepath = os.path.join(config.BASE_DIR,'data/proxy_' + data_flag + '.txt')

    def run(self):
        print('开始验证代理')
        data = SqlHelper.get(None,{'flag':self.data_flag})
        print('共{0}条数据待验证'.format(len(data)))
        count = 0
        #tasklist = []
        #for row in data:
        #        tasklist.append(gevent.spawn(self.check_proxy_and_save,row['ip'],row['port']))
        #gevent.joinall(tasklist)
        thread_num = 50
        with futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
            param_left = len(data)
            param_iter = iter(data)
            jobs = {}
            while(param_left):
                for param in param_iter:
                    job = executor.submit(self.check_proxy_and_save,param.ip,param.port)
                    jobs[job] = param
                    if len(jobs) > thread_num:
                        break
                for job in futures.as_completed(jobs):
                    param_left -= 1
                    #result = job.result()
                    del jobs[job]
                    break
        print('验证完成')
        save = True
        if save:
            count = len(self.proxies)
            if count <= 0:
                print('无有效代理，本次不同步到代理池')
                return
            print('共{0}条有效代理,开始同步到代理池'.format(count))

            data = list(self.proxies)
            LogHelper.debug('开始同步:')
            try:
                self.send_data_to_server(data)
            except :
                try:
                    self.send_data_to_server(data)
                except Exception as e :
                    LogHelper.error('同步数据到代理池出错:' + str(e))
                    LogHelper.error(data)

    def send_data_to_server(self,data):
        headers = {
                "Content-Type": "application/json; charset=UTF-8",
            }
        response = requests.post(config.API_SERVER_URL,json=json.dumps(data),headers=headers)
        if response.status_code != 200:
            response = requests.post(config.API_SERVER_URL,json=json.dumps(data),headers=headers)
            if response.status_code != 200:
                print('同步数据到代理池失败')
                LogHelper.error('同步数据到代理池失败')
                LogHelper.error(data)
                LogHelper.error(response)
        else:
            text = response.text
            LogHelper.debug(text)
            print('同步完成，服务器返回信息:',end='')
            print(text)
    def check_proxy_and_save(self,ip,port):
        if self.proxy_valid(ip,port):
            self.proxies.add(config.PROXY_DATA_TEMPLATE.format(ip=ip,port=port))
            lock.acquire()
            FileHelper.append(self.savepath,'{0}:{1}\n'.format(ip,port))
            lock.release()
            print('{0}:{1} 有效√'.format(ip,port))
        else:
             print('{0}:{1} 无效×'.format(ip,port))

    def proxy_valid(self,ip,port):
        proxies = {"http": "http://%s:%s" % (ip, port), "https": "https://%s:%s" % (ip, port)}
        flag = self.check_proxy(proxies)
        _flag = self.check_proxy(proxies,False)
        return flag or _flag

    def check_proxy(self,proxies,is_http=True):
        if is_http:
            test_url = config.TEST_HTTP_HEADER
        else:
            test_url = config.TEST_HTTPS_HEADER
        type = protocol = speed = 0
        start = time.time()
        try:
            response = requests.get(test_url, proxies=proxies, timeout=config.TIMEOUT)
            speed = round(time.time() - start, 2)
            if response.status_code != 200:
                return False
            else:
                return True

        except Exception as e:
            return False

if __name__ == '__main__':
    v = ProxyValidator('20180915213922')
    v.run()