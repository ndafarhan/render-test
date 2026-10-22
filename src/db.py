import os

from psycopg import AsyncConnection
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

# Neon connection string, e.g.
# postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
DATABASE_URL = os.environ.get("DATABASE_URL")

pool: AsyncConnectionPool | None = None


async def open_pool() -> None:
    global pool
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    pool = AsyncConnectionPool(
        DATABASE_URL,
        min_size=1,
        max_size=int(os.environ.get("DB_POOL_MAX", 5)),
        # Neon's pooled endpoint (PgBouncer, transaction mode) doesn't support
        # server-side prepared statements.
        kwargs={"row_factory": dict_row, "prepare_threshold": None},
        # Neon suspends idle computes, so verify connections before handing them out.
        check=AsyncConnectionPool.check_connection,
        max_idle=300,
        open=False,
    )
    await pool.open(wait=True, timeout=30)


async def close_pool() -> None:
    global pool
    if pool is not None:
        await pool.close()
        pool = None


async def get_conn():
    """FastAPI dependency yielding a pooled connection (commits on success)."""
    if pool is None:
        raise RuntimeError("Database pool is not open")
    async with pool.connection() as conn:
        yield conn


async def ping() -> bool:
    if pool is None:
        return False
    async with pool.connection() as conn:
        await conn.execute("SELECT 1")
    return True


__all__ = ["AsyncConnection", "open_pool", "close_pool", "get_conn", "ping"]
