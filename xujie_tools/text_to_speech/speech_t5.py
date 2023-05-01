# Following pip packages need to be installed:
# !pip install git+https://github.com/huggingface/transformers sentencepiece datasets

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf
from datasets import load_dataset
# import IPython.display as ipd
from io import BytesIO
import base64


class SpeechT5():
    """ https://huggingface.co/microsoft/speecht5_tts """
    cuda:bool = False

    def __init__(self, path_speecht5_tts='microsoft/speecht5_tts', path_speecht5_hifigan='microsoft/speecht5_hifigan', path_xvectors="Matthijs/cmu-arctic-xvectors"):
        self.processor = SpeechT5Processor.from_pretrained(path_speecht5_tts)
        self.model = SpeechT5ForTextToSpeech.from_pretrained(path_speecht5_tts)
        self.vocoder = SpeechT5HifiGan.from_pretrained(path_speecht5_hifigan)
        self.embeddings_dataset = load_dataset(path_xvectors, split='validation')

    def cuda(self):
        self.cuda = True
        self.model.cuda()
        self.vocoder.cuda()
        return self
        
    def __call__(self, text, speecher_id=0):
        inputs = self.processor(text=text, return_tensors="pt")
        speaker_embeddings = torch.tensor(self.embeddings_dataset[speecher_id]["xvector"]).unsqueeze(0)
        if self.cuda:
            speaker_embeddings = speaker_embeddings.cuda()
            inputs = inputs.to('cuda')
        speech = self.model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=self.vocoder).cpu()
        return speech.numpy(), 16000
    
    def get_mp3(self, text, speecher_id=0):
        wav, rate = self.__call__(text, speecher_id)
        # 写入mp3
        with BytesIO() as bio:
            sf.write(bio, wav, rate, format='mp3')
            # 转换为base64
            bio.seek(0)
            base64_str = base64.urlsafe_b64encode(bio.read())
        return base64_str, rate
