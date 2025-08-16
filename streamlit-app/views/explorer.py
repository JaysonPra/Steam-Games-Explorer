import streamlit as st
import math
import pandas as pd

@st.fragment
def game_explorer(df):
    st.title("🎮 Game Explorer")
    
    # Initializing page number to 1
    if 'page' not in st.session_state:
        st.session_state.page = 1

    filtered_df = df.copy()

    col1, col2 = st.columns([1, 4])

    with col1:
        st.header("Filters & Sort")
        
        # Creating form for Filtering and Sorting
        with st.form(key='filter_form'):
            # -- Sorting --
            sort_options = {
                "Reviews": "Reviews",
                "Reviews Percentage": "Reviews Percentage",
                "Price": "Price",
                "Peak CCU": "Peak CCU"
            }
            sort_by = st.selectbox("Sort by", options=list(sort_options.keys()))
            sort_order = st.radio("Order", ["Descending", "Ascending"])

            # -- Filtering --
            game_name = st.text_input("Search by name", placeholder="e.g., Cyberpunk 2077")
            
            all_genres = sorted(list(set([genre for sublist in df['Genre List'] for genre in sublist])))
            selected_genres = st.multiselect("Select Genres", options=all_genres)
            
            min_rating, max_rating = st.slider("Reviews Percentage", min_value=0, max_value=100, value=(0, 100), step=1)
            
            min_reviews = st.number_input("Minimum Reviews", min_value=0, step=100)

            min_price = st.number_input("Minimum Price ($)", min_value=0.0, step=0.01)
            max_price = st.number_input("Maximum Price ($)", min_value=0.0, step=0.01, value=float(100))

            st.form_submit_button("Apply Filters", type="primary")
            
    # Applying filters
    if game_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(game_name, case=False, na=False)]
    if selected_genres:
        filtered_df = filtered_df[filtered_df['Genre List'].apply(lambda x: all(genre in x for genre in selected_genres))]
    filtered_df = filtered_df[(filtered_df['Reviews Percentage'] >= min_rating) & (filtered_df['Reviews Percentage'] <= max_rating)]
    filtered_df = filtered_df[(filtered_df['Reviews'] >= min_reviews)]
    filtered_df = filtered_df[(filtered_df['Price'] >= min_price) & (filtered_df['Price'] <= max_price)]

    # Apply sorting after filtering
    ascending = sort_order == "Ascending"
    filtered_df = filtered_df.sort_values(by=sort_options[sort_by], ascending=ascending)

    with col2:
        st.subheader("Results")
        
        # -- Page Logic --
        games_per_page = 20
        total_games = len(filtered_df)
        total_pages = math.ceil(total_games / games_per_page)

        start_index = (st.session_state.page - 1) * games_per_page
        end_index = start_index + games_per_page
        paginated_df = filtered_df.iloc[start_index:end_index]
        
        # Display page info
        st.markdown(f"**Found {total_games} games.**")

        if paginated_df.empty:
            st.info("No games match your filters. Please adjust your selections.")
        else:
            for index, row in paginated_df.iterrows():
                with st.container(border=True):
                    game_col1, game_col2 = st.columns([1, 3])
                    
                    with game_col1:
                        if pd.notna(row['Header image']) and row['Header image']:
                            st.image(row['Header image'], use_container_width=True)
                        else:
                            st.write("No Image Available")
                    
                    with game_col2:
                        st.markdown(f"**[{row['Name']}]({row['Steam_URL']})**")
                        st.markdown(f"**Reviews:** {row['Reviews Percentage']}% ({row['Reviews']})")
                        st.markdown(f"**Price:** ${row['Price']:.2f}")

        # Page Buttons
        page_col1, page_col2, page_col3 = st.columns([1, 2, 1])
        with page_col1:
            if st.session_state.page > 1:
                if st.button("Previous"):
                    st.session_state.page -= 1
                    st.rerun()
        with page_col2:
            st.markdown(f"<div style='text-align:center;'>Page <b>{st.session_state.page}</b> of <b>{total_pages}</b></div>", unsafe_allow_html=True)
        with page_col3:
            if st.session_state.page < total_pages:
                if st.button("Next"):
                    st.session_state.page += 1
                    st.rerun()