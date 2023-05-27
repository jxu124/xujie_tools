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

### TTS - VITS(zh,jp)

服务端：
- 后面的参数也可以不加，这样程序会自动成huggingface上面下载模型参数。
- 如果还想了解更多：https://huggingface.co/spaces/zomehwh/vits-uma-genshin-honkai
```bash
python3 xujie_tools/api/vits_genshin.py \
    --fp16 \
    --token "urlsafe_token" \
    --path_config "/mnt/bn/hri-lq/projects/VITS/vits-uma-genshin-honkai/model/config.json" \
    --path_ckpt "/mnt/bn/hri-lq/projects/VITS/vits-uma-genshin-honkai/model/G_953000.pth" 
```

客户端：
- 可以在`requests.post`前加上`try`以避免网络不好的时候报错跳出
- tips: 可以发送token给`/vits_service/get_speakers`获得可用的speaker列表（名字）
```python
from io import BytesIO
import requests
import base64
import soundfile as sf

# 发送请求并等待tts结果(mp3格式)
data = {
    "token": "urlsafe_token",  # 简单校验用的token
    "text": "你好，可莉不知道哦。",  # 要转换的文字
    "speecher_id": 329,  # 可以省略，选择音色，默认为可莉
    "param": [0.1, 0.668, 1.2]  # 可以省略，这里是默认值
}
ret = requests.post("http://[fdbd:dc03:9:138:5400::e]:5010/vits_service", json=data).json()
with BytesIO(base64.urlsafe_b64decode(ret['mp3'].encode())) as f:
    wav, rate = sf.read(f)

# 如果使用jupyter
import IPython.display as ipd
ipd.Audio(wav, rate=rate)
```


> pip3 install text_generation icetk cpm_kernels

### Chatbot - chatglm(zh,en)

依赖：
"""bash
pip3 install text_generation icetk cpm_kernels
"""

服务端：
- 后面的参数也可以不加，这样程序会自动成huggingface上面下载模型参数。
- 如果还想了解更多：https://huggingface.co/THUDM/chatglm-6b
- 另外，量化模型可以看看这个：https://huggingface.co/spaces/josStorer/ChatGLM-6B-Int4-API-OpenAI-Compatible
- 官方实现：https://huggingface.co/THUDM/chatglm-6b-int4 与介绍 https://zhuanlan.zhihu.com/p/624317092
- 启用int4推理：直接在更改参数即可，`--path_model "THUDM/chatglm-6b-int4"`。
- 启用cpu：直接在后面加`--cpu`
```bash
python3 xujie_tools/api/chatglm.py \
    --token "urlsafe_token" \
    --path_model "/mnt/bn/hri-lq/projects/VITS/chatglm-6b"
```

客户端：
- 可以在`requests.post`前加上`try`以避免网络不好的时候报错跳出
```python
import requests

data = {
    "token": "urlsafe_token",  # 简单校验用的token
    "text": "你好。",  # 要转换的文字
    "history": [("1+1=?", "2")],  # 可以省略，历史对话信息
    "param": [1.0, 1.0]  # 可以省略，这里是默认值
}
ret = requests.post("http://[fdbd:dc03:9:138:5400::e]:5010/vits_service", json=data).json()
print(ret['text'])
```
