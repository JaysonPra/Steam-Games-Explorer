# utils.py
import pandas as pd
import numpy as np
import os
import streamlit as st # Import streamlit to use st.cache_data decorator

@st.cache_data()
def load_and_clean_data():
    BASE_DIR = os.path.dirname(__file__)
    DATA_PATH = os.path.join(BASE_DIR, "..", "data", "games.csv")

    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        st.error(f"Error: Data file not found at {DATA_PATH}")

    # Renaming columns
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
    cols_to_drop = [
        "Screenshots", "Movies", "Tags", "Website", "Support email",
        "Header image", "About the game", "Metacritic url", "Support url",
        "Score rank", "Notes", "Reviews"
    ]
    
    cols_to_drop_existing = [col for col in cols_to_drop if col in df.columns]
    df.drop(cols_to_drop_existing, axis=1, inplace=True)

    # Type Conversions and Initial Cleaning

    # Date Conversion
    df["Release date"] = pd.to_datetime(df["Release date"], errors='coerce')
    df.dropna(subset=["Release date"], inplace=True)

    # Cleaning Estimated Owners
    df['Estimated owners_str'] = df['Estimated owners'].copy()
    owners_split = df["Estimated owners"].astype(str).str.split(' - ', expand=True)
    owners_split_numeric = owners_split.apply(pd.to_numeric, errors='coerce')
    df["Estimated owners avg"] = owners_split_numeric.mean(axis=1)

    number_to_reduced_number = {
        '0 - 20000': '0 - 20K', '20000 - 50000': '20K - 50K',
        '50000 - 100000': '50K - 100K', '100000 - 200000': '100K - 200K',
        '200000 - 500000': '200K - 500K', '500000 - 1000000': '500K - 1M',
        '1000000 - 2000000': '1M - 2M', '2000000 - 5000000': '2M - 5M',
        '5000000 - 10000000': '5M - 10M', '10000000 - 20000000': '10M - 20M',
        '20000000 - 50000000': '20M - 50M', '50000000 - 100000000': '50M - 100M',
        '100000000 - 200000000': '100M - 200M'
    }
    df['Estimated owners_category'] = df['Estimated owners_str'].map(number_to_reduced_number)

    df.drop('Estimated owners', axis=1, inplace=True)


    # Convert other numerical columns
    numerical_cols_to_convert = [
        "Peak CCU", "Price", "Discount", "DLC count", "Metacritic score",
        "User score", "Positive", "Negative", "Achievements", "Recommendations",
        "Average playtime forever", "Average playtime two weeks",
        "Median playtime forever", "Median playtime two weeks"
    ]
    for col in numerical_cols_to_convert:
        if col in df.columns: # Check if column exists after initial drops
            df[col] = pd.to_numeric(df[col], errors='coerce')


    # Type optimization
    df["Required age"] = df["Required age"].astype('Int8')
    df["Price"] = df["Price"].astype('float32')
    df["DLC count"] = df["DLC count"].astype('Int16')
    df["Metacritic score"] = df["Metacritic score"].astype('Int8')
    df["Achievements"] = df["Achievements"].astype('Int16')
    df["Recommendations"] = df["Recommendations"].astype('Int32')
    df["Average playtime forever"] = df["Average playtime forever"].astype('Int32')
    df["Average playtime two weeks"] = df["Average playtime two weeks"].astype('Int16')
    df["Median playtime forever"] = df["Median playtime forever"].astype('Int32')
    df["Median playtime two weeks"] = df["Median playtime two weeks"].astype('Int16')

    return df