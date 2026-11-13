import os
import psycopg2

DB_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:pkgpass@localhost:5432/pkgcheck"
)


def get_conn():
    return psycopg2.connect(DB_URL)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            verdict TEXT NOT NULL,
            risk_score REAL NOT NULL,
            reasons TEXT,
            wrong_alert BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT now()
        )
        """
    )
    conn.commit()
    conn.close()


def log_prediction(name, verdict, risk, reasons):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predictions (name, verdict, risk_score, reasons) "
        "VALUES (%s, %s, %s, %s) RETURNING id",
        (name, verdict, risk, "; ".join(reasons)),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return new_id


def mark_wrong(check_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE predictions SET wrong_alert = TRUE WHERE id = %s", (check_id,)
    )
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed