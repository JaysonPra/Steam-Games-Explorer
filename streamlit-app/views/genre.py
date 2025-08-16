import streamlit as st
import altair as alt
import pandas as pd

from utils import get_unique_genres
from visualization_utils.altair_chart_helpers import *
from constants.color_schemes import COLOR_SCHEMES

# Genre Filter
def filter_by_genre(df, genre_selections):
    return df[df["Genre List"].apply(
        lambda game_genres_list: all(g in game_genres_list for g in genre_selections)
    )].copy()

# Genre Yearly Picks Visualization
def genre_yearly_picks(df):
    df.dropna(subset=['Release Year', 'Peak CCU'], inplace=True)
    df = df[df['Release Year'] >= 1997]

    genre_growth_df = df.groupby('Release Year')['Peak CCU'].sum().reset_index()
    genre_growth_df.rename(columns={'Peak CCU': 'Total Peak CCU'}, inplace=True)

    chart_title = "Total Played Games for Selected Genres by Release Date"

    col1, col2 = st.columns(2)

    with col1:
        # Displays the line chart with points
        line_chart = alt.Chart(genre_growth_df).mark_line(point=True).encode(
            x = alt.X("Release Year:O", axis=alt.Axis(format='d', title="Year")),
            y = alt.Y("Total Peak CCU:Q", title='Total Peak Concurrent Users'),
            tooltip=[
                alt.Tooltip('Release Year:O', title="Year"),
                alt.Tooltip('Total Peak CCU:Q', title="Total Players", format=",")
            ]
        ).properties(
            title = chart_title
        )
        
        st.altair_chart(line_chart, use_container_width=True)

    with col2:
        year_selection = st.selectbox(
            label="Select a Release Year",
            options=genre_growth_df["Release Year"],
            label_visibility="collapsed",
            index= len(genre_growth_df) - 1
        )

        filtered_year_df = df[
            df["Release Year"] == year_selection
        ]

        filtered_year_df = filtered_year_df.sort_values(by="Peak CCU", ascending=False).head(10)

        top_10_chart = alt.Chart(filtered_year_df).mark_bar().encode(
            x=alt.X('Peak CCU:Q', title="Peak Concurrent Players"),
            y=alt.Y('Name:N', sort="-x", title="Game Name"),
            href="Steam_URL:N",
            tooltip=game_tooltip(),
            color=price_color_getter()
        ).properties(
            title=f"Top 10 Games of the Selected Genres by Peak CCU ({year_selection})"
        )

        st.altair_chart(top_10_chart, use_container_width=True)

# Genre Pricing Trend
def genre_pricing(df):
    # Pricing Counting
    price_counts = df["Price Category"].value_counts().reset_index()
    price_counts.columns = ["Price Category", "Count"]

    chart_title = "Genre Pricing Trend"

    selection = alt.selection_point(
        fields=["Price Category"],
        name="price_category_selection",
        on="click",
        clear="dblclick"
    )

    col1, col2 = st.columns(2)

    with col1:
        chart = alt.Chart(price_counts).mark_bar().encode(
            x=alt.X('Price Category:N', sort=COLOR_SCHEMES['price_scale']['order'], title="Price Category"),
            y=alt.Y("Count:Q", title="Count")
        ).properties(
            title=chart_title
        ).add_params(
            selection
        )

        selection_data = st.altair_chart(
            chart,
            use_container_width=True,
            on_select="rerun",
            key="genre_pricing_chart"
        )

    with col2:
        if selection_data.selection["price_category_selection"]:
            selected_price_category = selection_data.selection["price_category_selection"][0]["Price Category"]

            filtered_df = df[df["Price Category"] == selected_price_category].copy()
            
            exploded_df = filtered_df.explode("Genre List")

            genre_counts = exploded_df["Genre List"].value_counts().reset_index().head(10)
            genre_counts.columns = ["Genre", "Count"]

            chart2 = alt.Chart(genre_counts).mark_bar().encode(
                x=alt.X("Count:Q", title="Number of Titles"),
                y=alt.Y("Genre:N", sort="-x", title="Genre"),
                tooltip=["Genre", "Count"]
            ).properties(
                title=f"Top 5 Genres in '{selected_price_category}' Category"
            )

            st.altair_chart(chart2, use_container_width=True)
        else:
            st.info("Select a price category from the chart on the left to see the genre breakdown.")

