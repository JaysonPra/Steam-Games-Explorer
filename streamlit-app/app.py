import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from utils import load_and_clean_data

steam_games = load_and_clean_data("../data/games.csv")
