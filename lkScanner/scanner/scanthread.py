import threading
import time
import socket
socket.setdefaulttimeout(100)
#lock = threading.Lock()
threads = []
class Scanner(object):
    def __init__(self):
        self.open_ports=[]
    def scan(self,ip,port):
        #lock.acquire()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            print('{0}:{1} open'.format(ip,port))
            self.open_ports.append(port)
            s.close()
        except Exception as e:
            print('{0}:{1} close err:{2}'.format(ip,port))
            pass


        #lock.release()
    def run(self,ip,port_start,port_end):
        for port in range(port_start,port_end):
             t = threading.Thread(target=self.scan,args=(ip,port))
             threads.append(t)
             t.start()
        for t in threads:
            t.join()


if __name__ =='__main__':
    time_start=time.time()

    scanner = Scanner()
    scanner.run('176.31.180.38',5000,6000)
    print(scanner.open_ports)

    time_end=time.time()
    print('totally cost',time_end-time_start)