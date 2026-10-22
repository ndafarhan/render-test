# render-test

Service FastAPI sederhana dengan CRUD item (in-memory).

## Jalankan lokal

```bash
uv sync
uv run main.py
```

Buka http://localhost:8000/docs untuk Swagger UI.

## Endpoint

| Method | Path          | Keterangan        |
|--------|---------------|-------------------|
| GET    | `/`           | Pesan sambutan    |
| GET    | `/health`     | Health check      |
| GET    | `/items`      | Daftar item       |
| GET    | `/items/{id}` | Detail item       |
| POST   | `/items`      | Buat item         |
| PUT    | `/items/{id}` | Ubah item         |
| DELETE | `/items/{id}` | Hapus item        |

## Deploy ke Render

- Build command: `pip install uv && uv sync --frozen`
- Start command: `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`
