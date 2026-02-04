import streamlit as st

conn = st.connection("postgresql", type="sql")
df = conn.query('SELECT * FROM clientes;', ttl="10m")

st.title("Clientes")
st.write("Veja, cadastre, edite e exclua clientes.")

st.dataframe(df)
