from rag.retriever import retrieve_with_scores

MIN_SIMILARITY_THRESHOLD = 0.35

def build_prompt(context: str, query: str):
    ''' 
        Strict grounded prompt to reduce hallucination
    '''
    
    return f"""
You are an internal assistant for Wyrd Media Labs.

You must answer ONLY using the provided context.
If the answer is not explicitly found in the context,
reply with: "Not found in company wiki."

Do not add external knowledge.

------------------
Context:
{context}
------------------

Question:
{query}

Answer:
"""


def generate_answer(llm, nodes, query: str):
    
    #Retrieve relevant nodes
    # nodes = retrieve_with_scores(index, query)
    
    if not nodes:
        return {
            "answer": "Not found in company wiki.",
            "sources": [],
            "confidence":0.0
        }
    
    #Extract Similarity Scores
    scores = [node.score for node in nodes if node.score is not None]
    
    if not scores:
        confidence = 0.0
    else:
        confidence = max(scores)   
        
    #Filter score above the Threshold only
    if confidence < MIN_SIMILARITY_THRESHOLD:
        return {
            "answer" : "Not found in company wiki",
            "sources": [],
            "confidence": round(confidence * 100, 2)
        }
    
    
        
    #Build context string 
    context = "\n\n".join([node.text for node in nodes])
    
    prompt = build_prompt(context, query)
    
    response = llm.complete(prompt)
    
    return {
        "answer":response.text.strip(),
        "sources": [node.metadata for node in nodes],
        "confidence": round(confidence * 100, 2)
    }