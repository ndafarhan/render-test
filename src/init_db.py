import logging

from src import db

logger = logging.getLogger(__name__)


async def ensure_schema() -> None:
    """Create the customer table if it's missing and seed one dummy row if it's empty."""
    async with db.pool.connection() as conn:
        cur = await conn.execute("SELECT to_regclass('public.customer') IS NOT NULL AS exists")
        if not (await cur.fetchone())["exists"]:
            logger.info("Table 'customer' not found, creating it")
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS customer (
                    customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    name        TEXT NOT NULL,
                    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
                    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )

        cur = await conn.execute("SELECT EXISTS (SELECT 1 FROM customer) AS has_rows")
        if not (await cur.fetchone())["has_rows"]:
            logger.info("Table 'customer' is empty, inserting dummy data")
            await conn.execute("INSERT INTO customer (name) VALUES (%s)", ("John Doe",))
