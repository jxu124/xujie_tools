
"""
用python写一个api服务器的类。
- 服务器一开始需要向http://[master_ip]:[master_port]/register发送一个数据包含ip、port、path。
- 只需要响应/test/hello_world这一个地址
- 响应结果为{"test_name": "hello_world!"}

"""
import requests
from flask import Flask, jsonify, request
import hashlib

get_hash = lambda data: hashlib.sha256(data.encode('utf-8')).hexdigest()

class APIServer:
    def __init__(self, ip, port, path, token, master_ip="127.0.0.1", master_port=5000):
        self.ip = ip
        self.port = port
        self.path = path
        
        self.master_ip = master_ip
        self.master_port = master_port
        self.token = token

        # 注册到主服务器
        self.register()

        # 创建Flask应用程序
        self.app = Flask(__name__)

        # 添加路由
        self.add_routes()

    def register(self):
        # 向主服务器注册
        url = f'http://{self.master_ip}:{self.master_port}/register'
        data = {'ip': self.ip, 'port': self.port, 'path': self.path, "token": self.token}
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise Exception('Failed to register with master server')
        
    def unregister(self):
        url = f'http://{self.master_ip}:{self.master_port}/unregister'
        data = {'path': self.path}
        response = requests.post(url, data=data)

    def add_routes(self):
        @self.app.route(self.path)
        def hello_world():
            print(request.data)
            return jsonify({'test_name': 'hello_world!'})

    def run(self):
        try:
            self.app.run(host=self.ip, port=self.port)
        finally:
            self.unregister()


if __name__ == "__main__":
    # import requests
    # data = {"ip": "127.0.0.1", "port": 5001, "path": "/test/hello_world"}
    # requests.post("http://localhost:5000/register", data=data)

    server = APIServer('127.0.0.1', 5001, '/test/hello_world', token=get_hash("xj19960124"))
    server.run()


