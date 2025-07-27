import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from utils import load_and_clean_data
from views.genre import *

st.set_page_config(page_title="Steam Explorer - Genre Selector", layout="wide")

steam_games = load_and_clean_data()

# Reducing top padding
st.markdown(
    """
    <style>
    .stMainBlockContainer {
        padding-top: 3.0rem; 
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Padding left and right
buff1, main, buff2 = st.columns([0.05,1,0.05])

with main:
    st.subheader("Genre Selector")
    genre_selector_builder(steam_games)
