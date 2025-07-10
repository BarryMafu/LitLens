# ==== LitLens ====
# model.py
#  
# author: Kai Wang (2025.7)
# Copyright: (2025) Mizu Studio

from dotenv import load_dotenv
load_dotenv("api_key.env")

import os
from openai import OpenAI
from dataclasses import dataclass

@dataclass
class ModelConfig:
    model_name: str = "doubao-seed-1-6-250615"
    base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    api_key: str = os.getenv("API_KEY")

class LanguageModel:
    def __init__(self, model_config: ModelConfig = ModelConfig()):
        self.client = OpenAI(
            base_url=model_config.base_url,
            api_key=model_config.api_key
        )
        self.model_name = model_config.model_name

    def get_response(self, prompts: list):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=prompts
        )
        return response.choices[0].message.content if response.choices else None

if __name__ == "__main__":
    model = LanguageModel()
    
    # Example usage
    prompts = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    
    response = model.get_response(prompts)
    print(response)  # Should print: "The capital of France is Paris."