import argparse
from rich import print 
from rag.config import MODEL_PROFILES, DEFAULT_PROFILE
from rag.ingestion import load_notion_docs, chunk_documents
from rag.pipeline import initialize_rag, query_rag

def parse_args():
    parser = argparse.ArgumentParser(
        description="Local RAG System"
    )
    
    parser.add_argument(
        "--profile",
        type = str,
        default= DEFAULT_PROFILE,
        help = f"Model profile: {list(MODEL_PROFILES.keys())}"
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    # docs = load_notion_docs()
    # nodes = chunk_documents(docs)
    
    print("\n[bold green]Initializing LOCAL RAG SYSTEM[/bold green]")
    print(f"Using profile: [bold yellow]{args.profile}[/bold yellow]")
    
    #Profile Sanity check
    if args.profile not in MODEL_PROFILES:
        print("[red]Invalid profile selected[/red]")
        return 
    
    print("Profile Description:", MODEL_PROFILES[args.profile]["description"])
    
    #Start rag
    index = initialize_rag(profile = args.profile)
    
    print(f"[bold green]System Ready.[/bold green]")
    
    while True:
        query = input("\nAsk a question (or type 'exit'):")
        
        if query.lower() == "exit":
            break
        
        result = query_rag(index, query, profile = args.profile)
        
        print("\n[bold blue]Answer:[/bold blue]")
        print(result["answer"])
        
        print(f"\n[bold yellow] Confidence: {result['confidence']}%")
        
        print("\n[bold yellow]Sources:[/bold yellow]")
        for src in result["sources"]:
            print(src)

if __name__ == "__main__":
    main()