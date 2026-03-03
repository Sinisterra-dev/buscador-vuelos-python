import sqlite3
import json
import os

DB_PATH = "data/cache.db"
os.makedirs("data", exist_ok=True)


def _create_table():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                origen  TEXT,
                destino TEXT,
                salida  TEXT,
                vuelta  TEXT,
                data    TEXT,
                PRIMARY KEY (origen, destino, salida, vuelta)
            )
        """)
        conn.commit()


_create_table()


def guardar_cache(origen, destino, salida, vuelta, data):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO cache VALUES (?,?,?,?,?)",
            (origen, destino, salida, vuelta or "", json.dumps(data)),
        )
        conn.commit()


def cargar_cache(origen, destino, salida, vuelta):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT data FROM cache WHERE origen=? AND destino=? AND salida=? AND vuelta=?",
            (origen, destino, salida, vuelta or ""),
        ).fetchone()
    return json.loads(row[0]) if row else None
