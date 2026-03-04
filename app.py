import time 
import gradio as gr 

from rag.pipeline import initialize_rag, query_rag
from rag.config import MODEL_PROFILES


#Load Index once at startup
print("Loading index....")
index = initialize_rag(profile = "fast")
print("System ready.")

def ask_question(question, profile):
    if not question.strip():
        return "Please enter a question.", "", ""
    
    start_time =time.time()
    
    result = query_rag(index, question, profile = profile)
    
    end_time = time.time()
    
    answer = result["answer"]
    confidence = f"{result['confidence']}%"
    latency = f"{round(end_time - start_time, 2)} seconds"
    
    #Format the Sources
    sources = ""
    for src in result["sources"]:
        sources += f"- {src.get('source', 'Unknown')}\n"
        
    return answer, confidence, f"{sources}\nLatency: {latency}"


with gr.Blocks(title = "Local RAG - Wyrd Wiki") as demo:
    
    gr.Markdown("# Local RAG System")
    gr.Markdown("Ask questions about the Wyrd Company Wiki (Fully Local, No API)")
    
    with gr.Row():
        profile_dropdown = gr.Dropdown(
            choices = list(MODEL_PROFILES.keys()),
            value = "fast",
            label = "Model Profile"
        )
    
    question_input = gr.Textbox(
        label = "Ask a question",
        placeholder= "What is this company?",
        lines = 2
    )
    
    ask_button = gr.Button("Ask")
    
    answer_output = gr.Textbox(label = "Answer")
    confidence_output = gr.Textbox(label = "Confidence")
    sources_output = gr.Textbox(label = "Sources & Latency")
    
    ask_button.click(
        ask_question,
        inputs = [question_input, profile_dropdown],
        outputs = [answer_output, confidence_output, sources_output]
    )
    

if __name__ == "__main__":
    demo.launch()