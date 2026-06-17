from transformers import pipeline
import torch

class ModelConfigurations:

    @staticmethod
    def get_model_config():
        model_id = "meta-llama/Llama-3.2-3B"
        pipe = pipeline(
            "text-generation",
            model=model_id,
            torch_dtype=torch.bfloat16,
            device_map="cpu"
        )
        return pipe

    @staticmethod
    def get_transformer_config():
        return {
            "do_sample": True,
            "temperature": 0.7,
            "max_new_tokens": 1000,
            "top_k": 50,
            "top_p": 0.95
        }