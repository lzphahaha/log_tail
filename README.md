# log_tail
a small tool that can monitor log file with web browser


使用flask，websocket实现的一个可以在浏览器实时查看日志文件更新的工具，当一些小项目没有日志系统，  
而又不方便登录服务器时，可以使用该工具。
使用方法：
在服务部署项目，运行文件是log_file_tail.py
然后在浏览器打开：http://ip地址:30066/home