from dataclasses import dataclass
from utils import *
from model import LanguageModel
from prompts import *

@dataclass
class LitLensConfig:
    """Configuration for LitLens application."""
    limit_cited: int = -1 # unlimited 
    limit_reference: int = -1 # unlimited
    limit_search: int = 10 # default to 10 results
    count_first_round = 50
    count_second_round = 10
    count_third_round = 5

class LitLens:
    def __init__(self,
        config: LitLensConfig = LitLensConfig(),
        model: LanguageModel = LanguageModel()
    ):
        self.model = model 
        self.config = config
    
