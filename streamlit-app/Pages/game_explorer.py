import streamlit as st
import pandas as pd

from utils import load_and_clean_data

# Page Config
st.set_page_config(page_title="Steam Explorer - Game Explorer")

steam_games = load_and_clean_data()

