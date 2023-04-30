# xujie_tools

这个项目主要放置一些比较通用的数据处理脚本，目前正在施工中。。。

## API 接口

### TTS - SpeechT5(en)

服务端：
- 后面的参数也可以不加，这样程序会自动成huggingface上面下载模型参数。
- 如果还想了解更多：https://huggingface.co/microsoft/speecht5_tts
```bash
python3 xujie_tools/api/speech_t5.py \
    --token "urlsafe_token" \
    --path_speecht5_tts "/mnt/bn/hri-lq/projects/VITS/speecht5_tts" \
    --path_speecht5_hifigan "/mnt/bn/hri-lq/projects/VITS/speecht5_hifigan" \
    --path_xvectors "/mnt/bn/hri-lq/projects/VITS/cmu-arctic-xvectors"
```

客户端：
- 可以在`requests.post`前加上`try`以避免网络不好的时候报错跳出。
```python
from io import BytesIO
import requests
import base64
import soundfile as sf

# 发送请求并等待tts结果(mp3格式)
data = {
    "token": "urlsafe_token",  # 简单校验用的token
    "text": "hello world",  # 要转换的文字
    "speecher_id": 3000  # 选择音色
}
ret = requests.post("http://[fdbd:dc03:9:130:6a00::33]:5010/tts_service", json=data).json()
with BytesIO(base64.urlsafe_b64decode(ret['mp3'].encode())) as f:
    wav, rate = sf.read(f)

# 如果使用jupyter
import IPython.display as ipd
ipd.Audio(wav, rate=rate)
```


