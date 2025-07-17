import streamlit as st
import time

# Comments written by AI because I am lazy

# Initialize session state flags
if "landing_played" not in st.session_state:
    st.session_state.landing_played = False

if "page" not in st.session_state:
    st.session_state.page = "home"

# Landing page content
landing = """
# 🎮 Steam Game Explorer

Welcome to **Steam Game Explorer** — your interactive data-driven app with over 100,000 Steam Games.

🔍 **Filter** games by genre, release date, and more. Find the game you want to play  
🏆 **Visualize** top-rated games, most-played games, and more  
🗂️ **Select** genres and discover trends

*Built by Jayson Pradhananga, using Streamlit 💻*
"""

# Stream the generator character by character only once per session
def landing_generator():    
    for char in landing:
        yield char
        time.sleep(0.02)

if not st.session_state.landing_played:
    st.write_stream(landing_generator)
    st.session_state.landing_played = True

# 3 navigation buttons
st.markdown("---")
col1, col2, col3 = st.columns(3)

# Navigation button: Explore Games
with col1:
    if st.button("🔍 Explore Games"):
        st.session_state.page = "explore"
        st.session_state.landing_played = False

# Navigation button: Game Showcase
with col2:
    if st.button("🏆 Game Showcase"):
        st.session_state.page = "showcase"
        st.session_state.landing_played = False

# Navigation button: Genre Selector
with col3:
    if st.button("🗂️ Genre Selector"):
        st.session_state.page = "genre_selector"
        st.session_state.landing_played = False

# Navigate to selected page
if st.session_state.page == "explore":
    st.session_state.page = "home"
    st.session_state.landing_played = False
    st.switch_page("Pages/game_explorer.py")
    
elif st.session_state.page == "showcase":
    st.session_state.page = "home"
    st.session_state.landing_played = False
    st.switch_page("Pages/game_showcase.py")
    
elif st.session_state.page == "genre_selector":
    st.session_state.page = "home"
    st.session_state.landing_played = False
    st.switch_page("Pages/genre_selector.py")
