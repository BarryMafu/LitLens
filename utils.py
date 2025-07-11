# ==== LitLens ====
# utils.py
#  
# author: Kai Wang (2025.7)
# Copyright: (2025) Mizu Studio

import requests
from bs4 import BeautifulSoup
import os
import tarfile
import pdfplumber
import fitz  # PyMuPDF

RESPONSE_CODE_OK = 200

class LitlensException(Exception):
    """Custom exception for LitLens errors."""
    pass

def is_valid_arxiv_id(arxiv_id: str) -> bool:
    # TODO: use Regex to validate arXiv ID format
    return True

def get_basic_info(arxiv_id: str):
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != RESPONSE_CODE_OK:
        raise LitlensException(f"Failed to fetch data from arXiv: {response.status_code}")

    # Parse the response using 
    soup = BeautifulSoup(response.content, 'xml')
    entry = soup.find('entry')
    ret = {
        "arxiv_id": entry.id.text.split('/')[-1] if entry.id else "",
        "title": entry.title.text if entry.title else "",
        # "authors": [author.name for author in entry.find_all('author')],
        "summary": entry.summary.text.replace("\n", " ") if entry.summary else "",
        "link": entry.id.text if entry.id else "",
        "publish_time": entry.published.text if entry.published else "",
    }
    return ret

def search_arxiv(query: str, max_results: int = 10):
    url = "http://export.arxiv.org/api/query"
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results
    }
    response = requests.get(url, params=params)
    print(response.content)
    
    # Check if the request was successful
    if response.status_code != RESPONSE_CODE_OK:
        raise LitlensException(f"Failed to fetch data from arXiv: {response.status_code}")

    # Parse the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'xml')
    entries = soup.find_all('entry')
    
    results = []
    for entry in entries:
        results.append({
            "arxiv_id": entry.id.text.split('/')[-1] if entry.id else "",
            "title": entry.title.text if entry.title else "",
            "summary": entry.summary.text.replace("\n", " ") if entry.summary else "",
            "link": entry.id.text if entry.id else "",
            "publish_time": entry.published.text if entry.published else "",
        })
    
    return results

def get_arxiv_id_by_title(title: str):
    query = f'ti:"{title}"'
    results = search_arxiv(query, max_results=1)
    if results:
        return results[0]['arxiv_id']
    raise LitlensException(f"No results found for title: {title}")
    
def trim_version(arxiv_id: str):
    if 'v' in arxiv_id:
        return arxiv_id.split('v')[0]
    return arxiv_id

def get_citation(arxiv_id: str):
    arxiv_id = trim_version(arxiv_id) # no "v" allowed in semantic API
    url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}/citations"
    response = requests.get(url)

    if response.status_code != RESPONSE_CODE_OK:
        raise LitlensException(f"Failed to fetch citations: {response.status_code}")
    
    data = response.json()
    # print(data['data'])
    titles = [
        paper['citingPaper']['title'] for paper in data['data']
    ]
    return titles

def get_reference(arxiv_id: str):
    arxiv_id = trim_version(arxiv_id) # no "v" allowed in semantic API
    url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}/references"
    response = requests.get(url)

    if response.status_code != RESPONSE_CODE_OK:
        raise LitlensException(f"Failed to fetch references: {response.status_code}")
    
    data = response.json()
    titles = [
        paper['citedPaper']['title'] for paper in data['data']
    ]
    return titles

def get_content_tex(arxiv_id: str):
    # Download 
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    response = requests.get(url, stream=True)

    if response.status_code != RESPONSE_CODE_OK:
        raise LitlensException(f"Failed to fetch content: {response.status_code}")
    
    # Create directory
    cwd = os.getcwd()
    tar_path = os.path.join(cwd, f"src/tar/{arxiv_id}.tar.gz")
    tex_path = os.path.join(cwd, f"src/tex/{arxiv_id}.tex")
    
    # Save .tar.gz file
    with open(tar_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    # 
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(tex_path)

def get_content_pdf(arxiv_id: str):
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    response = requests.get(url, stream=True)

    if response.status_code != RESPONSE_CODE_OK:
        raise LitlensException(f"Failed to fetch PDF content: {response.status_code}")
    
    # Create directory
    cwd = os.getcwd()
    pdf_path = os.path.join(cwd, f"src/pdf/{arxiv_id}.pdf")
    
    # Save PDF file
    with open(pdf_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    
    txt_path = os.path.join(cwd, f"src/txt/{arxiv_id}.txt")
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(text)
    return txt_path

if __name__ == "__main__":
    arxiv_id = "2404.13208"
    print(get_content_pdf(arxiv_id))

# https://api.semanticscholar.org/graph/v1/paper/arXiv:1706.03762/references