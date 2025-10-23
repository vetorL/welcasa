# app.py  (ou api/index.py no Vercel)
from typing import Literal, List, Dict, Any
from contextlib import asynccontextmanager, contextmanager
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import atexit

# --- Postgres (Neon) ---
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from psycopg_pool import PoolClosed

# ------------- Config -------------
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Missing env var DATABASE_URL. Set your Neon connection string (with sslmode=require).")

# Enforce sslmode=require in the URL (idempotent no-op if it’s already there)
if "sslmode=" not in DATABASE_URL:
    joiner = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL = f"{DATABASE_URL}{joiner}sslmode=require"

# ------------- DB pool (serverless-friendly) -------------
# - min_size=0: no idle connections
# - max_size=1: avoid fan-out in serverless
# - open=False: don't pre-open
pool = ConnectionPool(
    DATABASE_URL,
    min_size=0,
    max_size=1,
    open=False,
)

@contextmanager
def get_conn():
    """
    Context manager that opens the pool on demand and yields a DB connection.
    Handles cold starts where the pool isn't open yet.
    """
    try:
        with pool.connection() as conn:
            yield conn
    except PoolClosed:
        # Pool isn't open in this fresh process; open it and retry once.
        pool.open()
        with pool.connection() as conn:
            yield conn

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
    # Open pool lazily and create schema if needed
    with get_conn() as conn:
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
    # Initialize schema on first cold start
    try:
        init_db()
    except Exception as e:
        print("DB init failed:", repr(e))
    try:
        yield
    finally:
        # Let process shutdown handle cleanup; keep atexit safety below.
        pass

# ------------- App -------------
app = FastAPI(
    title="welhome Properties API",
    version="0.2.2",
    lifespan=lifespan,
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
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT id, title, address, status FROM properties ORDER BY id DESC;")
            rows: List[Dict[str, Any]] = cur.fetchall()
            return rows

@app.post("/properties", response_model=PropertyOut, status_code=201, tags=["properties"])
def create_property(payload: PropertyIn):
    with get_conn() as conn:
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
    with get_conn() as conn:
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
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM properties WHERE id = %s;", (id,))
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Property not found")
            conn.commit()
            return  # 204 No Content

# ------------- Fallback para encerramento abrupto -------------
def _close_pool_on_exit():
    try:
        pool.close()
    except Exception:
        pass

atexit.register(_close_pool_on_exit)

# ------------- Execução local -------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
