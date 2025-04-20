
import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Get API key - handle both local development and Hugging Face Spaces
try:
    # Try to get from Streamlit secrets (Hugging Face Spaces)
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    # Fallback to local .env file
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise Exception("GROQ API Key not found. Please check your environment configuration.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Different story starts for each genre
GENRE_STARTS = {
    "Crime": "It's 11:00 pm on a winter night, you are standing next to a phone booth, you are witnessing a murder scene, and then the murderers see you standing behind the booth and watching the scene.",
    "Comedy": "You accidentally walk into a top-secret government meeting, but instead of being arrested, they mistake you for their new intern. Now, you must pretend to know what you're doing.",
    "Dark": "The last thing you remember is falling asleep in your bed, but now you wake up in an abandoned hospital with flickering lights and a note in your hand that says 'RUN'.",
    "Educational": "A renowned scientist just discovered a way to time travel, and you're the first volunteer to test the machine. However, something goes wrong, and you end up in the year 3024."
}

def generate_story(genre, story_history):
    try:
        start_story = GENRE_STARTS.get(genre, "A new adventure begins...")
        prompt = f"""
        Write a story continuation and provide 4 options that map to specific personality traits:
        Story start: {start_story}

        Format:
        [STORY]
        Write the story continuation here (max 150 words)

        [OPTIONS]
        1. An option showing openness (creative, exploratory approach)
        2. An option showing conscientiousness (methodical, careful approach)
        3. An option showing extraversion and agreeableness (social, cooperative approach)
        4. An option showing neuroticism (emotional, cautious approach)

        Important: Present the options naturally without mentioning these traits explicitly.
        Each option should be a natural story choice while subtly reflecting its trait.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=800
        )
        
        content = response.choices[0].message.content
        
        # Split content into story and options
        parts = content.split("[OPTIONS]")
        if len(parts) == 2:
            story = parts[0].replace("[STORY]", "").strip()
            options_text = parts[1].strip()
            options = [line.strip() for line in options_text.split("\n") if line.strip().startswith(("1.", "2.", "3.", "4."))]
        else:
            story = content
            options = ["Continue the story", "Ask for help", "Take a different path", "Wait and observe"]
        
        story_history.append(story)
        return story, options
        
    except Exception as e:
        print(f"Error generating story: {e}")
        return "An error occurred while generating the story. Please try again.", ["Retry", "Choose different genre", "Start over", "Get help"]

def continue_story(story_history, selected_option):
    try:
        full_story = "\n".join(story_history)
        prompt = f"""
        Previous story: {full_story}
        Chosen action: {selected_option}

        Continue the story based on the chosen action.
        Provide 4 new options that map to:
        - Option 1: Openness (innovative, creative solutions)
        - Option 2: Conscientiousness (careful planning, responsibility)
        - Option 3: Extraversion/Agreeableness (social interaction, cooperation)
        - Option 4: Neuroticism (emotional awareness, caution)

        Format:
        [STORY]
        Write the continuation here (max 150 words)

        [OPTIONS]
        Present 4 natural story options that subtly reflect these traits without explicitly mentioning them.
        Make each option feel like a natural choice in the story.
        """
        
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        
        content = response.choices[0].message.content
        
        # Split content into story and options
        parts = content.split("[OPTIONS]")
        if len(parts) == 2:
            story = parts[0].replace("[STORY]", "").strip()
            options_text = parts[1].strip()
            options = [line.strip() for line in options_text.split("\n") if line.strip().startswith(("1.", "2.", "3.", "4."))]
        else:
            story = content
            options = ["Continue forward", "Take a different approach", "Reconsider the situation", "Try something new"]
        
        story_history.append(story)
        return story, options
        
    except Exception as e:
        print(f"Error continuing story: {e}")
        return "An error occurred while continuing the story. Please try again.", ["Retry", "Go back", "Choose different option", "Start over"]

# def predict_personality(choices_text):
#     prompt = f"""
#     Analyze the following choices made by the user and determine their personality type:
    
#     Choices:
#     {choices_text}
    
#     The choices are labeled as follows:
#     1. Emotional
#     2. Rational
#     3. Diplomatic
#     4. Angry
    
#     Based on the frequency and pattern of choices, predict the user's personality type.
#     Give a short summary of their personality traits.
    
#     ### Give me only output
#     """
    
#     response = client.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3,
#         max_tokens=300
#     )
    
#    return response.choices[0].message.content


