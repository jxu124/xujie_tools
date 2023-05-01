from flask import Flask, request, jsonify
import argparse
from xujie_tools.text_to_speech.vits_genshin import VITSGenshin


"""
使用方法：
import requests

data = {
    "token": "urlsafe_token",
    "text": "hello world!",
    "speecher_id": 3000
}
ret = requests.post("http://[fdbd:dc03:9:130:6a00::33]:5010/tts_service", json=data).json()

with BytesIO(base64.urlsafe_b64decode(ret['mp3'].encode())) as f:
    wav, rate = sf.read(f)
ipd.Audio(wav, rate=rate)
"""

# 我需要设置校验函数（或者token具体值）、处理函数、API路径、端口
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "--ip", default="::", type=str)
    parser.add_argument("--port", default=5010, type=int)
    parser.add_argument("--api_path", default="/vits_service", type=str)
    parser.add_argument("--token", default="19960124", type=str)
    parser.add_argument("--cpu", default=False, action="store_true")
    parser.add_argument("--debug", default=False, action="store_true")
    parser.add_argument("--path_ckpt", default="", type=str)
    parser.add_argument("--path_config", default="", type=str)
    args = parser.parse_args()

    if args.path_config == "":
        import huggingface_hub
        args.path_config = huggingface_hub.hf_hub_download("zomehwh/vits-uma-genshin-honkai", "model/config.json", repo_type='space')
    if args.path_ckpt == "":
        import huggingface_hub
        args.path_ckpt = huggingface_hub.hf_hub_download("zomehwh/vits-uma-genshin-honkai", "model/G_953000.pth", repo_type='space')
    # 初始化
    device = 'cpu' if args.cpu else 'cuda'
    vits = VITSGenshin(args.path_ckpt, args.path_config, device=device)
    app = Flask(__name__)

    # 处理tts函数
    @app.route(args.api_path, methods=["POST"])
    def vits_api():
        token = request.json.get("token")
        if token != args.token:
            return jsonify({"error": "Invalid token"}), 401
        text = request.json.get("text", "")
        language = request.json.get("language", 0)
        speecher_id = request.json.get("speecher_id", 329)
        param = request.json.get("param", [0.1, 0.668, 1.2])
        mp3, rate = vits.get_mp3(text, language, speecher_id, *param)
        return jsonify({'mp3': mp3.decode('utf-8'), 'rate': rate})
    
    # 处理tts函数
    @app.route(f"{args.api_path}/get_speakers", methods=["POST"])
    def get_speakers_api():
        token = request.json.get("token")
        if token != args.token:
            return jsonify({"error": "Invalid token"}), 401
        speakers = vits.get_speakers()
        return jsonify({'speakers': speakers})

    print("Service Ready.")
    if args.debug:
        # for debug
        app.run(host=args.host, port=args.port, debug=args.debug)
    else:
        # for production deployment
        from gevent import pywsgi
        server = pywsgi.WSGIServer((args.host, args.port), app)
        server.serve_forever()
