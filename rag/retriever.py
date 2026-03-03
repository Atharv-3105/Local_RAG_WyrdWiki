from rag.config import TOP_K

def retrieve_with_scores(index, query:str):
    ''' 
        Function to retrieve NODES along with SIMILARITY SCORES
    '''
    
    retriever = index.as_retriever(
        similarity_top_k = TOP_K
    )
    
    nodes = retriever.retrieve(query)
    return nodes