from pathlib import Path 

#==============PATHS==================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PERSIST_DIR = BASE_DIR / "vector_store"

PDF_PATH = DATA_DIR / "wiki.pdf"


#===============MODEL PROFILES================
MODEL_PROFILES = {
    "fast" : {
        "llm" : "phi3:mini",
        "embed" : "nomic-embed-text",
        "description" : "Fastest profile for low-ram systems"
    },
    "balanced" : {
        "llm" : "mistral:7b-instruct-q4_0",
        "emebd" : "nomic-embed-text",
        "description" : "Balanced speed and quality"
    },
    "quality" : {
        "llm" : "llama3:8b-instruct-q4_0",
        "embed" : "nomic-embed-text",
        "description" : "Best quality but slower on low-ram systems"
    }
}

DEFAULT_PROFILE = "fast"

#=================RETRIEVAL======================
CHUNK_SIZE = 750
CHUNK_OVERLAP = 120
TOP_K = 5