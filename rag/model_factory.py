from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from rag.config import MODEL_PROFILES, DEFAULT_PROFILE


def load_models(profile: str = DEFAULT_PROFILE) :
    '''
        Load LLM and Embedding model based on a profile
    '''
    
    if profile not in MODEL_PROFILES:
        raise ValueError (
            f"Invalid Profile '{profile}'"
            f"Available Profiles: {list(MODEL_PROFILES.keys())}" 
        )
        
    config = MODEL_PROFILES[profile]
    
    llm = Ollama(
        model = config["llm"],
        request_timeout=300.0,
        context_window=4096,  #Use this when running on LOW-RAM system
    )
    
    embed_model = OllamaEmbedding(model_name=config["embed"])
    
    return llm, embed_model