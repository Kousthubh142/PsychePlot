import streamlit as st
import os
from dotenv import load_dotenv
from story_engine import generate_story, continue_story
from model import predict_personality

# Load environment variables and set up API key first
load_dotenv()

# Get API key - handle both local development and Hugging Face Spaces
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ API Key not found. Please check your environment configuration.")
    st.stop()

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

# Initialize session state variables
if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = None
if "story_history" not in st.session_state:
    st.session_state.story_history = []
if "story_options" not in st.session_state:
    st.session_state.story_options = []
if "choice_history" not in st.session_state:
    st.session_state.choice_history = []
    
# Track trait counts across choices
if "trait_counts" not in st.session_state:
    st.session_state.trait_counts = {
        "O": 0,  # Openness
        "C": 0,  # Conscientiousness
        "E": 0,  # Extraversion
        "A": 0,  # Agreeableness
        "N": 0   # Neuroticism
    }
    
# Track personality predictions for each step
if "personality_history" not in st.session_state:
    st.session_state.personality_history = []

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

def update_personality_traits(choice_text):
    """Update trait counts based on the current choice"""
    result = predict_personality(choice_text)
    st.session_state.personality_history.append(result)
    
    # Custom thresholds for each trait
    thresholds = {
        "O": 0.20,  # Openness
        "C": 0.20,  # Conscientiousness
        "E": 0.15,  # Extraversion
        "A": 0.15,  # Agreeableness
        "N": 0.30   # Higher threshold for Neuroticism
    }
    
    # Update trait counts with custom thresholds
    for trait, score in result["traits"].items():
        if score >= thresholds[trait]:
            st.session_state.trait_counts[trait] += 1
    
    return result

def get_final_personality():
    """Calculate final personality based on accumulated trait counts"""
    from model import PERSONALITY_MAP, DOMINANT_TYPES
    traits = ["O", "C", "E", "A", "N"]
    trait_scores = {}
    
    # Calculate scores
    for trait in traits:
        count = st.session_state.trait_counts[trait]
        score = count / st.session_state.step_count
        trait_scores[trait] = score
    
    # Find potential dominant traits
    max_score = max(trait_scores.values())
    dominant_candidates = [
        trait for trait, score in trait_scores.items()
        if abs(score - max_score) < 0.01
    ]
    
    # Check if there's a clear dominant trait
    if len(dominant_candidates) == 1:
        dominant_trait = dominant_candidates[0]
        other_scores = [score for trait, score in trait_scores.items() 
                       if trait != dominant_trait]
        max_other = max(other_scores)
        
        if max_score >= 0.5 and (max_score - max_other) >= 0.2:
            profile = DOMINANT_TYPES[dominant_trait]
            return {
                "type": dominant_trait,
                "category": "Dominant Trait",
                "label": profile["label"],
                "description": profile["description"],
                "traits": trait_scores
            }
    
    # If no clear dominant trait, create binary code and use personality map
    binary_code = "".join(["H" if trait_scores[trait] > 0.3 else "L" 
                          for trait in traits])
    
    profile = PERSONALITY_MAP.get(binary_code, {
        "label": "Unique Profile",
        "description": "A distinctive combination of personality traits that creates a unique character profile."
    })
    
    return {
        "type": binary_code,
        "category": "Mixed Profile",
        "label": profile["label"],
        "description": profile["description"],
        "traits": trait_scores
    }

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
                
                # Store the choice
                st.session_state.choice_history.append({
                    "step": st.session_state.step_count + 1,
                    "chosen_option": option
                })
                st.session_state.chosen_options.append(option)
                
                # Update personality prediction after this choice
                choice_text = f"Step {st.session_state.step_count + 1}: {option}"
                update_personality_traits(choice_text)
                
                st.session_state.step_count += 1
                st.rerun()
    else:
        # Final personality calculation based on accumulated trait counts
        result = get_final_personality()

        st.subheader("🧠 Final Personality Assessment:")
        st.markdown(f"**Type:** `{result['type']}` ({result['category']})")
        st.markdown(f"**Label:** {result['label']}")
        st.markdown("**Description:**")
        st.write(result['description'])

        st.divider()
        st.markdown("### 📊 Trait Breakdown")
        for trait, score in result["traits"].items():
            count = st.session_state.trait_counts[trait]
            st.progress(score, text=f"{trait}: {score:.2f} ({count}/{st.session_state.step_count} choices)")

        # Show choices
        st.divider()
        with st.expander("📜 Your Story Choices"):
            choices_text = "\n".join([f"Step {choice['step']}: {choice['chosen_option']}" for choice in st.session_state.choice_history])
            st.text(choices_text)
        
        # Show personality evolution
        with st.expander("📈 Personality Evolution"):
            for i, personality in enumerate(st.session_state.personality_history):
                st.markdown(f"**Step {i+1}**: {personality['type']} - {personality['label']}")
                cols = st.columns(5)
                for j, (trait, score) in enumerate(personality['traits'].items()):
                    with cols[j]:
                        st.progress(score, text=f"{trait}: {score:.2f}")