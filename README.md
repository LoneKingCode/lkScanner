# lkScanner
### 多线程/协程 syn/tcp方式 扫描器

- 可验证是否为有效代理IP,并整理数据提交到指定接口入库(可配合本github中代理池接口)
- TCP方式扫描
- SYN方式扫描
- 通过字典验证mysql(暂无)
- 通过字典验证mssql(暂无)
- 通过字典验证ftp(暂无)

### 参数
参数名 | 值 | 作用
-|-|-
-c | tcp/syn | 连接模式 默认值:syn
-r | t/c | 运行模式 tcp时需要选择 t/c 多线程/协程 默认值:t
-tn | 整数 | 线程数,默认512
-t | 整数 | 连接超时时间 单位:秒 默认值:5
-ip | ip地址/范围 | 可以单个IP 1.1.1.1 或者IP范围 1.1.0.0/16,多个逗号隔开
-p | 端口范围 | 21,22,23 或者 1-500,900-1500 多个可逗号隔开
-ifile | ip地址范围文件 | 每行一个，多个可逗号隔开 默认值:data/port.txt
-pfile | 端口范围文件一行或多行 | 21,22,23 或者 1-500,900-1500 多个可逗号隔开 默认值:data/port.txt
-save | 保存位置 | 例如 result.txt or /result.txt or 完整路径
-v | proxy/mysql/mssql/ftp | 验证 proxy/mysql/mssql/ftp 验证 字典在data下

``` shell
scan.py -c tcp -save data/result.txt
scan.py -c tcp -r t -tn 512 -t 5 -ifile data/ip.txt -pfile data/port.txt -save result.txt
scan.py -c tcp -r c -tn 512 -t 5 -ifile data/ip.txt -pfile data/port.txt -save result.txt
scan.py -c syn -tn 512 -t 5 -ifile data/ip.txt -pfile data/port.txt -save result.txt
scan.py -c syn -tn 512 -t 5 -ifile data/ip.txt -pfile data/port.txt -save result.txt -v proxy
```
