from app.db.session import get_conn


class UsersRepository:

    def list(self, limit: int, offset: int):
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, first_name, last_name, email, is_active, created_at
                    FROM users
                    ORDER BY id
                    LIMIT %s OFFSET %s
                """, (limit, offset))
                return cur.fetchall()

    def get(self, user_id: int):
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, first_name, last_name, email, is_active, created_at
                    FROM users
                    WHERE id = %s
                """, (user_id,))
                return cur.fetchone()
