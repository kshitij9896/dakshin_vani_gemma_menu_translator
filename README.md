# DakshinVani (दक्षिण वाणी) — Gemma South Indian Menu Translator Agent

An open-source **3-Stage Culinary Menu Translator Agent** built with **Google Gemma** (`gemma3:4b` / `gemma2:9b` via Ollama) that translates authentic **South Indian Restaurant Dishes** into **Hindi (हिन्दी — Primary)**, **Marathi (मराठी)**, **French (Français)**, **Japanese (日本語)**, and **German (Deutsch)** without falling into the comical literal traps of generic translation tools (e.g. "Hot Lentil Bath" instead of *Bisi Bele Bath*, "Powder Crepe" instead of *Podi Dosa*).

## Prerequisites

- **Python 3.9+** (tested on Python 3.14)
- **pip** (ships with Python)
- **Ollama** — optional, only needed for live Gemma model output (see Step 4 below). Without it, the agent uses a built-in knowledge-base fallback and still works fully.

> **Windows users:** `python3` and bare `pip`/`uvicorn` commands often aren't on PATH. Use `python` instead of `python3`, and `python -m pip` / `python -m uvicorn` instead of the bare commands if you see a "not recognized" error. Both forms are shown below.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
If you get a `pip: command not recognized` error (common on Windows):
```bash
python -m pip install -r requirements.txt
```

### 2. Run the CLI Agent (Works With or Without Ollama Running)
```bash
python agent/gemma_menu_agent.py --dish "Ghee Roast Podi Masala Dosa" --langs hi,mr,fr,ja,de
```
Try a second sample dish:
```bash
python agent/gemma_menu_agent.py --dish "Mysuru Bisi Bele Bath with Kara Boondi" --langs hi,mr,fr,ja,de
```
This prints a structured JSON response with the 3-stage agent trace (`DishDeconstructor` → `CulturalBridgeMapper` → `GemmaMenuCopywriter`) and translations in all requested languages.

### 3. Run the Web App (FastAPI + index.html)
```bash
uvicorn server:app --reload --port 8000
```
If `uvicorn: command not recognized`:
```bash
python -m uvicorn server:app --reload --port 8000
```
Then open **http://localhost:8000** in your browser. The UI has three tabs: **Translator**, **Menu Card**, and **Glossary**.

### 4. Optional: Connect Live Google Gemma via Ollama
```bash
ollama pull gemma3:4b
ollama serve
```
Both the CLI and the FastAPI server will automatically call the live model at `http://localhost:11434/api/generate` when Ollama is running, and fall back to the local knowledge-base synthesis when it isn't.

## Project Structure
```
dakshin_vani_gemma_menu_translator/
├── agent/
│   └── gemma_menu_agent.py      # 3-stage translation agent (CLI + core logic)
├── data/
│   └── south_indian_culinary_kb.json   # Curated South Indian culinary knowledge base
├── index.html                   # Web UI (Translator / Menu Card / Glossary tabs)
├── server.py                    # FastAPI backend (/api/dishes, /api/translate)
├── requirements.txt
├── README.md
├── DEVRELAY_SESSION_GUIDE.md    # How to record your build session with DevRelay
└── DEV_SUBMISSION_POST.md       # Hacktoberfest DEV Challenge submission draft
```

## Record Your Agent Session with DevRelay
See [`DEVRELAY_SESSION_GUIDE.md`](./DEVRELAY_SESSION_GUIDE.md) for the exact workflow to record your build session in **Antigravity** or **Claude Code** and publish your draft to DEV using `DEV_SUBMISSION_POST.md`.

## Hosting / Deployment Notes
This project currently runs entirely locally. `server.py` calls Ollama at `localhost:11434`, so deploying online requires either hosting Ollama on a GPU-backed server or running in fallback (no-live-model) mode. `server.py` also allows all CORS origins (`allow_origins=["*"]`) by default, which is fine for local testing but should be restricted before any public deployment.

## License
MIT License — see [`LICENSE`](./LICENSE).
