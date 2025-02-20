import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = Groq(api_key=os.getenv("groq_api_key"))

# Different story starts for each genre
GENRE_STARTS = {
    "Crime": "It's 11:00 pm on a winter night, you are standing next to a phone booth, you are witnessing a murder scene, and then the murderers see you standing behind the booth and watching the scene.",
    "Comedy": "You accidentally walk into a top-secret government meeting, but instead of being arrested, they mistake you for their new intern. Now, you must pretend to know what you're doing.",
    "Dark": "The last thing you remember is falling asleep in your bed, but now you wake up in an abandoned hospital with flickering lights and a note in your hand that says 'RUN'.",
    "Educational": "A renowned scientist just discovered a way to time travel, and you're the first volunteer to test the machine. However, something goes wrong, and you end up in the year 3024."
}

def generate_story(genre, story_history):
    
    start_story = GENRE_STARTS.get(genre, "A new adventure begins...")

    prompt = f"""
    Generate the continuation of this story:
    - Start of the story: {start_story}

    Step-by-step process:
    1. Analyze the query
    2. Give continuation of the story
    3. Provide 4 options (emotional, rational, diplomatic, angry types) for the continuation.

    - Follow this format: 
    1. Analysed the query: [detailed understanding]
    2. Story: [Generated story not more than 150 words]
    3. Options: [4 options numbered 1,2,3,4]
    
   
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192",
        temperature=0.3,
        max_tokens=600
    )
    
    story_segment = response.choices[0].message.content
    story_history.append(story_segment)
    
    # Extract options (assuming they are numbered 1,2,3,4)
    options = [line.strip() for line in story_segment.split("\n") if line.startswith(("1.", "2.", "3.", "4."))]
    
    return story_segment, options

def continue_story(story_history, selected_option):
    """
    Continues the story based on the selected option and provides new options.
    """
    full_story = "\n".join(story_history)
    
    prompt = f"""
    Continue the following story based on the user's choice:

    {full_story}

    Selected Option: "{selected_option}"

    - Continue the story while maintaining consistency.
    - Generate another four options for the user to choose from.
    """
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600
    )
    
    story_segment = response.choices[0].message.content
    story_history.append(story_segment)
    
    # Extract new options
    options = [line.strip() for line in story_segment.split("\n") if line.startswith(("1.", "2.", "3.", "4."))]
    
    return story_segment, options
