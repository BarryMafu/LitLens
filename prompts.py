# ==== LitLens ====
# prompt.py
#  
# author: Kai Wang (2025.7)
# Copyright: (2025) Mizu Studio

def keyword_extraction(paper_content):
    return [
        {
            "role": "system",
            "content": """
You are a helpful assistant that extracts keywords from academic papers. You will be required to extract a few keywords from the provided paper content. The keywords should be relevant and concise, capturing the main themes or topics of the paper, since we are using the keywords to search for related papers.

Your answer should be a list of 1~2 keywords, each keyword should be a single word or a short phrase, and they should be separated by commas. Do not include any additional text or explanations in your response. Please do not include any special characters or punctuation in the keywords and ignore keywords with low relevance.

Example:
machine learning, natural language processing
"""
        },
        {
            "role": "user",
            "content": f"Extract a few keywords from the following paper: {paper_content}"
        },
    ]

def first_round(papers, limit, paper_content):
    cited_papers = "\n".join(papers['cited']) if papers['cited'] else "No cited papers."
    reference_papers = "\n".join(papers['reference']) if papers['reference'] else "No reference papers."
    search_papers = "\n".join(papers['search']) if papers['search'] else "No search papers."
    return [
        {
            "role": "system",
            "content": f"""
You are a helpful assistant that select relevant papers from a list of academic papers. You will be provided with a list of paper titles only. Your task is to select the most relevant papers based on the given content.

You will be provided with (1) first, the content of the original paper, and (2) a list of paper titles. You should select the most relevant papers from the list based on the content provided.

You are required to select no more than (<=) {limit} papers from the provided list. (If the list contains fewer than {limit} papers, select all of them.) The selected papers should be the most relevant to the content provided.

Your answer should be a list of paper titles, each title should be a single line, and they should be separated by new lines. Do not include any additional text or explanations in your response.

Example:
Attention is All You Need
Transformers for Natural Language Processing
"""
        },
        {
            "role": "user",
            "content": f"This is the content of the original paper {paper_content}"
        },
        {
            "role": "user",
            "content": f"""
Here is the list of paper titles, which consist of 3 parts:
1. Cited papers: 
{cited_papers}
2. Reference papers: 
{reference_papers}
3. Search papers: 
{search_papers}

Now you need to select exactly {limit} papers from the above list based on the content provided, excluding the original paper. Ordering from high relevance to low relevance.
"""
        }
    ]

def second_round(titles, abstracts, limit, paper_content):
    prompt_input = "\n".join([f"Title: {title}\nAbstract: {abstract}" for title, abstract in zip(titles, abstracts) if abstract])
    return [
        {
            "role": "system",
            "content": f"""
You are a helpful assistant that select relevant papers from a list of academic papers. You will be provided with a list of paper titles only. Your task is to select the most relevant papers based on the given content.

You will be provided with (1) first, the content of the original paper, and (2) a list of papers with both title and abstract. You should select the most relevant papers from the list based on the content provided.

You are required to select no more than (<=) {limit} papers from the provided list. (If the list contains fewer than {limit} papers, select all of them.) The selected papers should be the most relevant to the content provided.

Your answer should be a list of paper titles, each title should be a single line, and they should be separated by new lines. Do not include any additional text or explanations in your response.

Example:
Attention is All You Need
Transformers for Natural Language Processing
"""
        },
        {
            "role": "user",
            "content": f"This is the content of the original paper {paper_content}"
        },
        {
            "role": "user",
            "content": f"""
Here is the list of papers with both title and abstract:
{prompt_input}

Now you need to select EXACTLY {limit} papers from the above list based on the content provided, excluding the original paper. Ordering from high relevance to low relevance.
"""
        }
    ]

# def third_round(titles, contents, limit, paper_content):
#     prompt_input = "\n".join([f"Title: {title}\nContent: {content}" for title, content in zip(titles, contents) if content])
#     return [
#         {
#             "role": "system",
#             "content": f"""
# You are a helpful assistant that select relevant papers from a list of academic papers. You will be provided with a list of paper titles only. Your task is to select the most relevant papers based on the given content.

# You will be provided with (1) first, the content of the original paper, and (2) a list of papers with both title and content. You should select the most relevant papers from the list based on the content provided.

# You are required to select no more than (<=) {limit} papers from the provided list. (If the list contains fewer than {limit} papers, select all of them.) The selected papers should be the most relevant to the content provided and ranked from higher relationship to lower.

# Your answer should be a list of paper titles, each title should be a single line, followed by your reason to choose the paper.

# Example:
# Attention is All You Need [Reason:] <your reason here>
# Transformers for Natural Language Processing [Reason:] <your reason here>
# """
#         },
#         {
#             "role": "user",
#             "content": f"This is the content of the original paper {paper_content}"
#         },
#         {
#             "role": "user",
#             "content": f"""
# Here is the list of papers with both title and content:
# {prompt_input}
# """
#         }
#     ]