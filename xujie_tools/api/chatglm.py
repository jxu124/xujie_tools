from flask import Flask, request, jsonify
import argparse
from xujie_tools.chatbot.chatglm import ChatGLM


# 我需要设置校验函数（或者token具体值）、处理函数、API路径、端口
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "--ip", default="::", type=str)
    parser.add_argument("--port", default=5010, type=int)
    parser.add_argument("--api_path", default="/chatglm_service", type=str)
    parser.add_argument("--token", default="19960124", type=str)
    parser.add_argument("--cpu", default=False, action="store_true")
    parser.add_argument("--debug", default=False, action="store_true")
    parser.add_argument("--path_model", default="", type=str)
    args = parser.parse_args()

    # 初始化
    device = 'cpu' if args.cpu else 'cuda'
    chatglm = ChatGLM(path_chatglm=args.path_model, device=device)
    app = Flask(__name__)

    # 处理tts函数
    @app.route(args.api_path, methods=["POST"])
    def chatglm_api():
        token = request.json.get("token")
        if token != args.token:
            return jsonify({"error": "Invalid token"}), 401
        text = request.json.get("text", "")
        history = request.json.get("history", [])
        param = request.json.get("param", [1.0, 1.0])
        response, history = chatglm(text, history, *param)
        return jsonify({'text': response, 'status': "finished"})
    
    # TODO stream ver. 版本之后实现

    print("Service Ready.")
    if args.debug:
        # for debug
        app.run(host=args.host, port=args.port, debug=args.debug)
    else:
        # for production deployment
        from gevent import pywsgi
        server = pywsgi.WSGIServer((args.host, args.port), app)
        server.serve_forever()
