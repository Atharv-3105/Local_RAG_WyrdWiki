import argparse
from rich import print 
from rag.config import MODEL_PROFILES, DEFAULT_PROFILE

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
    
    print("\n[bold green]LOCAL RAG SYSTEM[/bold green]")
    print(f"Using profile: [bold yellow]{args.profile}[/bold yellow]")
    
    if args.profile not in MODEL_PROFILES:
        print("[red]Invalid profile selected[/red]")
        return 
    
    print("Profile Description:", MODEL_PROFILES[args.profile]["description"])
    

if __name__ == "__main__":
    main()