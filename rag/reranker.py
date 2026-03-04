from collections import defaultdict


def rerank_and_filter(nodes, final_top_k = 5, max_per_source = 2):
    ''' 
        Re-rank nodes by similarity score and apply diversity filtering
    '''
    
    sorted_nodes = sorted(nodes, key = lambda x: x.score if x.score is not None else 0,reverse=True)
    
    selected_nodes = []
    source_counter = defaultdict(int)
    
    for node in sorted_nodes:
        source = node.metadata.get("source", "unknown")
        
        if source_counter[source] < max_per_source:
            selected_nodes.append(node)
            source_counter[source] += 1
        
        if len(selected_nodes) >= final_top_k:
            break
        
    return selected_nodes