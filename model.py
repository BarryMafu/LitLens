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
    
    def create_file(self, file_path: str):
        with open(file_path, 'rb') as file:
            response = self.client.files.create(
                file=file,
                purpose='assistants'
            )
        return response

if __name__ == "__main__":
    model = LanguageModel()

    from utils import *
    import prompts

    arxiv_id = "2404.13208"
    txt_path = get_content_pdf(arxiv_id)
    print(txt_path)
    with open(txt_path, 'r', encoding='utf-8') as file:
        paper_content = file.read()
    # Example usage
    prompts = prompts.keyword_extraction(paper_content)

    resp = model.get_response(prompts)
    
    
    