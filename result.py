from pymongo import MongoClient
import streamlit as st
import pandas as pd
import altair as alt

def run():
    st.set_page_config(
        page_title="🌐 EuthMappers quizz result",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state='expanded'
    )

pg = st.navigation([
    st.Page("pages/Result09-10-2024.py", title="Result 09/10/2024", icon="🔥"),
    st.Page("pages/Result03-10-2024.py", title="Result 03/10/2024", icon="🔥")
])
