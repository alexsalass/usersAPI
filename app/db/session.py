from psycopg_pool import ConnectionPool
from app.core.config import settings

pool: ConnectionPool | None = None


def init_db():
    global pool
    dsn = (
        f"host={settings.DB_HOST} "
        f"port={settings.DB_PORT} "
        f"dbname={settings.DB_NAME} "
        f"user={settings.DB_USER} "
        f"password={settings.DB_PASSWORD}"
    )
    pool = ConnectionPool(conninfo=dsn, max_size=10, timeout=5, open=True)


def close_db():
    global pool
    if pool:
        pool.close()
        pool = None


def get_conn():
    if not pool:
        raise RuntimeError("DB not initialized")
    return pool.connection()
