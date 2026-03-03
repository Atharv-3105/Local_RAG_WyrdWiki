from rag.config import TOP_K

def get_retriever(index):
    ''' 
        This function returns retirever object
    '''
    
    retriever = index.as_retriever(
        similarity_top_k = TOP_K
    )
    
    return retriever