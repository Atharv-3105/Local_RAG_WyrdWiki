from pathlib import Path
from bs4 import BeautifulSoup
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

from rag.config import NOTION_EXPORT_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def extract_text_from_html(file_path : Path):
    ''' 
        Parse and Extract clean text from notion-exported htmls
    '''
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        
    #Remove scripts & styles
    for tag in soup(["script", "style"]):
        tag.decompose()
        
    text = soup.get_text(separator="\n")
    
    return text.strip()


def load_notion_docs():
    ''' 
        Recursively load all HTML files from Notion export.
        Returns a list of LLAMAINDEX Documnets
    '''
    
    documents = []
    
    #Recursively visit all the sub-pages in the Notion-Wiki Page
    html_files = list(NOTION_EXPORT_DIR.rglob("*.html"))
    
    for file_path in html_files:
        
        text = extract_text_from_html(file_path)
        
        if not text:
            continue
        
        documents.append(
            Document(
                text = text,
                metadata = {
                    "source": file_path.name,
                    "relative_path": str(file_path.relative_to(NOTION_EXPORT_DIR)),
                }
            )
        )
        
    return documents


def chunk_documents(documents):
    ''' 
        Split the Parsed documents into CHUNKS with overlap.
    '''
    
    splitter = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap= CHUNK_OVERLAP
    )
    
    nodes = splitter.get_nodes_from_documents(documents)
    
    return nodes