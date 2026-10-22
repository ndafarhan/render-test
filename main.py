import os
from contextlib import asynccontextmanager

from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from src import db
from src.init_db import ensure_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.open_pool()
    await ensure_schema()
    yield
    await db.close_pool()


app = FastAPI(title="render-test", lifespan=lifespan)


class ItemIn(BaseModel):
    name: str
    description: str | None = None


class Item(ItemIn):
    id: int


class Customer(BaseModel):
    customer_id: int
    name: str
    created_at: datetime
    updated_at: datetime


# In-memory storage; data resets on every restart.
items: dict[int, Item] = {}
next_id = 1


@app.get("/")
async def root():
    return {"message": "Hello from render-test"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/health/db")
async def health_db():
    try:
        await db.ping()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database unavailable: {exc}")
    return {"status": "ok"}


@app.get("/get_customer_data", response_model=list[Customer])
async def get_customer_data(conn: db.AsyncConnection = Depends(db.get_conn)):
    cur = await conn.execute(
        "SELECT customer_id, name, created_at, updated_at FROM customer ORDER BY customer_id"
    )
    return await cur.fetchall()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
