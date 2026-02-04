import streamlit as st

st.title("Financeiro")
st.write("Gerencie entradas, saídas e gastos fixos.")

tab_entrada, tab_saida, tab_gastos_fixos = st.tabs([
    ":material/list_alt: Entradas", 
    ":material/event: Despesas", 
    ":material/assignment_late: Gastos Fixos    "
])