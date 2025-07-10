# ==== LitLens ====
# main.py
#  
# author: Kai Wang (2025.7)
# Copyright: (2025) Mizu Studio

from dataclasses import dataclass
from utils import *
from model import LanguageModel
import prompts as pr

@dataclass
class LitLensConfig:
    """Configuration for LitLens application."""
    limit_cited: int = -1 # unlimited 
    limit_reference: int = -1 # unlimited
    limit_search: int = 10 # default to 10 results
    count_first_round: int = 50
    count_second_round: int = 10
    count_third_round: int = 5
    verbose: bool = True # Whether to print debug information

class LitLens:
    def __init__(self,
        config: LitLensConfig = LitLensConfig(),
        model: LanguageModel = LanguageModel()
    ):
        self.model = model 
        self.config = config

    def get_paper_content(self, arxiv_id: str):
        if self.config.verbose:
            print(f"Fetching content ...")

        txt_path = get_content_pdf(arxiv_id)
        with open(txt_path, 'r', encoding='utf-8') as file:
            paper_content = file.read()
        return paper_content
    
    def extract_keywords_model(self, paper_content):
        if self.config.verbose:
            print("Extracting keywords from paper content...")
        ek_prompts = pr.keyword_extraction(paper_content)
        keywords = self.model.get_response(ek_prompts)
        return keywords
    
    def get_all_papers(self, arxiv_id: str, paper_content: str):
        """Get all papers related to the given arXiv ID."""
        if self.config.verbose:
            print(f"Fetching citing papers ...")
        cited = get_citation(arxiv_id)
        if self.config.verbose:
            print(f"Fetching reference papers ...")
        reference = get_reference(arxiv_id)
        if self.config.limit_cited > 0:
            cited = cited[:self.config.limit_cited] # TODO: Maybe another way
        if self.config.limit_reference > 0:
            reference = reference[:self.config.limit_reference] # TODO: Maybe another way

        keywords = self.extract_keywords_model(paper_content)
        if self.config.verbose:
            print(f"Fetching relative papers with keywords: {keywords}")
        search = [paper['title'] for paper in search_arxiv(keywords, self.config.limit_search)]
        return {
            "cited": cited,
            "reference": reference,
            "search": search
        }
    
    def first_round(self, papers, paper_content):
        """Select relevant papers from the first round."""
        if self.config.verbose:
            print(f"Selecting papers... (Round 1 / 3)")
        fr_prompts = pr.first_round(papers, self.config.count_first_round, paper_content)
        response = self.model.get_response(fr_prompts)
        return response.splitlines() if response else []
    
if __name__ == "__main__":
    arxiv_id = "2404.13208"
    litlens = LitLens()
    paper_content = litlens.get_paper_content(arxiv_id)
    paper_titles = litlens.get_all_papers(arxiv_id, paper_content)
    first_round_papers = litlens.first_round(paper_titles, paper_content)
    print("First Round Papers:")
    for title in first_round_papers:
        print("  - ", title)
    