"""API simples do Dashboard — apenas 2 endpoints."""

import sqlite3
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "restaurante.db")

try:
    import redis
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    r.ping()
    REDIS = True
except Exception:
    r = None
    REDIS = False

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def query(cache_key: str, sql: str):
    if REDIS and r:
        cached = r.get(cache_key)
        if cached:
            return {"data": json.loads(cached), "cache": "HIT"}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = [dict(row) for row in conn.execute(sql).fetchall()]
    conn.close()

    if REDIS and r:
        r.setex(cache_key, 60, json.dumps(rows))
    return {"data": rows, "cache": "MISS"}


@app.get("/api/top-pratos")
def top_pratos():
    return query("dash:top", """
        SELECT prato, SUM(quantidade) as quantidade, ROUND(SUM(valor_total),2) as receita
        FROM vendas GROUP BY prato ORDER BY quantidade DESC
    """)


@app.get("/api/sexta-noite")
def sexta_noite():
    return query("dash:sexta", """
        SELECT prato, SUM(quantidade) as quantidade, ROUND(SUM(valor_total),2) as receita
        FROM vendas
        WHERE CAST(strftime('%w', data_hora) AS INTEGER) = 5
          AND CAST(strftime('%H', data_hora) AS INTEGER) >= 18
        GROUP BY prato ORDER BY quantidade DESC
    """)


# Serve frontend
DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST, "assets")), name="assets")

    @app.get("/{path:path}")
    async def spa(path: str):
        f = os.path.join(DIST, path)
        return FileResponse(f if os.path.isfile(f) else os.path.join(DIST, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=True)
