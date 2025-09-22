# Projeto de Persistência Poliglota (SQLite + MongoDB + Geo)

## Projeto realizado por: 
 - Ana Julia Grzyb (32703902)
 - Bruna Gabriela Soares de Lima (30481901)
 - Patrick Luan Ventura Aragão (29432294)

Este projeto implementa **persistência poliglota** integrando **SQLite** (dados tabulares) e **MongoDB** (documentos JSON com coordenadas), além de **funções de geoprocessamento** (cálculo de distâncias e proximidade geográfica).  
A interface é construída em **Streamlit**, permitindo cadastro, consulta e visualização em mapa.  

---

## 🚀 Funcionalidades
- Cadastro de cidades em **SQLite**.
- Cadastro de locais em **MongoDB**.
- Consulta integrada: locais do MongoDB relacionados a cidades do SQLite.
- Busca por locais próximos de uma coordenada.
- Visualização em mapa via `st.map`.

---

## 📂 Estrutura
projeto_persistencia_poliglota/
│── app.py
│── db_sqlite.py
│── db_mongo.py
│── geoprocessamento.py
│── seed.py
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── .env.example
│── data/ # SQLite persistente
│── mongo_data/ # MongoDB persistente

## ⚙️ Requisitos
- **Docker** e **Docker Compose** instalados.  
- Opcional: Python 3.10+ (se quiser rodar fora do container).

## ▶️ Executando com Docker Compose
1. Construa os containers:
   ```bash
   docker-compose build

2. Suba os serviços:
    docker-compose up

3. Acesse o app no navegador:
👉 http://localhost:8501

## 🌱 População de Dados
Para inserir cidades e locais de exemplo dentro do container:
    docker exec -it polyglot-persistence-app python seed.py

## ⚡ Variáveis de Ambiente
Configuração de variáveis:
MONGO_URI=mongodb://mongo:27017
MONGO_DB=poliglota
MONGO_COL=locais
(O docker-compose.yml já carrega estas variáveis automaticamente.)

## 🛑 Parar e remover containers
    docker-compose down

## ✨ Tecnologias
Python 3.11 (slim, via Docker)
SQLite 3
MongoDB 6
Streamlit
Pandas
PyMongo

## 📸 Demonstração do projeto
### Cadastro:
<img width="1894" height="940" alt="image" src="https://github.com/user-attachments/assets/17affed8-3335-41ce-a1de-6f45d9fb5591" />


### Consulta:
<img width="1910" height="926" alt="image" src="https://github.com/user-attachments/assets/5619bd7d-1189-47a2-8445-001ffdea562d" />


### Geo-proximidade:
<img width="1902" height="946" alt="image" src="https://github.com/user-attachments/assets/802ad8db-9f20-47d6-8eea-e731d14335c4" />



