# 🧠 Local RAG System — Wyrd Company Wiki

A fully local Retrieval-Augmented Generation (RAG) system that answers questions about the Wyrd Company Wiki.

No API keys.  
No per-query cost.  
Runs completely offline using local LLMs via Ollama.

---

## 🚀 Objective

&gt; **"We have documents. We have questions. A human reads both and types replies. That doesn't scale. Fix it — locally."**

This project builds a production-style Local RAG pipeline that:

- Ingests a Notion-exported company wiki
- Embeds documents locally
- Stores embeddings persistently
- Retrieves relevant context
- Generates grounded answers
- Displays confidence and sources
- Runs fully offline

---

## 🏗️ Architecture

```
Notion Export (HTML)
        ↓
Document Loader
        ↓
Chunking (Smart Overlap)
        ↓
Local Embeddings (nomic-embed-text via Ollama)
        ↓
ChromaDB (Persistent Vector Store)
        ↓
Semantic Retrieval (Top-K)
        ↓
Re-Ranking + Diversity Filtering
        ↓
Grounded Prompt
        ↓
Local LLM (phi3 / qwen2 via Ollama)
        ↓
Answer + Confidence + Sources
        ↓
Gradio UI
```

---


---

## 🧩 Core Components

### 1️⃣ Ingestion Layer

- Parses exported Notion HTML files
- Extracts clean text using BeautifulSoup
- Preserves metadata (source filename, relative path)

**Why HTML instead of PDF?**

- The Notion export only included the main page in PDF, with hyperlinks to subpages.
- The HTML export preserves all subpages — enabling full document ingestion.

### 2️⃣ Chunking Strategy

- **Chunk size:** ~750 characters
- **Overlap:** ~120 characters

Preserves semantic continuity and avoids context fragmentation. Smaller chunks were chosen due to CPU constraints for generation.

### 3️⃣ Embedding Model (Local)

- **Model:** `nomic-embed-text` (via Ollama)

**Why:**
- Fully local
- Good semantic quality
- Lightweight
- No API cost

### 4️⃣ Vector Database

- **ChromaDB** (Persistent Mode)
- Stored locally in `/vector_store`
- No external services
- Fast startup after first embedding
- Zero per-query cost

### 5️⃣ LLM (Generation Layer)

**Model profiles:**

| Profile  | Model                          | Use Case           |
|----------|--------------------------------|--------------------|
| `fast`   | `phi3:mini`                    | Low RAM systems    |
| `balanced` | `mistral:7b-instruct-q4_0`   | General use        |
| `quality` | `llama3:8b-instruct-q4_0`     | Best quality       |

All models:
- Run locally via Ollama
- CPU inference
- No external API calls

### 6️⃣ Retrieval Strategy

**Semantic Retrieval:**
- Top 10 candidates retrieved based on cosine similarity

**Re-Ranking & Diversity Filtering:**
- Sort by similarity score
- Maximum 1–2 chunks per source page
- Final Top-K = 3 (hardware-aware tuning)

This prevents:
- Redundant chunks
- Single-page dominance
- Context bloating

### 7️⃣ Confidence Scoring

Confidence is calculated as:

> **Max similarity score among retrieved chunks**

If confidence < threshold (0.35):
- System returns: *"Not found in company wiki."*

This prevents hallucinations.

### 8️⃣ Grounded Prompting

Strict system instruction:
- Answer ONLY from provided context
- Do not fabricate
- Return "Not found" if missing

This ensures answer reliability.

---

## 🖥️ UI Layer

Built with **Gradio**.

**Features:**
- Model profile selection
- Question input
- Answer output
- Confidence display
- Source attribution
- Latency tracking

---

## 🐛 Bugs Encountered & Fixes

### 1️⃣ Notion PDF Export Issue

**Problem:**  
PDF export only contained main page with hyperlinks.

**Fix:**  
Used HTML export to ingest all subpages.

### 2️⃣ HTTP Timeout Errors

```
httpx.ReadTimeout
```

**Cause**:
CPU inference slow due to large prompt context.

**Fixes:**

- Increased Ollama timeout

- Reduced context length (1000–1500 chars)

- Reduced Top-K retrieval

- Smaller model profile

### 3️⃣ **Similarity Threshold Too Aggressive**

Initially set threshold to 0.60.

Observed real embedding similarity scores ~0.40–0.50.

**Fix:**
Lowered threshold to 0.35 and switched to max-score logic.

---

## ▶️ How To Run

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```
>**Note** Ensure Ollama is installed:

### 2️⃣ Pull Required Models

```bash
ollama pull qwen2:1.5b
ollama pull nomic-embed-text
```

### 3️⃣ Build Index (First Run)
```python
python cli.py --profile fast
```

**This will:**

-  Parse wiki

- Chunk documents

- Embed

- Store in Chroma

### 4️⃣ Launch Gradio UI
```python
python app.py

Open:

http://127.0.0.1:7860
```

---

## 📁 Project Structure

```
local_rag/
│
├── rag/
│   ├── config.py
│   ├── ingestion.py
│   ├── chunking.py
│   ├── vector_store.py
│   ├── generator.py
│   ├── pipeline.py
│   ├── reranker.py
│   └── model_factory.py
│
├── data/
│   └── notion_export/
│
├── vector_store/
│
├── cli.py
├── app.py
└── README.md
```
---

## 🏁 Final Result

**This project delivers:**

- Fully local RAG

- Zero API cost

- Persistent vector storage

- Retrieval re-ranking

- Confidence scoring

- Grounded answers

- Clean UI

- Hardware-aware optimization
