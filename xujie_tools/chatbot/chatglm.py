
import json
import requests
import os
# from text_generation import Client, InferenceAPIClient
from transformers import AutoModel, AutoTokenizer


class ChatGLM():
    """ 
    https://huggingface.co/THUDM/chatglm-6b
    https://huggingface.co/THUDM/chatglm-6b-int4
    https://huggingface.co/spaces/ysharma/ChatGLM-6b_Gradio_Streaming 
    """
    def __init__(self, path_chatglm="THUDM/chatglm-6b", device='cuda'):
        self.tokenizer_glm = AutoTokenizer.from_pretrained(path_chatglm, trust_remote_code=True)
        self.model_glm = AutoModel.from_pretrained(path_chatglm, trust_remote_code=True).half().to(device)
        # self.model_glm.eval()

    def predict_glm_stream(self, input, history=[], top_p=1.0, temperature=1.0): 
        history = list(map(tuple, history))
        for response, updates in self.model_glm.stream_chat(self.tokenizer_glm, input, history, top_p=top_p, temperature=temperature):   
            yield updates 

    def __call__(self, input, history=[], top_p=1.0, temperature=1.0):
        response, history = self.model_glm.chat(self.tokenizer_glm, input, history, top_p=top_p, temperature=temperature)
        return response, history
