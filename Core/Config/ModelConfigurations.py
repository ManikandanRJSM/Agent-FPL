from transformers import pipeline
import torch
from langchain.chat_models import init_chat_model
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os

class ModelConfigurations:

    @staticmethod
    def get_model_config() -> object:
        model_id = "meta-llama/Llama-3.2-3B"
        pipe = pipeline(
            "text-generation",
            model=model_id,
            torch_dtype=torch.bfloat16,
            device_map="cpu"
        )
        return pipe

    @staticmethod
    def get_transformer_config() -> dict:
        return {
            "do_sample": True,
            "temperature": 0.7,
            "max_new_tokens": 1000,
            "top_k": 50,
            "top_p": 0.95
        }
    
    @staticmethod
    def get_hf_lang_chain_model_config(): # Runs in Hugginface inference
        llm = HuggingFaceEndpoint(
            repo_id="Qwen/Qwen2.5-7B-Instruct",
            temperature=0.5,
            max_new_tokens=2048,
            timeout=300,
        )
        return ChatHuggingFace(llm=llm)
    

    def get_hf_local_lang_chain_model_config():
        return init_chat_model(
            "huggingface:Qwen/Qwen2.5-7B-Instruct",
            temperature=0.5,
            timeout=300,
            max_tokens=2048,
        )