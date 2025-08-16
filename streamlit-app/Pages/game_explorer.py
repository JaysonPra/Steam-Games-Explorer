import streamlit as st
import pandas as pd
import math

from utils import load_and_clean_data
from views.explorer import game_explorer

st.set_page_config(page_title="Steam Explorer - Game Explorer", layout="wide")

st.markdown(
    """
    <style>
    .stMainBlockContainer {
        padding-top: 1.5rem; 
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

steam_games = load_and_clean_data()

# Calling function from Views/explorer
game_explorer(steam_games)