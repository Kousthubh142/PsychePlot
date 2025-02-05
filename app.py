import streamlit as st
from story_engine import generate_story, continue_story

# Initialize session state
if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = None
if "story_history" not in st.session_state:
    st.session_state.story_history = []
if "story_options" not in st.session_state:
    st.session_state.story_options = []

# Streamlit UI
st.set_page_config(layout="wide", page_title="PSYCHEPLOT", page_icon="👾")

st.title("👾 PSYCHEPLOT")
st.header("Select your genre")

# Show genre selection only if no genre is selected
if st.session_state.selected_genre is None:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Crime"):
            st.session_state.selected_genre = "Crime"
            story_segment, options = generate_story("Crime", st.session_state.story_history)
            st.session_state.story_options = options

    with col2:
        if st.button("Comedy"):
            st.session_state.selected_genre = "Comedy"
            story_segment, options = generate_story("Comedy", st.session_state.story_history)
            st.session_state.story_options = options

    with col3:
        if st.button("Dark"):
            st.session_state.selected_genre = "Dark"
            story_segment, options = generate_story("Dark", st.session_state.story_history)
            st.session_state.story_options = options

    with col4:
        if st.button("Educational"):
            st.session_state.selected_genre = "Educational"
            story_segment, options = generate_story("Educational", st.session_state.story_history)
            st.session_state.story_options = options

# Display selected genre's story progression
if st.session_state.selected_genre:
    st.subheader(f"📖 Story Progression ({st.session_state.selected_genre}):")
    
    for segment in st.session_state.story_history:
        st.write(segment)
    
    st.subheader("🔮 Choose the next step:")
    for option in st.session_state.story_options:
        if st.button(option):
            story_segment, options = continue_story(st.session_state.story_history, option)
            st.session_state.story_options = options
            st.rerun()  
