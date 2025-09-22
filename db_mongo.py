import os
from pymongo import MongoClient
from typing import List, Dict

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "poliglota")
MONGO_COL = os.getenv("MONGO_COL", "locais")

_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
_db = _client[MONGO_DB]
_col = _db[MONGO_COL]

def add_local(nome_local: str, cidade: str, latitude: float, longitude: float, descricao: str = "", metadata: dict = None) -> str:
    doc = {
        "nome_local": nome_local,
        "cidade": cidade,
        "coordenadas": {"latitude": float(latitude), "longitude": float(longitude)},
        "descricao": descricao,
        "metadata": metadata or {}
    }
    res = _col.insert_one(doc)
    return str(res.inserted_id)

def find_locais_by_city(cidade: str) -> List[Dict]:
    cursor = _col.find({"cidade": cidade})
    return [_parse_doc(d) for d in cursor]

def get_all_locais() -> List[Dict]:
    return [_parse_doc(d) for d in _col.find()]

def _parse_doc(d):
    return {
        "id": str(d.get("_id")),
        "nome_local": d.get("nome_local"),
        "cidade": d.get("cidade"),
        "descricao": d.get("descricao", ""),
        "coordenadas": d.get("coordenadas", {})
    }

