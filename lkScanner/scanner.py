import argparse
import sys
def helpinfo():
    print('scanner.py -c <connectmode> -r <runmode> -t <timeout> -ip <ip> -p <port> -if <ipfile> -pf <portfile>')

def main():
    parser = argparse.ArgumentParser(description='lkScanner')

    parser.add_argument('-c',choices = ['tcp', 'syn'],help = '连接模式 tcp(即普通的connect)/syn 默认值:syn', type=str, default='syn')
    parser.add_argument('-r', choices = ['t','c'],help = '运行模式 tcp时需要选择 t/c 多线程/协程 默认值:t', type=str, default='t')
    parser.add_argument('-tn',choices = [],help = '选择多线程时 需要输入线程数 默认值512', type=int, default=512)
    parser.add_argument('-t', choices = [],help = '连接超时时间 单位:秒 默认值:100', type=int, default=100)
    parser.add_argument('-ip', choices = [],help = 'ip地址 可以单个IP 1.1.1.1 或者IP范围 1.1.0.0/16', type=int, required=True)
    parser.add_argument('-p', choices = [],help = '端口范围 21,22,23 或者 1-500,900-1500 多个可逗号隔开', type=str,default=None)
    parser.add_argument('-if',choices = [], help = 'ip地址文件 每行一个', type=str, default=None)
    parser.add_argument('-pf',choices = [], help = '端口文件 端口范围 21,22,23 或者 1-500,900-1500 多个可逗号隔开', type=str, default=None)

    args = parser.parse_args()



    print(args)
if __name__ == "__main__":
   main()