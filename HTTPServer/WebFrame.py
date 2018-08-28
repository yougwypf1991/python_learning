#!/usr/bin/env python3

from views import *

# 设置静态文件夹路径
STATIC_DIR = './static'

# 应用
class Application(object):
    def __init__(self, urls):
        self.urls = urls
        
    def __call__(self, env):
        method = env.get('METHOD', 'GET')
        path = env.get('PATH_INFO', '/')
        if method == 'GET':
            if path == '/' or path[-5:] == '.html':
                # 获取静态页面
                response = self.get_html(path)
            else:
                # 获取数据
                response = self.get_data(path)
        elif method == 'POST':
            pass
        elif method == 'PUT':
            pass
            
        return response
        
    def get_html(self, path):
        if path == '/':
        # 返回主目录
            filename = STATIC_DIR + '/index.html'
        else:
            filename = STATIC_DIR + path
            
        # 读取页面
        try:
            f = open(filename)
        except Exception:
            # 没有找到页面
            # 组织状态行
            responseHeadlers = "HTTP/1.1 404 Not Found\r\n"
            # 组织响应头
            responseHeadlers += "Content-Type: text/html\r\n"
            # 组织响应空行
            responseHeadlers += "\r\n"
            # 组织响应体
            responseBody = '<h1>Sorry, not found the page<h1>'
        else:
            # 找到页面
            # 组织状态行
            responseHeadlers = "HTTP/1.1 200 OK\r\n"
            # 组织响应头
            responseHeadlers += "Content-Type: text/html\r\n"
            # 组织响应空行
            responseHeadlers += "\r\n"
            # 组织响应体
            responseBody = f.read()
        finally:
            return responseHeadlers + responseBody
            
    def get_data(self, data):
        for url, handler in self.urls:
            if data == url:
                response_headers = "HTTP/1.1 200 OK\r\n"
                response_headers += '\r\n'
                response_body = handler()
                return response_headers + response_body
                
        response_headers = "HTTP/1.1 404 NOT FOUND\r\n"
        response_headers += '\r\n'
        response_body = '对不起，没有找到你请求的页面'
        return response_headers + response_body
            

urls = [
    ('/time', show_time),
    ('/hello', say_hello),
    ('/bye', say_bye)
]
            
app = Application(urls)         # 实现app(env)的调用
