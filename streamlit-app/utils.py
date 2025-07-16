import pandas as pd
import numpy as np

def load_and_clean_data(path):
    df = pd.read_cs(path)

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
    df["Estimated owners"] = owners_split.mean(axis=1)

    return df