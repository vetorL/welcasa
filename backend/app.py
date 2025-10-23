# app.py  (ou api/index.py no Vercel)
from typing import Literal, List, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import atexit

# --- Postgres (Neon) ---
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

# ------------- Config -------------
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Missing env var DATABASE_URL. Set your Neon connection string (with sslmode=require).")

# Enforce sslmode=require in the URL (idempotent no-op if it’s already there)
if "sslmode=" not in DATABASE_URL:
    joiner = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL = f"{DATABASE_URL}{joiner}sslmode=require"

# ------------- DB pool (serverless-friendly) -------------
# Key settings for Vercel/Neon:
# - min_size=0: no connections kept warm between invocations
# - max_size=1: Neon free/low tiers hate fan-out from parallel lambdas
# - open=False: don't pre-open pool at import/startup
pool = ConnectionPool(
    DATABASE_URL,
    min_size=0,
    max_size=1,
    open=False,
)

# ------------- Modelos -------------
Status = Literal["active", "inactive"]

class PropertyIn(BaseModel):
    title: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    status: Status

class PropertyOut(PropertyIn):
    id: int

# ------------- DB bootstrap -------------
def init_db() -> None:
    # Lazily create a single connection via the pool when needed
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS properties (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    address TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('active','inactive'))
                );
                """
            )
            conn.commit()

# ------------- Lifespan -------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # DO NOT call pool.open() here; keep it lazy per-invocation
    # Initialize schema on first cold start (will open exactly one conn)
    try:
        init_db()
    except Exception as e:
        # Optional: print for Vercel logs
        print("DB init failed:", repr(e))
        # Don't crash health checks — continue; endpoints will still raise properly
    try:
        yield
    finally:
        # No explicit close here — serverless instances are short-lived.
        # Pool will clean up when the process ends. (We keep atexit as a safety net.)
        pass

# ------------- App -------------
app = FastAPI(
    title="welhome Properties API",
    version="0.2.1",
    lifespan=lifespan,   # <-- IMPORTANTE: registra o lifespan!
)

# CORS liberado para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste se quiser restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------- Endpoints -------------
@app.get("/health", tags=["health"])
def health():
    return {"ok": True}

@app.get("/properties", response_model=List[PropertyOut], tags=["properties"])
def list_properties():
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id, title, address, status FROM properties ORDER BY id DESC;")
            rows: List[Dict[str, Any]] = cur.fetchall()
            return rows

@app.post("/properties", response_model=PropertyOut, status_code=201, tags=["properties"])
def create_property(payload: PropertyIn):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO properties (title, address, status)
                VALUES (%s, %s, %s)
                RETURNING id, title, address, status;
                """,
                (payload.title, payload.address, payload.status),
            )
            row = cur.fetchone()
            conn.commit()
            return row

@app.put("/properties/{id}", response_model=PropertyOut, tags=["properties"])
def update_property(
    payload: PropertyIn,
    id: int = Path(..., ge=1),
):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id FROM properties WHERE id = %s;", (id,))
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Property not found")

            cur.execute(
                """
                UPDATE properties
                   SET title = %s, address = %s, status = %s
                 WHERE id = %s
             RETURNING id, title, address, status;
                """,
                (payload.title, payload.address, payload.status, id),
            )
            row = cur.fetchone()
            conn.commit()
            return row

@app.delete("/properties/{id}", status_code=204, tags=["properties"])
def delete_property(id: int = Path(..., ge=1)):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM properties WHERE id = %s;", (id,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Property not found")
            conn.commit()
            return  # 204 No Content

# ------------- Fallback para encerramento abrupto (ex.: Ctrl+C, reload, testes) -------------
def _close_pool_on_exit():
    try:
        pool.close()
    except Exception:
        pass

atexit.register(_close_pool_on_exit)

# ------------- Execução local -------------
if __name__ == "__main__":
    import uvicorn
    # Em dev com --reload, o servidor cria subprocessos; o lifespan acima cuida do ciclo de vida.
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
