# PSYCHEPLOT

Interactive storytelling application with personality analysis.

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add GROQ API key to Hugging Face Spaces secrets

## Files
- `app.py`: Main Streamlit application
- `story_engine.py`: Story generation logic
- `model.py`: Personality prediction model
- `personality_profiles.json`: Personality type definitions

## Models
Make sure these files are included in the repository:
- personality_rf_model.joblib
- tfidf_vectorizer.joblib
- label_encoder.joblib

## Features
- Multiple story genres
- Dynamic story generation
- Personality analysis
- Real-time trait tracking