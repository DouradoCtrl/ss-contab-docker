import altair as alt
import math
import pages.home
import pandas as pd
import streamlit as st

pages = [
    st.Page("pages/home.py", title="Início"),
    st.Page("pages/dashboard.py", title="Painel"),
]

pg = st.navigation(pages, position="sidebar")

pg.run()