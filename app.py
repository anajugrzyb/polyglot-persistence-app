import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

from db_sqlite import init_db, add_city, get_cities, get_city_by_name
from db_mongo import add_local, find_locais_by_city, get_all_locais
from geoprocessamento import locais_proximos

st.set_page_config(page_title="Persistência Poliglota + Geo", layout="wide")
init_db()

st.title("Persistência Poliglota (SQLite + MongoDB) + Geo 🗺️")

with st.sidebar:
    st.header("Conexões")
    st.write("Mongo URI")
    st.write("**Usando:** " + (os.getenv("MONGO_URI", "mongodb://localhost:27017")))

tab1, tab2, tab3 = st.tabs(["Cadastro", "Consulta", "Geo-proximidade"])

with tab1:
    st.subheader("Cadastrar cidade (SQLite)")
    with st.form("form_city"):
        nome = st.text_input("Nome da cidade")
        estado = st.text_input("Estado")
        pais = st.text_input("País", value="Brasil")
        lat = st.text_input("Latitude")
        lon = st.text_input("Longitude")
        submitted = st.form_submit_button("Adicionar cidade")
        if submitted:
            try:
                lat_v = float(lat) if lat else None
                lon_v = float(lon) if lon else None
                add_city(nome.strip(), estado.strip() or None, pais.strip() or None, lat_v, lon_v)
                st.success(f"Cidade '{nome}' adicionada.")
            except Exception as e:
                st.error(f"Erro: {e}")

    st.markdown("---")
    st.subheader("Cadastrar local (MongoDB)")
    cidades = get_cities()
    cidades_nomes = [c["nome"] for c in cidades]
    with st.form("form_local"):
        nome_local = st.text_input("Nome do local")
        cidade_sel = st.selectbox("Cidade (relacionar com SQLite)", options=cidades_nomes or [""])
        lat_local = st.number_input("Latitude", format="%.6f", value=0.0)
        lon_local = st.number_input("Longitude", format="%.6f", value=0.0)
        descricao = st.text_area("Descrição")
        btn_local = st.form_submit_button("Adicionar local")
        if btn_local:
            try:
                add_local(nome_local.strip(), cidade_sel.strip(), float(lat_local), float(lon_local), descricao.strip())
                st.success(f"Local '{nome_local}' adicionado em '{cidade_sel}'.")
            except Exception as e:
                st.error(f"Erro ao inserir no MongoDB: {e}")

with tab2:
    st.subheader("Consultar locais por cidade")
    cidades = get_cities()
    nomes = [c["nome"] for c in cidades]
    sel = st.selectbox("Selecione cidade", options=nomes or [""])
    if sel:
        locais = find_locais_by_city(sel)
        st.write(f"Locais encontrados: {len(locais)}")
        if locais:
            df = pd.DataFrame([{
                "nome_local": l["nome_local"],
                "descricao": l.get("descricao",""),
                "latitude": l["coordenadas"].get("latitude"),
                "longitude": l["coordenadas"].get("longitude")
            } for l in locais])
            st.dataframe(df)
            # mostrar no mapa (st.map)
            if not df[["latitude","longitude"]].isnull().any().any():
                st.map(df.rename(columns={"latitude":"lat","longitude":"lon"}))
            else:
                st.warning("Alguns locais não possuem coordenadas válidas para exibir no mapa.")

with tab3:
    st.subheader("Pesquisar locais próximos (a partir de um ponto)")
    escolha = st.radio("Origem do ponto", ("Manual", "Usar centro de uma cidade"))
    if escolha == "Manual":
        lat0 = st.number_input("Latitude", format="%.6f", value=-7.11532)
        lon0 = st.number_input("Longitude", format="%.6f", value=-34.861)
    else:
        cidades = get_cities()
        nomes = [c["nome"] for c in cidades]
        cidade_origem = st.selectbox("Escolha cidade como origem", options=nomes or [""])
        cinfo = get_city_by_name(cidade_origem) if cidade_origem else None
        if cinfo and cinfo.get("latitude") is not None and cinfo.get("longitude") is not None:
            lat0 = float(cinfo["latitude"])
            lon0 = float(cinfo["longitude"])
            st.write(f"Usando coordenadas de {cidade_origem}: {lat0}, {lon0}")
        else:
            st.warning("Cidade selecionada não possui coordenadas. Use entrada manual.")
            lat0 = st.number_input("Latitude", value=0.0)
            lon0 = st.number_input("Longitude", value=0.0)

    raio = st.slider("Raio (km)", min_value=1, max_value=200, value=10)
    if st.button("Buscar locais próximos"):
        locais = get_all_locais()
        encontrados = locais_proximos(locais, lat0, lon0, raio)
        st.write(f"{len(encontrados)} locais encontrados em até {raio} km")
        if encontrados:
            df = pd.DataFrame([{
                "nome_local": e["nome_local"],
                "cidade": e["cidade"],
                "dist_km": e["distance_km"],
                "latitude": e["coordenadas"]["latitude"],
                "longitude": e["coordenadas"]["longitude"]
            } for e in encontrados])
            st.dataframe(df)
            st.map(df.rename(columns={"latitude":"lat","longitude":"lon"}))
        else:
            st.info("Nenhum local encontrado dentro do raio informado.")

st.markdown("---")
st.caption("Desenvolvido para Projeto de Persistência Poliglota — SQLite + MongoDB + Geo")
