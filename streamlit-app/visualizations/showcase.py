import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

from constants.color_schemes import COLOR_SCHEMES
from constants.layout_configs import VISUALIZATION_INNER_COL_LAYOUT
from visualization_utils.altair_chart_helpers import *

# -- Top Games By Peak CCU --
@st.fragment
def top_games_ccu(steam_games):
    sidebar, spacer_col, main, buff_col = st.columns(VISUALIZATION_INNER_COL_LAYOUT)

    min_year = int(steam_games["Release Year"].min())
    max_year = int(steam_games["Release Year"].max())

    # Sidebar input (Release Year)
    with sidebar:
        start_year, end_year = st.slider(
            "__Release Years__",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key="peak_ccu_year"
        )
        start_review_percent, end_review_percent = st.slider(
            "__Review% Range__",
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

    # Creation of dataframe for charting
    top_ccu_games = year_filter.dropna(subset=['Peak CCU']).sort_values(by="Peak CCU", ascending=False).head(20)

    # Altair Horizontal Bar Chart with Tooltip Features
    chart = alt.Chart(top_ccu_games).mark_bar().encode(
        x = alt.X("Peak CCU:Q", title="Peak Concurrent Users"),
        y = alt.Y('Name:N', sort='-x', title="Game Name"),
        href="Steam_URL:N",
        color=price_color_getter(),
        tooltip=game_tooltip()
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

    # Variable Declaration
    min_year = int(steam_games["Release Year"].min())
    max_year = int(steam_games["Release Year"].max())

    # Sidebar input (Release Year + Review Count)
    with sidebar:
        # Year Slider
        start_year, end_year = st.slider(
            "__Release Years__",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key="value_year"
        )
        # Review Count Slider
        review_count = st.slider(
            "__Minimum Reviews__",
            min_value=0,
            max_value=500000,
            value=0,
            key="value_review",
            step=10000
        )
        # Review% Range
        start_review_percent, end_review_percent = st.slider(
            "__Review% Range__",
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

    # Creation of dataframe for charting
    top_value = value_filter.dropna(subset=['Weighted Value']).sort_values(by="Weighted Value", ascending=False).head(20)

    # Altair Horizontal Bar Chart with Tooltip Features
    chart = alt.Chart(top_value).mark_bar().encode(
        x = alt.X("Weighted Value:Q", title="Value"),
        y = alt.Y('Name:N', sort='-x', title="Game Name"),
        href="Steam_URL:N",
        color=price_color_getter(),
        tooltip=game_tooltip()
    ).properties(
        title=f"Top 20 Games by Value ({start_year}-{end_year})"
    )

    with main:
        st.altair_chart(chart, use_container_width=True)

# -- Sleeper Hit --
@st.fragment
def sleeper_games(steam_games):
    sidebar, spacer_col, main, buff_col = st.columns(VISUALIZATION_INNER_COL_LAYOUT)

    # Variable Declaration
    min_year = int(steam_games["Release Year"].min())
    max_year = int(steam_games["Release Year"].max())

    # Sidebar input (Release Year)
    with sidebar:
        # Year Slider
        start_year, end_year = st.slider(
            "__Release Years__",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key="sleeper_year"
        )

    sleeper_filter = steam_games[
        (steam_games["Reviews Percentage"] >= 90) &
        (steam_games["Release Year"] >= start_year) & (steam_games["Release Year"] <= end_year) &
        (steam_games["Reviews"] <= 2000) & (steam_games["Reviews"] > 0) &
        (steam_games["Peak CCU"] <= 2000) & (steam_games["Peak CCU"] > 100)
    ]

    # Creation of dataframe for charting
    top_sleeper_games = sleeper_filter.dropna(subset=["Reviews"]).sort_values(by=["Peak CCU", "Reviews Percentage"], ascending=False).head(20)

    # Altair Bar Chart with Tooltip Features
    chart = alt.Chart(top_sleeper_games).mark_bar().encode(
        x=alt.X("Reviews:Q", title="Reviews"),
        y=alt.Y("Name:N", sort='-x', title="Game Name"),
        href="Steam_URL:N",
        color=price_color_getter(),
        tooltip=game_tooltip()
    ).properties(
        title=f"Top 20 Sleeper Hit Games ({start_year}-{end_year})"
    )

    with main:
        st.altair_chart(chart, use_container_width=True)

# -- Game Pricing --
@st.fragment
def games_pricing(steam_games):
    sidebar, spacer_col, main, buff_col = st.columns(VISUALIZATION_INNER_COL_LAYOUT)

    # Variable Declaration
    min_year = int(steam_games["Release Year"].min())
    max_year = int(steam_games["Release Year"].max())

    # Sidebar input (Release Year)
    with sidebar:
        # Year Slider
        start_year, end_year = st.slider(
            "__Release Years__",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key="pricing_year"
        )    
        # Review Percentage Slider
        start_review_percentage, end_review_percentage = st.slider(
            "__Review% Range__",
            min_value=0,
            max_value=100,
            value=(0,100),
            step=1
        )

    # Release Year and Reviews Filter
    pricing_filter = steam_games[
        (steam_games["Release Year"] >= start_year) & (steam_games["Release Year"] <= end_year) &
        (steam_games["Reviews Percentage"] >= start_review_percentage) & (steam_games["Reviews Percentage"] <= end_review_percentage)
    ]

    # Creation of dataframe for charting
    pricing_distribution = pricing_filter.dropna(subset=["Price Category", "Is_Indie"])[
        ["Price Category", "Is_Indie"]
    ]

    # Aggregation for Faster visualization
    aggregated_data = pricing_distribution.groupby(['Price Category', 'Is_Indie']).size().reset_index(name="Count")
    total_counts_per_category = aggregated_data.groupby('Price Category')['Count'].transform('sum')
    aggregated_data['Proportion'] = (aggregated_data['Count'] / total_counts_per_category).fillna(0)

    # Stacked Bar Chart with Altair
    chart = alt.Chart(aggregated_data).mark_bar().encode(
        x=alt.X(
            "Price Category:O",
            title="Price Range",
            sort=COLOR_SCHEMES["price_scale"]["order"],
            axis=alt.Axis(labelAngle=-60, labelOverlap="greedy")
        ),
        y=alt.Y(
            "Count:Q",
            stack="normalize",
            axis=alt.Axis(format=".0%", title="Proportion of Games")
        ),
        color=indie_color_getter(),
        tooltip=[
            "Price Category:O",
            "Is_Indie:N",
            alt.Tooltip("Count:Q", title="Number of Games", format=",d"),
            alt.Tooltip("Proportion:Q", format=".1%", title="Proportion in Category")
        ]
    ).properties(
        title="Proportion of Indies vs Non Indies games by Price Range"
    )

    with main:
        st.altair_chart(chart, use_container_width=True)
