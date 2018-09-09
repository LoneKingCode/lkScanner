import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='lkScanner')

    parser.add_argument('-c',choices = ['tcp', 'syn'],help = '连接模式 tcp(即普通的connect)/syn 默认值:syn', type=str, default='syn')
    parser.add_argument('-r', choices = ['t','c'],help = '运行模式 tcp时需要选择 t/c 多线程/协程 默认值:t', type=str, default='t')
    parser.add_argument('-tn',choices = [],help = '选择多线程时 需要输入线程数 默认值512', type=int, default=512)
    parser.add_argument('-t', choices = [],help = '连接超时时间 单位:秒 默认值:100', type=int, default=100)
    parser.add_argument('-ip', choices = [],help = 'ip地址 可以单个IP 1.1.1.1 或者IP范围 1.1.0.0/16,多个逗号隔开', type=int, required=None)
    parser.add_argument('-p', choices = [],help = '端口范围 21,22,23 或者 1-500,900-1500 多个可逗号隔开', type=str,default=None)
    parser.add_argument('-ifile',choices = [], help = 'ip地址范围文件 每行一个，多个可逗号隔开', type=str, default=None)
    parser.add_argument('-pfile',choices = [], help = '端口范围文件一行或多行 21,22,23 或者 1-500,900-1500 多个可逗号隔开', type=str, default=None)
    parser.add_argument('-save',choices = [], help = '保存位置 例如 result.txt or /result.txt or 完整路径', type=str, default=None)

    args = parser.parse_args()

    if not args.ip and not args.ifile:
        print('请输入IP或设置IP地址范围文件')
    elif not args.port and not args.pfile:
        print('请输入端口或设置端口范围文件')
    else:
        pass
if __name__ == "__main__":
   main()