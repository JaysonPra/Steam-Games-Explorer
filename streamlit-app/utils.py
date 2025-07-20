# utils.py
import pandas as pd
import numpy as np
import os
import streamlit as st

from constants.color_schemes import COLOR_SCHEMES

# Helper function for Color Category
def apply_categorical_order(df):
    df['Price Category'] = pd.Categorical(
        df['Price Category'],
        categories=COLOR_SCHEMES["price_scale"]["order"],
        ordered=True
    )

    return df

# Function to be used in load_and_clean_data for creating features used for filtering
def feature_creation(df):
    #  -- Reviews --
    df["Reviews"] = df["Positive"] + df["Negative"]
    df["Reviews Percentage"] = (df["Positive"] / df["Reviews"]) * 100

    df.loc[df["Reviews"] == 0, "Reviews Percentage"] = 0

    df["Reviews Percentage"] = df["Reviews Percentage"].round(0).astype(int)

    # -- Value / Weighted Value --
    df.loc[df["Price"] > 0, "Value"] = df["Average playtime forever"] / df["Price"]

    valid_mask = (
        (df["Price"] > 0) &
        np.isfinite(df["Value"]) &
        df["Metacritic score"].notna() &
        (df["Metacritic score"] > 0)
    )

    df.loc[valid_mask, "Weighted Value"] = df.loc[valid_mask, "Value"] * df.loc[valid_mask, "Metacritic score"]

    # -- Release Year --
    df["Release Year"] = df["Release date"].dt.year
    
    # -- Price Category --
    price_conditions = [
        (df['Price'] == 0),
        (df['Price'] > 0) & (df['Price'] <= 4.99),
        (df['Price'] > 4.99) & (df['Price'] <= 9.99),
        (df['Price'] > 9.99) & (df['Price'] <= 19.99),
        (df['Price'] > 19.99) & (df['Price'] <= 39.99),
        (df['Price'] > 39.99) & (df['Price'] <= 59.99),
        (df['Price'] > 59.99)
    ]

    choices = [
        'Free',
        '$0.01 - $4.99',
        '$5.00 - $9.99',
        '$10.00 - $19.99',
        '$20.00 - $39.99',
        '$40.00 - $59.99',
        '$60.00+'
    ]

    df['Price Category'] = np.select(price_conditions, choices, default="Unknown")

    # -- Indie Or Not --
    df["Is_Indie"] = df["Genres"].fillna('').apply(
        lambda x: 'Indie' if "Indie" in x else "Non-Indie"
    )

    # -- Steam store URL --
    df['Steam_URL'] = 'https://store.steampowered.com/app/' + df["AppID"].astype(str) + '/'

    return df

# -- Loading and Cleaning Data --
@st.cache_data()
def load_and_clean_data():
    BASE_DIR = os.path.dirname(__file__)
    DATA_PATH = os.path.join(BASE_DIR, "..", "data", "games.csv")

    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        st.error(f"Error: Data file not found at {DATA_PATH}")

    # -- Working with columns --

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

    # -- Is a Game or Not --
    df["Is_Game"] = df["Categories"].fillna('').apply(
        lambda x: "single-player" in x.lower() or "multi-player" in x.lower()
    )
    df = df[df["Is_Game"] == True].copy()

    # -- Index Reset --
    df = df.reset_index(names=['AppID'])

    # -- Type Conversions and Initial Cleaning --

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
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')


    # -- Type optimization --
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

    # Floating point optimization
    df['Price'] = df['Price'].round(2)

    # -- Feature Creation for Filtering --
    df = feature_creation(df)

    # -- Category Order for Coloring --
    df = apply_categorical_order(df)

    return df
