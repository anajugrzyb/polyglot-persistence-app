"""
Script para popular automaticamente o SQLite e o MongoDB com dados de exemplo.
Pode ser executado localmente ou dentro do container Docker:
    docker exec -it poliglota_app python seed.py
"""

from db_sqlite import init_db, add_city, get_cities
from db_mongo import add_local, get_all_locais

def main():
    print(">>> Inicializando banco SQLite...")
    init_db()

    # Inserir cidades
    cidades = [
        ("João Pessoa", "PB", "Brasil", -7.11532, -34.861),
        ("Recife", "PE", "Brasil", -8.0476, -34.8770),
        ("Natal", "RN", "Brasil", -5.79448, -35.2110),
    ]
    for nome, estado, pais, lat, lon in cidades:
        add_city(nome, estado, pais, lat, lon)

    print(">>> Cidades adicionadas ao SQLite.")

    # Inserir locais
    locais = [
        ("Praça da Independência", "João Pessoa", -7.11532, -34.861, "Ponto turístico central da cidade."),
        ("Farol do Cabo Branco", "João Pessoa", -7.1460, -34.8010, "Ponto mais oriental das Américas."),
        ("Marco Zero", "Recife", -8.0632, -34.8711, "Centro histórico de Recife."),
        ("Forte dos Reis Magos", "Natal", -5.7681, -35.1999, "Fortaleza histórica do século XVI."),
    ]
    for nome, cidade, lat, lon, desc in locais:
        add_local(nome, cidade, lat, lon, desc)

    print(">>> Locais adicionados ao MongoDB.")

    # Mostrar resumo
    print("\n--- Resumo ---")
    print("Cidades (SQLite):")
    for c in get_cities():
        print(f"- {c['nome']} ({c['estado']}, {c['pais']})")

    print("\nLocais (MongoDB):")
    for l in get_all_locais():
        print(f"- {l['nome_local']} -> {l['cidade']}")

if __name__ == "__main__":
    main()
