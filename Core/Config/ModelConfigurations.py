from transformers import pipeline
import torch
from langchain.chat_models import init_chat_model

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
    def get_hf_lang_chain_model_config():
        return init_chat_model(
            "huggingface:meta-llama/Llama-3.2-3B-Instruct",
            # model_provider="huggingface",
            temperature=0.5,
            timeout=300,
            max_tokens=25000,
        )
    
    @staticmethod
    def get_gemini_lang_chain_model_config():
        return init_chat_model(
            "gemini-2.0-flash",
            model_provider="google-genai",
            temperature=0.5,
            timeout=600,
            max_tokens=25000,
            streaming=True,
        )