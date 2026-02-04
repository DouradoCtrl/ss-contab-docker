import streamlit as st
from sqlalchemy import text
import pandas as pd

def render(filtros, conn):
    # st.write(filtros)
    query = "SELECT * FROM entradas WHERE 1=1"
    params = {}

    if filtros['cliente_id']:
        query += " AND cliente_id = :cliente_id"
        params["cliente_id"] = filtros['cliente_id']

    if filtros['data_inicio'] and filtros['data_fim']:
        query += " AND data_entrada BETWEEN :data_inicio AND :data_fim"
        params["data_inicio"] = filtros['data_inicio']
        params["data_fim"] = filtros['data_fim']
    
    elif filtros['mes'] != "Todos" and filtros['ano']:
        meses = {
            "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4, "Maio": 5, "Junho": 6,
            "Julho": 7, "Agosto": 8, "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
        }
        mes_num = meses.get(filtros['mes'])
        query += " AND EXTRACT(MONTH FROM data_entrada) = :mes AND EXTRACT(YEAR FROM data_entrada) = :ano"
        params["mes"] = mes_num
        params["ano"] = int(filtros['ano'])

    with conn.session as s:
        result = s.execute(text(query), params)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    st.dataframe(df)