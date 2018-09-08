from gevent import monkey
monkey.patch_socket()
import socket
socket.setdefaulttimeout(100)
import gevent
import time
class Scanner(object):
    def __init__(self):
        self.open_ports = []
    def scan(self,ip,port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            print('{0}:{1} open'.format(ip,port))
            self.open_ports.append(port)
            s.close()
        except socket.timeout as e:
            s.close()
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                print('{0}:{1} open'.format(ip,port))
                self.open_ports.append(port)
                s.close()
            except Exception as e:
                s.close()
        except Exception as e:
            s.close()



    def run(self,ip,port_start,port_end):
        tasklist = []
        for port in range(port_start,port_end):
            tasklist.append(gevent.spawn(self.scan,ip,port))
        gevent.joinall(tasklist)


if __name__ == '__main__':
    time_start = time.time()

    scanner = Scanner()
    scanner.run('176.31.180.38',5000,6000)
    print(scanner.open_ports)

    time_end = time.time()
    print('totally cost',time_end - time_start)