import chromadb 
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from rag.config import PERSIST_DIR
from rag.model_factory import load_models


def build_or_load_index(nodes = None, profile = "fast"):
    ''' 
        This function builds new INDEX if nodes(docs) provided
        Or loads already built persistent INDEX
        
        Args:
            By-Default we consider no Nodes(None) and Profile is Fast
    '''

    #We will load LLM in PIPELINE
    _ , embed_model = load_models(profile)
    
    #Set-up a ChromaDB client
    client = chromadb.PersistentClient(path = str(PERSIST_DIR))
    
    collection = client.get_or_create_collection(name = "wyrd_wiki")
    
    vector_store = ChromaVectorStore(chroma_collection= collection)
    
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    #If NODES present
    if nodes:
        print("Building new index (embedding docus)...")
        
        index = VectorStoreIndex(
            nodes, 
            storage_context=storage_context,
            embed_model = embed_model,
        )
    
    else:
        print("Loading existing INDEXs...")
        
        index = VectorStoreIndex.from_vector_store(
            vector_store= vector_store,
            embed_model = embed_model,
        )
        
    return index