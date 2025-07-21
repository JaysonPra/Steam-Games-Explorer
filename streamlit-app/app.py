import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from utils import load_and_clean_data, get_unique_genres

# Page Config
st.set_page_config(
        page_icon="🎮",
        layout="centered",
    )

# Page Logo
current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "..", "assets", "logo.png")

st.logo(logo_path, size="large")

with st.spinner("Loading the steam dataset and preparing dashboard..."):
    # Loading cleaned dataset for caching
    steam_games = load_and_clean_data()

    # Loading unique genres for caching
    get_unique_genres(steam_games)

pages = [
    st.Page("Pages/landing.py", title="Steam Explorer", default=True),
    st.Page("Pages/game_explorer.py", title="Game Explorer"),
    st.Page("Pages/game_showcase.py", title="Game Showcase"),
    st.Page("Pages/genre_selector.py", title="Genre Selector")
]

pg = st.navigation(pages, position="top")
pg.run()