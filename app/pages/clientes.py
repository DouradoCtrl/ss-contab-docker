import streamlit as st
from sqlalchemy import text

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT * FROM clientes;', ttl="10m")

st.title("Clientes")
st.write("Veja, cadastre, edite e exclua clientes.")

st.dataframe(df)

@st.dialog("Adicionar Cliente")
def adicionar_cliente():
    nome = st.text_input("Nome")
    empreendimento = st.text_input("Empreendimento")
    if st.button("Salvar"):
        if nome and empreendimento:
            with conn.session as s:
                s.execute(
                    text("INSERT INTO clientes (nome, empreendimento) VALUES (:nome, :empreendimento)"),
                    {"nome": nome, "empreendimento": empreendimento}
                )
                s.commit()
            st.success("Cliente adicionado com sucesso!")
            st.rerun()
        else:
            st.error("Preencha todos os campos.")

if st.button("Adicionar"):
    adicionar_cliente()