# Genre Indie Number
def genre_indie(df):
    # Filter the DataFrame to include only indie games
    indie_df = df[df['Is_Indie'] == 'Indie'].copy()
    
    # Count the number of indie games for each release year
    indie_counts = indie_df['Release Year'].value_counts().reset_index()
    indie_counts.columns = ['Release Year', 'Count']
    
    indie_counts = indie_counts.sort_values('Release Year')

    chart_title = "Number of Indie Games Released Per Year"

    # Define a selection for the first chart
    selection = alt.selection_point(
        fields=['Release Year'],
        name="year_selection",
        on="click",
        clear="dblclick"
    )

    col1, col2 = st.columns(2)
    with col1:
        chart1 = alt.Chart(indie_counts).mark_bar().encode(
            x=alt.X('Release Year:O', axis=alt.Axis(format="d", title="Release Year")),
            y=alt.Y("Count:Q", title="Number of Indie Games"),
            tooltip=[
                alt.Tooltip('Release Year', title='Year'), 
                alt.Tooltip('Count', title='Number of Titles')
            ]
        ).properties(
            title=chart_title
        ).add_params(
            selection
        )
        
        selection_data = st.altair_chart(
            chart1,
            use_container_width=True,
            on_select="rerun",
            key="genre_indie_chart"
        )

    with col2:
        if selection_data.selection is not None and "year_selection" in selection_data.selection and selection_data.selection["year_selection"]:
            # Get the selected year
            selected_year = selection_data.selection["year_selection"][0]["Release Year"]
            
            # Filter the df for the selected year and indie games
            top_games_df = df[
                (df["Release Year"] == selected_year) & 
                (df["Is_Indie"] == "Indie")
            ].copy()
            
            top_games_df = top_games_df.sort_values(by="Peak CCU", ascending=False).head(10)
            
            if not top_games_df.empty:
                chart2 = alt.Chart(top_games_df).mark_bar().encode(
                    x=alt.X("Peak CCU:Q", title="Peak Concurrent Users (CCU)"),
                    y=alt.Y("Name:N", sort="-x", title="Game Title"),
                    href="Steam_URL:N",
                    tooltip=game_tooltip()
                ).properties(
                    title=f"Top 10 Indie Games by Peak CCU"
                )
                
                st.altair_chart(chart2, use_container_width=True)
        else:
            st.info("Click on a bar in the chart on the left to see the top indie games for that year.")

# Genre Saturation Chart
def genre_saturation(df):
    df = df[
        (df["Reviews"] >= 100)
    ]
    saturation_counts = df.groupby('Release Year').size().reset_index(name='Count')
    
    chart_title = "Genre Saturation Over Time (100+ Reviews Games)"
    
    col1, col2 = st.columns(2)
    with col1:
        chart = alt.Chart(saturation_counts).mark_line(point=True).encode(
            x=alt.X('Release Year:O', axis=alt.Axis(title="Release Year", format="d")),
            y=alt.Y("Count:Q", title="Number of Releases"),
            tooltip=[
                alt.Tooltip('Release Year', title='Year'),
                alt.Tooltip('Count', title='Number of Titles')
            ]
        ).properties(
            title=chart_title
        )

        st.altair_chart(chart, use_container_width=True)
    with col2:
        st.info("2025 will show low saturation due to the dataset being last updated in April 2025.")

# Builder for the Genre Selector Page
@st.fragment
def genre_selector_builder(steam_games):
    # Columns for Sidebar(Filters) and Main(Visualizations)
    sidebar, main = st.columns([1,5])
    with sidebar:
        unique_genres = get_unique_genres(steam_games)

        genre_selections = st.multiselect(
            label="Select 1 or More Genres",
            options=unique_genres,
            width="stretch"
        )

    # Filtering by selected genres
    if genre_selections:
        filtered_df = filter_by_genre(steam_games, genre_selections)

    with main:
        tab1, tab2, tab3, tab4 = st.tabs(["Yearly Genre Picks", "Genre Pricing" ,"Indie Number", "Genre Saturation"])
        with tab1:
            if genre_selections:
                genre_yearly_picks(filtered_df)
        with tab2:
            if genre_selections:
                genre_pricing(filtered_df)
        with tab3:
            if genre_selections:
                genre_indie(filtered_df)
        with tab4:
            if genre_selections:
                genre_saturation(filtered_df)