from typing import Literal, Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sqlite3
import os

# ------------- Configuração básica -------------
DB_PATH = os.getenv("DB_PATH", "properties.db")

app = FastAPI(title="Welcasa Properties API", version="0.1.0")

# Liberar o frontend (ajuste origins se quiser restringir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # troque por ["http://localhost:5173"] etc., se quiser
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------- Modelos -------------
Status = Literal["active", "inactive"]

class PropertyIn(BaseModel):
    title: str = Field(..., min_length=1)
    address: str = Field(..., min_length=1)
    status: Status

class PropertyOut(PropertyIn):
    id: int

# ------------- Banco de dados (sqlite3 puro) -------------
def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = connect_db()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                address TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('active','inactive'))
            );
            """
        )
        conn.commit()
    finally:
        conn.close()

@app.on_event("startup")
def _startup():
    init_db()

def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {"id": row["id"], "title": row["title"], "address": row["address"], "status": row["status"]}

# ------------- Endpoints mínimos -------------
@app.get("/", tags=["health"])
def health():
    return {"ok": True}

@app.get("/properties", response_model=List[PropertyOut], tags=["properties"])
def list_properties():
    conn = connect_db()
    try:
        cur = conn.execute("SELECT id, title, address, status FROM properties ORDER BY id DESC;")
        rows = cur.fetchall()
        return [row_to_dict(r) for r in rows]
    finally:
        conn.close()

@app.post("/properties", response_model=PropertyOut, status_code=201, tags=["properties"])
def create_property(payload: PropertyIn):
    conn = connect_db()
    try:
        cur = conn.execute(
            "INSERT INTO properties (title, address, status) VALUES (?, ?, ?);",
            (payload.title, payload.address, payload.status),
        )
        conn.commit()
        new_id = cur.lastrowid
        return {"id": new_id, **payload.model_dump()}
    finally:
        conn.close()

@app.put("/properties/{id}", response_model=PropertyOut, tags=["properties"])
def update_property(
    payload: PropertyIn,
    id: int = Path(..., ge=1),
):
    conn = connect_db()
    try:
        # Verifica existência
        cur = conn.execute("SELECT id FROM properties WHERE id = ?;", (id,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Property not found")

        conn.execute(
            "UPDATE properties SET title = ?, address = ?, status = ? WHERE id = ?;",
            (payload.title, payload.address, payload.status, id),
        )
        conn.commit()
        return {"id": id, **payload.model_dump()}
    finally:
        conn.close()

@app.delete("/properties/{id}", status_code=204, tags=["properties"])
def delete_property(id: int = Path(..., ge=1)):
    conn = connect_db()
    try:
        cur = conn.execute("DELETE FROM properties WHERE id = ?;", (id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Property not found")
        return  # 204 No Content
    finally:
        conn.close()

# ------------- Execução local -------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
