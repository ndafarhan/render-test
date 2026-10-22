import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="render-test")


class ItemIn(BaseModel):
    name: str
    description: str | None = None


class Item(ItemIn):
    id: int


# In-memory storage; data resets on every restart.
items: dict[int, Item] = {}
next_id = 1


@app.get("/")
async def root():
    return {"message": "Hello from render-test"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
