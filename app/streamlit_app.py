import altair as alt
import math
import pages.home
import pandas as pd
import streamlit as st

pages = [
    st.Page("pages/home.py", title="Home"),
]

pg = st.navigation(pages, position="sidebar")

pg.run()