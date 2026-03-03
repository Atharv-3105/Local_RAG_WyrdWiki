import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

from rag.config import PERSIST_DIR


def initialize_vector_store(collection_name: str = "wyrd.wiki"):
    ''' 
        Initialize persistent ChromaDB vector store
    '''
    
    #Initialize the chromaDB client
    client = chromadb.PersistentClient(path = str(PERSIST_DIR))
    
    collection = client.get_or_create_collection(
        name = collection_name
    )
    
    vector_store = ChromaVectorStore(
        chroma_collection= collection
    )
    
    storage_context  = StorageContext.from_defaults(
        vector_store = vector_store
    )
    
    return vector_store, storage_context
    
    