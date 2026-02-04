import streamlit as st
from pages.tabs import tab_entradas
from components import filtros_financeiro

conn = st.connection("postgresql", type="sql")

st.title("Financeiro")
st.write("Gerencie entradas, saídas e gastos fixos.")

# filtro reutilizável 
filtros = filtros_financeiro.render_filtros(conn)

tab_entrada, tab_saida, tab_gastos_fixos = st.tabs([
    ":material/list_alt: Entradas", 
    ":material/event: Despesas", 
    ":material/assignment_late: Gastos Fixos"
])

with tab_entrada:
    tab_entradas.render(filtros)
    
