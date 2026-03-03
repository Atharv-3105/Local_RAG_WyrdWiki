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


def generate_answer(llm, retriever, query: str):
    
    #Retrieve relevant nodes
    nodes = retriever.retrieve(query)
    
    if not nodes:
        return {
            "answer": "Not found in company wiki.",
            "sources": [],
        }
        
    #Build context string 
    context = "\n\n".join([node.text for node in nodes])
    
    prompt = build_prompt(context, query)
    
    response = llm.complete(prompt)
    
    return {
        "answer":response.text.strip(),
        "sources": [node.metadata for node in nodes]
    }