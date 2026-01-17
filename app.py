import json
import os
import random
import time
from datetime import date
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

QUOTES_PATH = os.getenv("QUOTES_PATH", "/data/quotes.json")
app = FastAPI(title="Logos")

def load_quotes():
    with open(QUOTES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    quotes = []
    for q in data:
        text = (q.get("text") or "").strip()
        if not text:
            continue
        quotes.append({
            "text": text,
            "author": (q.get("author") or "").strip(),
            "tags": q.get("tags") or []
        })
    return quotes

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/quote")
def quote(
    tag: str | None = Query(default=None),
    daily: bool = Query(default=False)
):
    quotes = load_quotes()
    if tag:
        quotes = [q for q in quotes if tag in q.get("tags", [])]

    if not quotes:
        return JSONResponse(status_code=404, content={"error": "No quotes found", "tag": tag})

    if daily:
        seed = f"{date.today().isoformat()}::{tag or ''}"
        rnd = random.Random(seed)
        q = rnd.choice(quotes)
    else:
        q = random.choice(quotes)

    author_line = f"— {q['author']}" if q["author"] else ""

    return {
        "text": q["text"],
        "author": q["author"],
        "authorLine": author_line,
        "tags": q["tags"],
        "updatedAt": int(time.time())
    }
