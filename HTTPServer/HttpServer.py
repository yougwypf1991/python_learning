#!/usr/bin/env python3

from socketserver import *
from socket import *
from threading import Thread
import time, sys, re, readline
from setting import *

# 存放静态页面的路径
STATIC_DIR = "./static"
ADDR = ('0.0.0.0', 8000)

# 定义一个HTTPServer类，用来封装具体的功能
class HTTPServer(object):
    def __init__(self, application):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.application = application
    
    def bind(self, host, port):
        self.host = host
        self.port = port
        self.sockfd.bind((self.host, self.port))
        
    def serve_forever(self):
        self.sockfd.listen(10)
        print('Listen the port %d...' % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print('Connect from ', addr)
            # 创建线程， 目标函数为self.client_handler, 参数为connfd为元组
            handle_client = Thread(target = self.client_handler, args = (connfd,))
            # 设置父线程终止后，子线程不退出
            handle_client.setDaemon(True)
            # 启动线程
            handle_client.start()
            
    def client_handler(self, connfd):
        # 接收浏览器的请求
        request = connfd.recv(4096)
        # 可以分析请求头和请求体
        request_lines = request.splitlines()
        # 获取请求行 [请求类型 空格 请求内容 空格 协议类型]
        request_line = request_lines[0].decode('utf-8')
        # 获取请求方法和请求内容
        # findall的第一个子组返回元组的第一个元素，第二个子组返回元组的第二个元素
        # method, filename = re.findall(r'^([A-Z]+)\s+(/\S*)', request_line)[0]
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'
        try:
            env = re.match(pattern, request_line).groupdict()
        except:
            response_handlers = 'HTTP/1.1 500  Server Error.\r\n'
            # 一定要加\r\n
            response_handlers += '\r\n'
            response_body = 'server error'
            response = response_handlers + response_body
            connfd.send(response.encode())
        # 将env给Frame处理，得到返回内容
        response = self.application(env)
        if response:
            connfd.send(response.encode())
            connfd.close()
        
    
if __name__ == "__main__":
    # 将要使用的模块导入进来
    sys.path.insert(1, MODULE_PATH)
    m = __import__(MODULE)
    application = getattr(m, APP)
    
    # 生成服务器对象
    httpd = HTTPServer(application)
    httpd.bind(HOST, PORT)
    # 启动服务器
    httpd.serve_forever()