import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

from utils import load_and_clean_data

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "games.csv")
steam_games = load_and_clean_data(DATA_PATH)

st.set_page_config(
    page_title="Steam Game Explorer",
    page_icon="🎮",
    layout="wide"
)

st.write("Hello world")