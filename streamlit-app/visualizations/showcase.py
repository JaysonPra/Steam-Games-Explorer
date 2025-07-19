import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

from constants.color_schemes import COLOR_SCHEMES
from constants.layout_configs import VISUALIZATION_INNER_COL_LAYOUT

# -- Top Games By Peak CCU --
@st.fragment
def top_games_ccu(steam_games):
    sidebar, spacer_col, main, buff_col = st.columns(VISUALIZATION_INNER_COL_LAYOUT)

    min_year = int(steam_games["Release Year"].min())
    max_year = int(steam_games["Release Year"].max())

    # Sidebar input (Release Year)
    with sidebar:
        start_year, end_year = st.slider(
            "**Range of Release Years**",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key="peak_ccu_year"
        )
        start_review_percent, end_review_percent = st.slider(
            "__Review Percent Range__",
            min_value=0,
            max_value=100,
            value=(0,100),
            key="peak_ccu_review_percentage",
            step=1
        )

    # Release Year Filter
    year_filter = steam_games[
        (steam_games["Release Year"] >= start_year) & (steam_games["Release Year"] <= end_year) &
        (steam_games["Reviews Percentage"] >= start_review_percent) & (steam_games["Reviews Percentage"] <= end_review_percent)
    ]

    top_ccu_games = year_filter.dropna(subset=['Peak CCU']).sort_values(by="Peak CCU", ascending=False).head(20)

    # Color Coding
    price_scheme = COLOR_SCHEMES["price_scale"]

    # Altair Horizontal Bar Chart with Tooltip Features
    chart = alt.Chart(top_ccu_games).mark_bar().encode(
        x = alt.X("Peak CCU:Q", title="Peak Concurrent Users"),
        y = alt.Y('Name:N', sort='-x', title="Game Name"),
        color=alt.Color(
            "Price Category:N",
            title="Price Range",
            sort=price_scheme["order"],
            scale=alt.Scale(
                domain=price_scheme["order"],
                range=price_scheme["colors"]
            )
        ),
        tooltip=[
            "Name:N",
            alt.Tooltip("AppID", title="App ID"),
            alt.Tooltip("Peak CCU:Q", title="Peak CCU", format=",d"),
            alt.Tooltip("Release date:T", title="Release Date"),
            
        ]
    ).properties(
        title=f"Top 20 Games by Peak CCU ({start_year}-{end_year})"
    )
    # Main Column
    with main:
        st.altair_chart(chart, use_container_width=True)

# -- Top Games by Value --
@st.fragment
def top_value_games(steam_games):
    sidebar, spacer_col, main, buff_col = st.columns(VISUALIZATION_INNER_COL_LAYOUT)

    min_year = int(steam_games["Release Year"].min())
    max_year = int(steam_games["Release Year"].max())

    # Sidebar input (Release Year + Review Count)
    with sidebar:
        # Year Slider
        start_year, end_year = st.slider(
            "__Range of Release Years__",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key="value_year"
        )
        # Review Count Slider
        review_count = st.slider(
            "__Minimum No. of Reviews__",
            min_value=0,
            max_value=500000,
            value=0,
            key="value_review",
            step=10000
        )
        # Review Percent Range
        start_review_percent, end_review_percent = st.slider(
            "__Review Percent Range__",
            min_value=0,
            max_value=100,
            value=(0,100),
            key="value_review_percentage",
            step=1
        )
        # Price Number Input
        st.markdown("<p><b>Price Range</b><p>", unsafe_allow_html=True)
        col_min_price, col_max_price = st.columns(2)
        with col_min_price:
            start_price = st.number_input(
                "Min ($)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.01,
                format="%.2f",
                key="value_min_price_input"
            )
        with col_max_price:
            end_price = st.number_input(
                "Min ($)",
                min_value=start_price,
                max_value=100.0,
                value=100.0,
                step=0.01,
                format="%.2f",
                key="value_max_price_input"
            )

    # Release Year and Reviews Filter
    value_filter = steam_games[
        (steam_games["Release Year"] >= start_year) & (steam_games["Release Year"] <= end_year) &
        (steam_games["Reviews"] >= review_count) &
        (steam_games["Price"] >= start_price) & (steam_games["Price"] <= end_price) &
        (steam_games["Reviews Percentage"] >= start_review_percent) & (steam_games["Reviews Percentage"] <= end_review_percent)
    ]

    top_value = value_filter.dropna(subset=['Weighted Value']).sort_values(by="Weighted Value", ascending=False).head(20)

    # Color Coding
    price_scheme = COLOR_SCHEMES["price_scale"]

    # Altair Horizontal Bar Chart with Tooltip Features
    chart = alt.Chart(top_value).mark_bar().encode(
        x = alt.X("Weighted Value:Q", title="Value"),
        y = alt.Y('Name:N', sort='-x', title="Game Name"),
        color=alt.Color(
            "Price Category:N",
            title="Price Range",
            sort=price_scheme["order"],
            scale=alt.Scale(
                domain=price_scheme["order"],
                range=price_scheme["colors"]
            )
        ),tooltip=[
            "Name:N",
            alt.Tooltip("AppID", title="App ID"),
            alt.Tooltip("Reviews Percentage:Q", title="Review Percentage"),
            alt.Tooltip("Price:Q", title="Price", format="$.2f"),
            alt.Tooltip("Release date:T", title="Release Date"),
        ]
    ).properties(
        title=f"Top 20 Games by Value ({start_year}-{end_year})"
    )

    with main:
        st.altair_chart(chart, use_container_width=True)
