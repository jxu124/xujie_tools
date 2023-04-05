"""
### 版本1
你需要用python实现http的api代理服务。实现为一个class.

功能1：客户端可以通过发送一个json到http://[服务器ip]:[服务器port]/register来注册一个项目。
注册的json例子:
{
    "ip": 127.0.0.1,
    "port": 12345,
    "local_path": "local_path_1/test_1",
    "remote_path": "remote_path_1/test_2",
    "override": False  # (optional)
}
服务端的返回：
如果remote_path没有被注册，或者remote_path被注册但发生了override：
{
    "status": "ok",  # 或者"override"
}
如果remote_path被注册，但没设置override，或override未False：
{
    "status": "failed"
}

功能2：其他客户端可以通过访问http://[服务器ip]:[服务器port]/[remote_path]来访问注册的http://[注册客户端ip]:[注册客户端port]/[local_path]
{
    "remote_path": "remote_path_1/test_2",
    "data": ...
}
"data"部分会被转发给功能1中注册的另一个客户端，然后返回另一客户端返回的内容，实现代理。

功能3：以上功能需要使用线程池实现，且限制最大线程数。


### 版本2
用python实现一个http_api代理服务器的类，需要给予flask。它拥有这些功能：
- 注册功能：后端可以通过访问http://[server_ip]:[server_port]/register注册一个http://[register_ip]:[register_port]/[register_path]到服务器。
- 透明代理功能：客户端可以通过直接访问http://[server_ip]:[server_port]/[path]来访问对应的http://[register_ip]:[register_port]/[path]。
- get_apis：客户端可以访问http://[server_ip]:[server_port]/get_apis来得到一个已经注册的api列表。
- 你需要使用多线程来处理透明代理，最多可以有10个线程同时进行。

"""
from flask import Flask, request
import requests
import hashlib

get_hash = lambda data: hashlib.sha256(data.encode('utf-8')).hexdigest()


class HttpApiProxy:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.apis = {}
        self.tokens = [get_hash("xj19960124")]

        self.app = Flask(__name__)
        self.app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.app.add_url_rule('/unregister', 'unregister', self.unregister, methods=['POST'])
        self.app.add_url_rule('/get_apis', 'get_apis', self.get_apis)
        self.app.add_url_rule('/<path:path>', 'proxy', self.proxy)

    def register(self):
        if request.values.get('token', "0") not in self.tokens:
            return "Authentication failed", 403
        try:
            register_ip = request.values['ip']
            register_port = request.values['port']
            register_path = request.values['path']
            self.apis[register_path] = (register_ip, register_port)
            return 'Registered API: http://{}:{}{}'.format(register_ip, register_port, register_path)
        except:
            return "Missing or incorrect registration information.", 400

    def unregister(self):
        try:
            register_path = request.values['path']
            register_ip, register_port = self.apis[register_path]
            self.apis.pop(register_path)
            return 'Unregistered API: http://{}:{}{}'.format(register_ip, register_port, register_path)
        except:
            return "Failed", 400

    def get_apis(self):
        if request.args.get('token', "0") not in self.tokens:
            print(self.tokens, request.values.get('token', "0"))
            return "Authentication failed", 403
        return str(self.apis)

    def proxy(self, path):
        # if request.values.get('token', "0") not in self.tokens:
        #     return "Authentication failed", 403
        if path not in self.apis:
            return 'API path not found'

        api_url = 'http://{}:{}{}'.format(self.apis[path][0], self.apis[path][1], path)
        try:
            response = requests.get(api_url)
        finally:
            return response.content, response.status_code, response.headers.items()

    def run(self):
        self.app.run(host=self.server_ip, port=self.server_port, threaded=True)

if __name__ == '__main__':
    proxy_server = HttpApiProxy('localhost', 5000)
    proxy_server.run()

