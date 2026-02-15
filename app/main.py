import os
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Query
import psycopg

app = FastAPI(title="Users API", version="1.0.0")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "devdb")
DB_USER = os.getenv("DB_USER", "dev")
DB_PASSWORD = os.getenv("DB_PASSWORD", "dev123")

def get_conn():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=5,
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users")
def list_users(limit: int = Query(50, ge=1, le=500), offset: int = Query(0, ge=0)):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, first_name, last_name, email, is_active, created_at
                    FROM users
                    ORDER BY id
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset),
                )
                rows = cur.fetchall()

        users = [
            {
                "id": r[0],
                "first_name": r[1],
                "last_name": r[2],
                "email": r[3],
                "is_active": r[4],
                "created_at": r[5].isoformat() if r[5] else None,
            }
            for r in rows
        ]
        return {"count": len(users), "items": users}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"DB error: {ex}")

@app.get("/users/{user_id}")
def get_user(user_id: int):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, first_name, last_name, email, is_active, created_at
                    FROM users
                    WHERE id = %s
                    """,
                    (user_id,),
                )
                r = cur.fetchone()

        if not r:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": r[0],
            "first_name": r[1],
            "last_name": r[2],
            "email": r[3],
            "is_active": r[4],
            "created_at": r[5].isoformat() if r[5] else None,
        }
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"DB error: {ex}")
