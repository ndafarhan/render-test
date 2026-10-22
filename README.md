# render-test

Service FastAPI sederhana dengan CRUD item (in-memory).

## Jalankan lokal

```bash
uv sync
cp .env.example .env   # isi DATABASE_URL dari dashboard Neon
uv run --env-file .env main.py
```

## Database (Neon Postgres)

Koneksi ada di `src/db.py` (psycopg 3 + connection pool async). Gunakan
connection string **pooled** dari Neon (host `...-pooler...`) dengan
`sslmode=require`. Dependency `db.get_conn` bisa dipakai di endpoint:

```python
from fastapi import Depends
from src import db

@app.get("/now")
async def now(conn=Depends(db.get_conn)):
    cur = await conn.execute("SELECT now() AS now")
    return await cur.fetchone()
```

Buka http://localhost:8000/docs untuk Swagger UI.

## Endpoint

| Method | Path          | Keterangan        |
|--------|---------------|-------------------|
| GET    | `/`           | Pesan sambutan    |
| GET    | `/health`     | Health check      |
| GET    | `/health/db`  | Cek koneksi DB    |
| GET    | `/get_customer_data` | Daftar customer |
| GET    | `/items`      | Daftar item       |
| GET    | `/items/{id}` | Detail item       |
| POST   | `/items`      | Buat item         |
| PUT    | `/items/{id}` | Ubah item         |
| DELETE | `/items/{id}` | Hapus item        |

## Deploy ke Render

- Build command: `pip install uv && uv sync --frozen`
- Start command: `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`
- Environment variable: `DATABASE_URL` (connection string Neon)
