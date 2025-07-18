import streamlit as st
import time

# Page Config
st.set_page_config(
    page_title="Steam Explorer",
    page_icon="🎮",
    layout="centered"
)

# Session state to ensure the stream only runs once
if "landing_stream_finished" not in st.session_state:
    st.session_state.landing_stream_finished = False

# Landing page content
landing_text = """
# 🎮 Steam Game Explorer

Welcome to **Steam Game Explorer** — your interactive data-driven app with over 100,000 Steam Games.  

🔍 **Filter** games by genre, release date, and more. Find the game you want to play  
🏆 **Visualize** top-rated games, most-played games, and more  
🗂️ **Select** genres and discover trends

*Built by Jayson Pradhananga, using Streamlit 💻*
"""

# Stream the generator character by character only once per session
def landing_generator():
    for char in landing_text:
        yield char
        time.sleep(0.02)
    st.session_state.landing_stream_finished = True

if not st.session_state.landing_stream_finished:
    st.write_stream(landing_generator())
else:
    st.markdown(landing_text)

st.markdown("---")
st.markdown("### Choose your path to explore:")

# 3 navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("Pages/game_explorer.py", label="🔍 Explore Games")

with col2:
    st.page_link("Pages/game_showcase.py", label="🏆 Game Showcase")

with col3:
    st.page_link("Pages/genre_selector.py", label="🗂️ Genre Selector")
