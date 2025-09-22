from math import radians, sin, cos, asin, sqrt
from typing import List, Dict

def haversine_km(lat1, lon1, lat2, lon2) -> float:
    # retorna distância em km entre dois pontos (Haversine)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    R = 6371.0
    return R * c

def distancia_entre(coordA: dict, coordB: dict) -> float:
    return haversine_km(coordA["latitude"], coordA["longitude"], coordB["latitude"], coordB["longitude"])

def locais_proximos(locais: List[Dict], latitude: float, longitude: float, raio_km: float) -> List[Dict]:
    encontrados = []
    for l in locais:
        c = l.get("coordenadas", {})
        if c and "latitude" in c and "longitude" in c:
            d = haversine_km(latitude, longitude, c["latitude"], c["longitude"])
            if d <= raio_km:
                new = dict(l)
                new["distance_km"] = round(d, 3)
                encontrados.append(new)
    return sorted(encontrados, key=lambda x: x["distance_km"])
