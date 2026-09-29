import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "goldfolio")
DB_USER = os.getenv("DB_USER", "readonly_user")
DB_PASS = os.getenv("DB_PASS", "readonly_password")

SQL = """
SELECT
    id,
    user_id,
    symbol,
    quantity,
    avg_buy_price,
    current_price,
    (quantity * current_price) AS market_value
FROM holdings
ORDER BY market_value DESC
LIMIT 100;
"""


def main() -> None:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        sslmode=os.getenv("DB_SSLMODE", "require"),
    )
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(SQL)
            rows = cur.fetchall()
            for row in rows:
                print(dict(row))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
