import sqlite3
from typing import List, Dict
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "poliglota.sqlite")

def get_conn(path=DB_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(path=DB_PATH):
    conn = get_conn(path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        estado TEXT,
        pais TEXT,
        latitude REAL,
        longitude REAL
    );
    """)
    conn.commit()
    conn.close()

def add_city(nome: str, estado: str = None, pais: str = None, latitude: float = None, longitude: float = None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT OR IGNORE INTO cidades(nome, estado, pais, latitude, longitude)
    VALUES (?, ?, ?, ?, ?)
    """, (nome, estado, pais, latitude, longitude))
    conn.commit()
    conn.close()

def get_cities() -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cidades ORDER BY nome")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_city_by_name(nome: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cidades WHERE nome = ?", (nome,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None
