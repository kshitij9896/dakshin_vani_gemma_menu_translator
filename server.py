#!/usr/bin/env python3
"""
FastAPI Backend for DakshinVani — Gemma South Indian Menu Translator Agent
Run locally with:
  uvicorn server:app --reload --port 8000
"""
import json
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from agent.gemma_menu_agent import GemmaCulinaryAgent

app = FastAPI(title="DakshinVani Gemma Menu Translator API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = GemmaCulinaryAgent()
BASE_DIR = Path(__file__).resolve().parent


class TranslateRequest(BaseModel):
    dish: str
    languages: Optional[List[str]] = ["hi", "mr", "fr", "ja", "de"]
    notes: Optional[str] = ""
    model: Optional[str] = "gemma3:4b"
    use_live_ollama: Optional[bool] = True


@app.get("/api/dishes")
def list_dishes():
    return {"dishes": agent.kb.get("dishes", []), "glossary": agent.kb.get("culinary_glossary", {})}


@app.post("/api/translate")
def translate_menu_item(req: TranslateRequest):
    agent.model_name = req.model or "gemma3:4b"
    return agent.translate_dish(
        dish_query=req.dish,
        target_languages=req.languages,
        custom_notes=req.notes or "",
        use_live_ollama=bool(req.use_live_ollama),
    )


@app.get("/")
def serve_ui():
    return FileResponse(BASE_DIR / "index.html")
