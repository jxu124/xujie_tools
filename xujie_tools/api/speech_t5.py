from flask import Flask, request, jsonify
from io import BytesIO
import soundfile as sf
import argparse
import base64
from xujie_tools.text_to_speech.speech_t5 import SpeechT5


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
    parser.add_argument("--api_path", default="/tts_service", type=str)
    parser.add_argument("--token", default="19960124", type=str)
    parser.add_argument("--cpu", default=False, action="store_true")
    parser.add_argument("--debug", default=False, action="store_true")
    parser.add_argument("--path_speecht5_tts", default='microsoft/speecht5_tts', type=str)
    parser.add_argument("--path_speecht5_hifigan", default='microsoft/speecht5_hifigan', type=str)
    parser.add_argument("--path_xvectors", default="Matthijs/cmu-arctic-xvectors", type=str)
    args = parser.parse_args()

    # 初始化
    t5_tts = SpeechT5(
        path_speecht5_tts=args.path_speecht5_tts,
        path_speecht5_hifigan=args.path_speecht5_hifigan,
        path_xvectors=args.path_xvectors
    )
    if not args.cpu:
        t5_tts = t5_tts.cuda()
    app = Flask(__name__)

    # 处理tts函数
    @app.route(args.api_path, methods=["POST"])
    def my_api_func():
        token = request.json.get("token")
        if token != args.token:
            return jsonify({"error": "Invalid token"}), 401
        text = request.json.get("text", "")
        speecher_id = request.json.get("speecher_id", 0)
        mp3, rate = t5_tts.get_mp3(text, speecher_id)
        return jsonify({'mp3': mp3.decode('utf-8'), 'rate': rate})

    print("Service Ready.")
    if args.debug:
        # for debug
        app.run(host=args.host, port=args.port, debug=args.debug)
    else:
        # for production deployment
        from gevent import pywsgi
        server = pywsgi.WSGIServer((args.host, args.port), app)
        server.serve_forever()
