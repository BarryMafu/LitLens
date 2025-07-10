# ==== LitLens ====
# utils.py
#  
# author: Kai Wang (2025.7)
# Copyright: (2025) Mizu Studio

import requests
from bs4 import BeautifulSoup

RESPONSE_CODE_OK = 200

class LitlensException(Exception):
    """Custom exception for LitLens errors."""
    pass

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
    """Trim the version number from the arXiv ID."""
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

if __name__ == "__main__":
    title = "Attention Is All"
    arxiv_id = get_arxiv_id_by_title(title)
    for t in get_citation(arxiv_id):
        print(t)
