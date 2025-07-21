import streamlit as st
import altair as alt

from utils import get_unique_genres

# Builder for the Genre Selector Page
@st.fragment
def genre_selector_builder(steam_games):
    # Columns for Sidebar(Filters) and Main(Visualizations)
    sidebar, main = st.columns([1,4])
    with sidebar:
        unique_genres = get_unique_genres(steam_games)

        genre_selections = st.multiselect(
            label="Select 1 or More Genres",
            options=unique_genres
        )

