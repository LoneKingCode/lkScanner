import argparse
import sys
import threading
from multiprocessing import Process
from scanner import syn_scanner,thread_scanner
from scanner.scanner_param import ScannerParam
from util.sqlhelper import SqlHelper
def main():
    SqlHelper.create_db()
    parser = argparse.ArgumentParser(description='lkScanner')

    parser.add_argument('-c',choices = ['tcp', 'syn'],help = '连接模式 tcp(即普通的connect)/syn 默认值:syn', type=str, default='tcp')
    parser.add_argument('-r', choices = ['t','c'],help = '运行模式 tcp时需要选择 t/c 多线程/协程 默认值:t', type=str, default='t')
    parser.add_argument('-tn',help = '线程数 默认值512', type=int, default=512)
    parser.add_argument('-t',help = '连接超时时间 单位:秒 默认值:5', type=int, default=5)
    parser.add_argument('-ip',help = 'ip地址 可以单个IP 1.1.1.1 或者IP范围 1.1.0.0/16,多个逗号隔开', type=int, required=None)
    parser.add_argument('-p',help = '端口范围 21,22,23 或者 1-500,900-1500 多个可逗号隔开', type=str,default=None)
    parser.add_argument('-ifile', help = 'ip地址范围文件 每行一个，多个可逗号隔开 默认值:data/port.txt', type=str, default='data/ip.txt')
    parser.add_argument('-pfile', help = '端口范围文件一行或多行 21,22,23 或者 1-500,900-1500 多个可逗号隔开 默认值:data/port.txt', type=str, default='data/port.txt')
    parser.add_argument('-save', help = '保存位置 例如 result.txt or /result.txt or 完整路径', type=str, default=None)
    parser.add_argument('-v', help = '验证 proxy/mysql/mssql/ftp 验证 字典在data下', type=str, default=None)

    args = parser.parse_args()
    scannerparam = ScannerParam(args.c,args.r,args.tn,args.t,args.ip,args.p,args.ifile,args.pfile,args.save,args.v)
    scannerparam.timeout = 10
    scannerparam.validator = 'proxy'
    if not args.ip and not args.ifile:
        print('请输入IP或设置IP地址范围文件')
    elif not args.p and not args.pfile:
        print('请输入端口或设置端口范围文件')
    elif args.c == 'syn':
        syn_scanner.run_syn_scanner(scannerparam)
    elif args.c == 'tcp':
        if args.r == 't':
            thread_scanner.run_thread_scanner(scannerparam)
        elif args.r == 'c':
            pass
            #coroutine_scanner.run_coroutine_scanner()
    else:
        print('缺少参数')

if __name__ == "__main__":
   main()