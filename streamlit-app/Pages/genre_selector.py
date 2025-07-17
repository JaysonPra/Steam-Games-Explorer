import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from utils import load_and_clean_data

# Page Config
st.set_page_config(page_title="Steam Explorer - Genre Selector")

steam_games = load_and_clean_data()


