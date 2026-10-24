#!/usr/bin/env python3
"""
FastAPI Backend for DakshinVani — Gemma South Indian Menu Translator Agent
Run locally with:
  uvicorn server:app --reload --port 8000
"""
import json
import os
import time
from collections import defaultdict
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from agent.gemma_menu_agent import GemmaCulinaryAgent

app = FastAPI(title="DakshinVani Gemma Menu Translator API", version="1.0.0")

# CORS: restrict to known origins in production. Reads a comma-separated
# list from the ALLOWED_ORIGINS env var; defaults to localhost dev origins
# only, never a wildcard, so a stray env var can't silently reopen this.
_default_origins = "http://localhost:8000,http://127.0.0.1:8000"
ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", _default_origins).split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

agent = GemmaCulinaryAgent()
BASE_DIR = Path(__file__).resolve().parent

# Allow-list of models this server will actually call, so a client can't
# pass an arbitrary string through to the local Ollama instance.
ALLOWED_MODELS = {"gemma3:4b", "gemma2:9b"}
ALLOWED_LANGUAGES = {"hi", "mr", "fr", "ja", "de"}

# Very small in-memory rate limiter: N requests per IP per window.
# Good enough for a single-process local/demo deployment; swap for
# slowapi + Redis (or a reverse-proxy limiter) before any real production use.
RATE_LIMIT_MAX_REQUESTS = 10
RATE_LIMIT_WINDOW_SECONDS = 60
_request_log: dict = defaultdict(list)


def _check_rate_limit(client_ip: str) -> None:
    now = time.time()
    recent = [t for t in _request_log[client_ip] if now - t < RATE_LIMIT_WINDOW_SECONDS]
    if len(recent) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests. Please slow down and try again shortly.")
    recent.append(now)
    _request_log[client_ip] = recent


class TranslateRequest(BaseModel):
    dish: str
    languages: Optional[List[str]] = ["hi", "mr", "fr", "ja", "de"]
    notes: Optional[str] = ""
    model: Optional[str] = "gemma3:4b"
    use_live_ollama: Optional[bool] = True

    @field_validator("dish")
    @classmethod
    def dish_must_be_reasonable(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("dish must not be empty")
        if len(v) > 200:
            raise ValueError("dish name is too long (max 200 characters)")
        return v

    @field_validator("notes")
    @classmethod
    def notes_length(cls, v: Optional[str]) -> str:
        v = v or ""
        if len(v) > 1000:
            raise ValueError("notes are too long (max 1000 characters)")
        return v

    @field_validator("languages")
    @classmethod
    def languages_must_be_known(cls, v: Optional[List[str]]) -> List[str]:
        v = v or ["hi", "mr", "fr", "ja", "de"]
        unknown = [lang for lang in v if lang not in ALLOWED_LANGUAGES]
        if unknown:
            raise ValueError(f"unsupported language(s): {unknown}. Allowed: {sorted(ALLOWED_LANGUAGES)}")
        return v

    @field_validator("model")
    @classmethod
    def model_must_be_allowed(cls, v: Optional[str]) -> str:
        v = v or "gemma3:4b"
        if v not in ALLOWED_MODELS:
            raise ValueError(f"unsupported model: {v}. Allowed: {sorted(ALLOWED_MODELS)}")
        return v


@app.get("/api/dishes")
def list_dishes():
    return {"dishes": agent.kb.get("dishes", []), "glossary": agent.kb.get("culinary_glossary", {})}


@app.post("/api/translate")
def translate_menu_item(req: TranslateRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    _check_rate_limit(client_ip)

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
