from rag.ingestion import load_notion_docs, chunk_documents
from rag.vector_store import build_or_load_index
# from rag.retriever import get_retriever
from rag.generator import generate_answer
from rag.reranker import rerank_and_filter

from rag.model_factory import load_models
import chromadb
from rag.config import PERSIST_DIR

def initialize_rag(profile = "fast"):
    ''' 
        This function initialize's the system:
            1- First it tries loading existing index
            2- If empty index, build's new one
    '''
    
    client = chromadb.PersistentClient(path = str(PERSIST_DIR))
    collection_name = "wyrd_wiki"
    
    try:
        collection = client.get_collection(collection_name)
        count = collection.count()
    except:
        count = 0
    
    if count == 0:
        print("No existing embeddings found. Building new index...")
        
        documents = load_notion_docs()
        print(f"Loaded {len(documents)} documents")
        
        nodes = chunk_documents(documents)
        print(f"Created {len(nodes)} chunks")
        
        index = build_or_load_index(nodes = nodes, profile = profile)
    
    else:
        print(f"Loading existing index ({count} chunks found)....")
        index = build_or_load_index(profile=profile)
    
    return index
    

def query_rag(index, query: str, profile = "fast"):
    
    llm, _ = load_models(profile)
    
    #Retrieve more node
    retriever = index.as_retriever(similarity_top_k=10)
    nodes = retriever.retrieve(query)
    
    #Add re-ranking and diversity filter
    filtered_nodes = rerank_and_filter(
        nodes, 
        final_top_k=5,
        max_per_source=2
    )

    result = generate_answer(llm, filtered_nodes, query)
    
    return result