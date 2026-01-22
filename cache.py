import sqlite3
import json
import os

DB_PATH = "data/cache.db"
os.makedirs("data", exist_ok=True)

def _create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS cache (
                    origen TEXT, destino TEXT,
                    salida TEXT, vuelta TEXT,
                    data TEXT)""")
    conn.commit()
    conn.close()

_create_table()

def guardar_cache(origen, destino, salida, vuelta, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO cache VALUES (?,?,?,?,?)",
              (origen, destino, salida, vuelta, json.dumps(data)))
    conn.commit()
    conn.close()

def cargar_cache(origen, destino, salida, vuelta):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT data FROM cache WHERE origen=? AND destino=? AND salida=? AND vuelta=?",
              (origen, destino, salida, vuelta))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None
