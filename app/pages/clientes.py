import streamlit as st
from sqlalchemy import text

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT * FROM clientes;', ttl=0)

st.title("Clientes")
st.write("Veja, cadastre, edite e exclua clientes.")

# Card editar cliente
@st.dialog("Editar Cliente")
def editar_cliente(row):
    nome = st.text_input("Nome", value=row["nome"])
    empreendimento = st.text_input("Empreendimento", value=row["empreendimento"])
    if st.button("Salvar"):
        with conn.session as s:
            s.execute(
                text("UPDATE clientes SET nome=:nome, empreendimento=:empreendimento WHERE id=:id"),
                {"nome": nome, "empreendimento": empreendimento, "id": row["id"]}
            )
            s.commit()
        st.success("Cliente atualizado com sucesso!")
        st.rerun()

# Card adicionar cliente
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

# Card p/ excluir cliente
@st.dialog("Confirmar Exclusão")
def confirmar_exclusao(row):
    st.warning(f"Tem certeza que deseja excluir o cliente '{row['nome']}'? Esta ação não pode ser desfeita e todos os dados associados serão perdidos.")
    if st.button("Confirmar Exclusão", key=f"confirm_{row['id']}"):
        with conn.session as s:
            s.execute(
                text("DELETE FROM clientes WHERE id=:id"),
                {"id": row["id"]}
            )
            s.commit()
        st.success("Cliente excluído com sucesso!")
        st.rerun()

# Dropdown cliente
for idx, row in df.iterrows():
    with st.expander(f"{row['nome']} - {row['empreendimento']}"):
        st.write(f"Criado em: {row['criado_em']}")
        col1, col2, _ = st.columns([1,1,6])
        if col1.button("Editar", key=f"edit_{row['id']}"):
            editar_cliente(row)
        if col2.button("Excluir", key=f"delete_{row['id']}"):
            confirmar_exclusao(row)

if st.button("Adicionar"):
    adicionar_cliente()
