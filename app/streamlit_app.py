import altair as alt
import math
import pages.home
import pandas as pd
import streamlit as st

pages = [
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/dashboard.py", title="Dashboard"),
    st.Page("pages/relatorio.py", title="Relatórios"),
    st.Page("pages/financeiro.py", title="Financeiro"),
    st.Page("pages/clientes.py", title="Clientes"),
]

pg = st.navigation(pages, position="sidebar")

pg.run()