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


    # botões de ação
    if filtros['cliente'] != "Todos":
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            if st.button("Adicionar", type="primary"):
                @st.dialog("Adicionar Entrada")
                def adicionar_entrada():
                    # Usa cliente_id e nome do filtro
                    cliente_id = filtros['cliente_id']
                    cliente_nome = filtros['cliente']

                    st.write(f"Cliente selecionado: {cliente_nome}")

                    nome = st.text_input("Nome da Entrada")
                    categoria = st.text_input("Categoria")
                    valor = st.number_input("Valor", min_value=0.0, format="%.2f")
                    banco_origem = st.text_input("Banco de Origem")
                    data_entrada = st.date_input("Data de Entrada")

                    if st.button("Salvar", type="primary"):
                        with conn.session as s:
                            s.execute(
                                text("INSERT INTO entradas (cliente_id, nome, categoria, valor, banco_origem, data_entrada) VALUES (:cliente_id, :nome, :categoria, :valor, :banco_origem, :data_entrada)"),
                                {"cliente_id": cliente_id, "nome": nome, "categoria": categoria, "valor": valor, "banco_origem": banco_origem, "data_entrada": data_entrada}
                            )
                            s.commit()
                        st.success("Entrada adicionada com sucesso!")
                        st.rerun()
                adicionar_entrada()
        
        with col2:
            if st.button("Opções"):
                @st.dialog("Excluir ou Editar Entrada")
                def editar_excluir_entrada():
                    if df.empty:
                        st.warning("Nenhuma entrada encontrada para editar.")
                        return
                    
                    # Criar lista de opções para o selectbox
                    entradas = []
                    for _, row in df.iterrows():
                        label = f"{row['nome']} - {row['categoria']} - {row['data_entrada']}"
                        entradas.append((label, row))
                    
                    # Selectbox para escolher a entrada
                    entrada_selecionada = st.selectbox(
                        "Selecione a entrada",
                        options=entradas,
                        format_func=lambda x: x[0]
                    )
                    
                    if entrada_selecionada:
                        _, entrada = entrada_selecionada
                        
                        # Campos preenchidos com os dados da entrada selecionada
                        nome = st.text_input("Nome da Entrada", value=entrada['nome'])
                        categoria = st.text_input("Categoria", value=entrada['categoria'])
                        valor = st.number_input("Valor", min_value=0.0, format="%.2f", value=float(entrada['valor']) if 'valor' in entrada and entrada['valor'] is not None else 0.0)
                        banco_origem = st.text_input("Banco de Origem", value=entrada['banco_origem'] if 'banco_origem' in entrada else "")
                        data_entrada = st.date_input("Data de Entrada", value=entrada['data_entrada'])
                        
                        # Botões de ação
                        col_salvar, col_cancelar, col_excluir = st.columns(3)
                        
                        with col_salvar:
                            if st.button("Salvar alterações", type="primary"):
                                with conn.session as s:
                                    s.execute(
                                        text("UPDATE entradas SET nome=:nome, categoria=:categoria, valor=:valor, banco_origem=:banco_origem, data_entrada=:data_entrada WHERE id=:id"),
                                        {"nome": nome, "categoria": categoria, "valor": valor, "banco_origem": banco_origem, "data_entrada": data_entrada, "id": entrada['id']}
                                    )
                                    s.commit()
                                st.success("Entrada atualizada com sucesso!")
                                st.rerun()
                        
                        with col_cancelar:
                            if st.button("Cancelar"):
                                st.rerun()
                        
                        with col_excluir:
                            if st.button("Excluir registro", type="secondary"):
                                with conn.session as s:
                                    s.execute(
                                        text("DELETE FROM entradas WHERE id=:id"),
                                        {"id": entrada['id']}
                                    )
                                    s.commit()
                                st.success("Entrada excluída com sucesso!")
                                st.rerun()
                
                editar_excluir_entrada()

        
    if filtros['cliente'] == "Todos":
        st.info("Escolha um cliente para exibir.")
    else:
        st.dataframe(df)