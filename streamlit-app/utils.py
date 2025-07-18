import pandas as pd
import streamlit as st
import numpy as np
import os

# Data Cleaning
@st.cache_data(show_spinner="Loading and cleaning raw data...")
def load_and_clean_data():
    BASE_DIR = os.path.dirname(__file__)
    DATA_PATH = os.path.join(BASE_DIR, "..", "data", "games.csv")
    df = pd.read_csv(DATA_PATH)
    
    # Renaming all columns
    df.columns = ['Name', 'Release date', 'Estimated owners', 'Peak CCU',
       'Required age', 'Price', 'Discount', 'DLC count', 'About the game',
       'Supported languages', 'Full audio languages', 'Reviews',
       'Header image', 'Website', 'Support url', 'Support email', 'Windows',
       'Mac', 'Linux', 'Metacritic score', 'Metacritic url', 'User score',
       'Positive', 'Negative', 'Score rank', 'Achievements', 'Recommendations',
       'Notes', 'Average playtime forever', 'Average playtime two weeks',
       'Median playtime forever', 'Median playtime two weeks', 'Developers',
       'Publishers', 'Categories', 'Genres', 'Tags', 'Screenshots', 'Movies']
    
    # Dropping unneeded columns
    cols_to_drop = ["Screenshots",  "Movies", "Tags", "Website", "Support email", "Header image", "About the game" , "Metacritic url", "Support url", "Score rank", "Notes", "Reviews", "About the game"]
    df.drop(cols_to_drop, axis=1, inplace=True)

    # Dropping all null rows
    df.dropna(inplace=True)

    # Date Conversion
    pd.to_datetime(df["Release date"], errors='coerce')
    df.dropna(subset=["Release date"], inplace=True)

    # Cleaning Estimated Owners
    owners_split = df["Estimated owners"].str.split(' - ', expand=True).astype(float)
    df["Estimated owners avg"] = owners_split.mean(axis=1)

    number_to_reduced_number = {
      '0 - 20000': '0 - 20K',
      '20000 - 50000': '20K - 50K',
      '50000 - 100000': '50K - 100K',
      '100000 - 200000': '100K - 200K',
      '200000 - 500000': '200K - 500K',
      '500000 - 1000000': '500K - 1M',
      '1000000 - 2000000': '1M - 2M',
      '2000000 - 5000000': '2M - 5M',
      '5000000 - 10000000': '5M - 10M',
      '10000000 - 20000000': '10M - 20M',
      '20000000 - 50000000': '20M - 50M',
      '50000000 - 100000000': '50M - 100M',
      '100000000 - 200000000': '100M - 200M'
    }
   
    df['Estimated owners'] = df['Estimated owners'].map(number_to_reduced_number)

    return df
