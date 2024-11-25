from huggingface_hub import InferenceClient
import os
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# List of different aspects to rotate through
NUTRITION_ASPECTS = [
    "meal planning",
    "healthy snacking",
    "portion control",
    "hydration",
    "vegetable intake",
    "protein sources",
    "healthy breakfast ideas",
    "mindful eating",
    "food preparation",
    "balanced meals"
]

PARENTING_ASPECTS = [
    "positive discipline",
    "bedtime routines",
    "quality time",
    "emotional support",
    "communication skills",
    "learning activities",
    "building confidence",
    "managing tantrums",
    "establishing boundaries",
    "encouraging independence"
]

def get_tip(topic, aspects_list):
    token = os.getenv("HUGGING_FACE_TOKEN")
    if not token:
        raise ValueError("HUGGING_FACE_TOKEN environment variable is not set")
    
    # Use today's date to select a different aspect each day
    day_of_year = datetime.now().timetuple().tm_yday
    aspect = aspects_list[day_of_year % len(aspects_list)]
    
    client = InferenceClient(
        model="meta-llama/Llama-3.2-3B-Instruct",
        token=token
    )
    
    prompt = f"""As an expert in {topic}, provide a unique and specific tip about {aspect}.
    The tip should be practical, implementable today, and thought provoking.
    Focus on actionable steps and immediate benefits.
    Current date: {datetime.now().strftime('%Y-%m-%d')}
    Random seed: {random.randint(1, 1000)}"""
    
    response = client.text_generation(
        prompt,
        max_new_tokens=1500,
        temperature=0.7,  # Slightly increased for more variety
        top_p=0.9,
        repetition_penalty=1.2,
        seed=day_of_year  # Use day of year as seed for consistency within the day
    )
    
    return response.strip()

def get_nutrition_tip():
    return get_tip("nutrition and healthy eating", NUTRITION_ASPECTS)

def get_parenting_tip():
    return get_tip("parenting", PARENTING_ASPECTS)

if __name__ == "__main__":
    print("Getting nutrition tip...")
    print("-" * 40)
    print(get_nutrition_tip())
    print("\nGetting parenting tip...")
    print("-" * 40)
    print(get_parenting_tip())