import streamlit as st
import pandas as pd
import altair as alt

from utils import load_and_clean_data, COLOR_SCHEMES
from visualizations.showcase import *

# Reducing top and bottom padding (Very hacky implementation for a sidebar)
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

st.set_page_config(page_title="Steam Explorer - Game Showcase", layout="wide")

# Loading Dataset
steam_games = load_and_clean_data()

sidebar, main, buff = st.columns([1,4,1])
with main:
    st.header("Game Showcase Page")
    tab1, tab2, tab3, tab4 = st.tabs(["Top Games by Peak CCU", "Top Value Games", "Sleeper Hits", "Game Pricing"])

with tab1:
    top_games_ccu(steam_games)
with tab2:
    top_value_games(steam_games)
with tab3:
    sleeper_games(steam_games)
with tab4:
    games_pricing(steam_games)