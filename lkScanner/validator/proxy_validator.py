import json
import time
import requests
from datetime import datetime
import config

class ProxyValidator(object):
    @staticmethod
    def proxy_valid(ip,port,proxy=None):
        proxies = {"http": "http://%s:%s" % (ip, port), "https": "https://%s:%s" % (ip, port)}
        flag,type,speed = Validator.check_proxy(proxies)
        _flag,_type,_speed = Validator.check_proxy(proxies,False)
        #http
        if flag and proxy:
            proxy.type = type
            proxy.protocol = 0
            proxy.speed = speed
        #https
        elif _flag and proxy:
            proxy.type = _type
            proxy.protocol = 1
            proxy.speed = _speed
        #http_https
        elif flag and _flag and proxy:
            proxy.type = _type
            proxy.protocol = 2
            proxy.speed = int((speed + _speed) / 2)
        return flag or _flag

    @staticmethod
    def check_proxy(proxies,is_http=True):
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
                return False,type,speed
            else:
                #判断什么类型，协议
                content = json.loads(response.text)
                client_ip = Validator.get_client_ip()
                headers = content['headers']
                ip = content['origin']
                #透明
                #例如:"origin": "42.234.9.201, 158.69.206.181"
                #还发现一个少见的情况headers中 "Forwarded": "for=本机IP:8419;by=srv-vpn:89",
                forwaded = headers.get('Forwarded','')
                if(client_ip in ip or ',' in ip or ip in forwaded):
                    type = 2
                #普通匿名 在headers中存在 "Proxy-Connection": "keep-alive" 还是暴漏了
                elif headers.get('Proxy-Connection',None):
                    type = 1
                else:
                    type = 0
                return True,type,speed

        except Exception as e:
            return False,type,speed
    @staticmethod
    def get_client_ip():
        response = requests.get(config.TEST_IP, timeout=config.TIMEOUT)
        content = json.loads(response.text)
        return content['origin']

if __name__ == '__main__':
    ip = '116.62.194.248'
    port = '3128'
    ProxyValidator.proxy_valid(ip,port)