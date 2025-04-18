# import streamlit as st
# from story_engine import generate_story, continue_story

# if "selected_genre" not in st.session_state:
#     st.session_state.selected_genre = None
# if "story_history" not in st.session_state:
#     st.session_state.story_history = []
# if "story_options" not in st.session_state:
#     st.session_state.story_options = []
# if "choice_history" not in st.session_state:
#     st.session_state.choice_history = []  # Stores only chosen step and option name

# st.set_page_config(layout="wide", page_title="PSYCHEPLOT", page_icon="👾")

# st.title("👾 PSYCHEPLOT")
# st.header("Select your genre")


# if st.session_state.selected_genre is None:
#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         if st.button("Crime"):
#             st.session_state.selected_genre = "Crime"
#             story_segment, options = generate_story("Crime", st.session_state.story_history)
#             st.session_state.story_options = options

#     with col2:
#         if st.button("Comedy"):
#             st.session_state.selected_genre = "Comedy"
#             story_segment, options = generate_story("Comedy", st.session_state.story_history)
#             st.session_state.story_options = options

#     with col3:
#         if st.button("Dark"):
#             st.session_state.selected_genre = "Dark"
#             story_segment, options = generate_story("Dark", st.session_state.story_history)
#             st.session_state.story_options = options

#     with col4:
#         if st.button("Educational"):
#             st.session_state.selected_genre = "Educational"
#             story_segment, options = generate_story("Educational", st.session_state.story_history)
#             st.session_state.story_options = options

# if "step_count" not in st.session_state:
#     st.session_state.step_count = 0
# if "chosen_options" not in st.session_state:
#     st.session_state.chosen_options = []

# if st.session_state.selected_genre:
#     st.subheader(f"📖 Story Begins ({st.session_state.selected_genre} story):")
    
#     for i, segment in enumerate(st.session_state.story_history):
#         cleaned_segment = "\n".join([line for line in segment.split("\n") if not line.startswith(("1.", "2.", "3.", "4."))])
#         st.write(cleaned_segment)
        
#         if i < len(st.session_state.story_history) - 1:
#             st.divider()
    
#     if st.session_state.step_count < 6:
#         st.subheader("🔮 Choose the next step:")
        
#         for option in st.session_state.story_options:
#             if st.button(option):
#                 story_segment, options = continue_story(st.session_state.story_history, option)
#                 st.session_state.story_options = options
                
#                 # Store only step number and chosen option name
#                 st.session_state.choice_history.append({
#                     "step": st.session_state.step_count + 1,
#                     "chosen_option": option
#                 })
                
#                 st.session_state.chosen_options.append(option)
#                 st.session_state.step_count += 1
#                 st.rerun()
#     else:
#         st.subheader("📝 Your chosen path:")
#         for choice in st.session_state.choice_history:
#             st.write(f"**Step {choice['step']}:** {choice['chosen_option']}")





import streamlit as st
from story_engine import generate_story, continue_story, predict_personality

if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = None
if "story_history" not in st.session_state:
    st.session_state.story_history = []
if "story_options" not in st.session_state:
    st.session_state.story_options = []
if "choice_history" not in st.session_state:
    st.session_state.choice_history = []

st.set_page_config(layout="wide", page_title="PSYCHEPLOT", page_icon="👾")

st.title("👾 PSYCHEPLOT")
st.header("Select your genre")

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

if "step_count" not in st.session_state:
    st.session_state.step_count = 0
if "chosen_options" not in st.session_state:
    st.session_state.chosen_options = []

if st.session_state.selected_genre:
    st.subheader(f"📖 Story Begins ({st.session_state.selected_genre} story):")
    for i, segment in enumerate(st.session_state.story_history):
        cleaned_segment = "\n".join([line for line in segment.split("\n") if not line.startswith(("1.", "2.", "3.", "4."))])
        st.write(cleaned_segment)
        if i < len(st.session_state.story_history) - 1:
            st.divider()
    
    if st.session_state.step_count < 6:
        st.subheader("🔮 Choose the next step:")
        for option in st.session_state.story_options:
            if st.button(option):
                story_segment, options = continue_story(st.session_state.story_history, option)
                st.session_state.story_options = options
                st.session_state.choice_history.append({
                    "step": st.session_state.step_count + 1,
                    "chosen_option": option
                })
                st.session_state.chosen_options.append(option)
                st.session_state.step_count += 1
                st.rerun()
    else:
        choices_text = "\n".join([f"Step {choice['step']}: {choice['chosen_option']}" for choice in st.session_state.choice_history])
        
        st.subheader("🔍 Predicted Personality Type:")
        personality_type = predict_personality(choices_text)
        st.write(personality_type)
        st.write(choices_text)
