import IPy
from scannerparam import ScannerParam

class IpHelper(object):
    @staticmethod
    def net_check(ip):
        return True

    @staticmethod
    def get_ip_list(scannerparam,parse_ip_segment=True):
        iplist = []
        if scannerparam.ip:
           iplist.extend(IpHelper.get_list(scannerparam.ip,parse_ip_segment))
        if scannerparam.ipfile:
            iplist.extend(IpHelper.get_list_by_file(ipfile,parse_ip_segment))
        return iplist

    #获取ip列表 例如传入192.168.0.0/16
    #返回该网段每一个ip构成的列表
    @staticmethod
    def get_list_by_segment(ip):
        result = []
        ip = IPy.IP(ip)
        for x in ip:
            result.append(str(x))
        return result

    @staticmethod
    def get_list(_ip,parse_ip_segment):
        #_ip 例如 1.1.1.1,2.2.0.0/16
        iplist = []
        result = []
        iparr = _ip.split(',')
        for ip in iparr:
            if '/' in ip and parse_ip_segment:
                result.extend(IpHelper.get_list_by_segment(ip))
            else:
                result.append(ip)
        return result
    @staticmethod
    def get_list_by_file(ipfile,parse_ip_segment):
        iplist = []
        result = []
        with open(ipfile) as f:
            for line in f.readlines():
                iplist.append(line.strip())
        for ip in iplist:
            iparr = ip.split(',')
            for x in iparr:
                if '/' in x and parse_ip_segment:
                    result.extend(IpHelper.get_list_by_segment(ip))
                else:
                    result.append(ip)
        return result

class PortHelper(object):
    @staticmethod
    def get_port_list(scannerparam):
        portlist=[]
        if scannerparam.port:
            portlist.extend(PortHelper.get_list(scannerparam.port))
        if scannerparam.portfile:
            portlist.extend(PortHelper.get_list_by_file(scannerparam.portfile))
        return portlist
    @staticmethod
    def get_list(port):
        #port 例如 21,22,23,500-600
        result = []
        portlist = port.split(',')
        for p in portlist:
            if '-' in p:
                port_range = p.split('-')
                result.extend(range(int(port_range[0]),int(port_range[1]) + 1))
            else:
                result.append(int(p))
        return result
    @staticmethod
    def get_list_by_file(portfile):
        portlist = []
        result = []
        with open(portfile) as f:
            for line in f.readlines():
                portlist.append(line.strip())
        for port in portlist:
            result.extend(PortHelper.get_list(port))
        return result
