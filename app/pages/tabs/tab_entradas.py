import streamlit as st
from sqlalchemy import text
import pandas as pd

def render(filtros, conn):
    st.write(filtros)
    query = "SELECT * FROM entradas WHERE 1=1"
    params = {}

    # query para pesquisar por filtros
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


    # botão de adicionar entrada
    if filtros['cliente'] != "Todos":
        if st.button("Adicionar", type="primary"):
            @st.dialog("Adicionar Entrada")
            def adicionar_entrada():
                # Usa cliente_id e nome do filtro
                cliente_id = filtros['cliente_id']
                cliente_nome = filtros['cliente']

                st.write(f"Cliente selecionado: {cliente_nome}")

                nome = st.text_input("Nome da Entrada")
                categoria = st.text_input("Categoria")
                data_entrada = st.date_input("Data de Entrada")

                if st.button("Salvar", type="primary"):
                    with conn.session as s:
                        s.execute(
                            text("INSERT INTO entradas (cliente_id, nome, categoria, data_entrada) VALUES (:cliente_id, :nome, :categoria, :data_entrada)"),
                            {"cliente_id": cliente_id, "nome": nome, "categoria": categoria, "data_entrada": data_entrada}
                        )
                        s.commit()
                    st.success("Entrada adicionada com sucesso!")
                    st.rerun()
            adicionar_entrada()

        
    if filtros['cliente'] == "Todos":
        st.info("Escolha um cliente para exibir.")
    else:
        st.dataframe(df)