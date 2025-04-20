import joblib
import json
import re

# Load the models
rf_model = joblib.load("personality_rf_model.joblib")
vectorizer = joblib.load("tfidf_vectorizer.joblib")
label_encoder = joblib.load("label_encoder.joblib")

# Load personality profiles
with open("personality_profiles.json", "r") as f:
    PERSONALITY_MAP = json.load(f)

# Define dominant types
DOMINANT_TYPES = {
    "O": {
        "label": "High Openness",
        "description": "Curious, imaginative, and open to new experiences. Thrives in creative and unconventional environments."
    },
    "C": {
        "label": "High Conscientiousness",
        "description": "Organized, dependable, and goal-oriented. Strong sense of duty and self-discipline."
    },
    "E": {
        "label": "High Extraversion",
        "description": "Energetic, outgoing, and thrives on social interaction. Feeds off external stimulation."
    },
    "A": {
        "label": "High Agreeableness",
        "description": "Kind-hearted, empathetic, and cooperative. Seeks harmony and avoids conflict."
    },
    "N": {
        "label": "High Neuroticism",
        "description": "Emotionally sensitive, reactive, and prone to mood swings. Deeply introspective."
    }
}

def preprocess_text(text):
    """Preprocess text for prediction"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def predict_personality(choices_text):
    """Predict personality based on choices text"""
    try:
        # Extract choice numbers from the text
        choices = re.findall(r'Step \d+: (\d+)\.', choices_text)
        
        # Define trait mapping for each option number
        trait_mapping = {
            "1": "O",  # Openness
            "2": "C",  # Conscientiousness
            "3": "E",  # Extraversion/Agreeableness
            "4": "N"   # Neuroticism
        }
        
        # Initialize trait counts
        trait_counts = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
        total_choices = len(choices)
        
        # Count traits based on choices
        for choice in choices:
            if choice in trait_mapping:
                trait = trait_mapping[choice]
                trait_counts[trait] += 1
                # Special case: option 3 contributes to both E and A
                if choice == "3":
                    trait_counts["A"] += 0.5  # Reduced weight for secondary trait
        
        # Calculate trait scores as percentages
        trait_scores = {
            trait: count/total_choices 
            for trait, count in trait_counts.items()
        } if total_choices > 0 else trait_counts
        
        # Find dominant trait(s) with stricter criteria
        max_score = max(trait_scores.values())
        
        # Count traits that share the max score
        max_score_traits = [
            trait for trait, score in trait_scores.items() 
            if abs(score - max_score) < 0.01  # Account for floating point comparison
        ]
        
        # Only consider dominant if:
        # 1. Single trait has highest score
        # 2. Score is significantly higher than others (>= 0.5)
        # 3. No other trait is close to the max score
        if len(max_score_traits) == 1 and max_score >= 0.5:
            dominant_trait = max_score_traits[0]
            other_scores = [score for trait, score in trait_scores.items() 
                          if trait != dominant_trait]
            max_other = max(other_scores) if other_scores else 0
            
            if max_score - max_other >= 0.2:  # Must be significantly higher
                profile = DOMINANT_TYPES[dominant_trait]
                return {
                    "type": dominant_trait,
                    "category": "Dominant Trait",
                    "label": profile["label"],
                    "description": profile["description"],
                    "traits": trait_scores
                }

        # If no clear dominant trait, use binary code
        binary_code = "".join(["H" if trait_scores[trait] > 0.3 else "L" 
                              for trait in ["O", "C", "E", "A", "N"]])  # Fixed order
        
        # Get profile from personality map
        profile = PERSONALITY_MAP.get(binary_code, {
            "label": "Mixed Profile",
            "description": "A balanced combination of different personality traits."
        })
        
        return {
            "type": binary_code,
            "category": "Mixed Profile",
            "label": profile["label"],
            "description": profile["description"],
            "traits": trait_scores
        }
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {
            "type": "ERROR",
            "category": "Error",
            "label": "Prediction Error",
            "description": str(e),
            "traits": {}
        }

# if __name__ == "__main__":
#     example_text = "I enjoy meeting new people and trying new experiences"
#     result = predict_personality(example_text)
#     print(json.dumps(result, indent=2))