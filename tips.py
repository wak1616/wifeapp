from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_tip(topic):
    token = os.getenv("HUGGING_FACE_TOKEN")
    if not token:
        raise ValueError("HUGGING_FACE_TOKEN environment variable is not set")
        
    client = InferenceClient(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        token=token
    )
    
    prompt = f"Provide a specific, practical tip on {topic} that can be implemented today. Explain it in a few sentences."
    
    response = client.text_generation(
        prompt,
        max_new_tokens=150,
        temperature=0.9,  # Increase for more randomness
        top_p=0.9,        # Nucleus sampling for diversity
        repetition_penalty=1.2
    )
    
    return response.strip()

def get_nutrition_tip():
    return get_tip("nutrition and healthy eating")

def get_parenting_tip():
    return get_tip("parenting")

if __name__ == "__main__":
    print("Getting nutrition tip...")
    print("-" * 40)
    print(get_nutrition_tip())
    print("\nGetting parenting tip...")
    print("-" * 40)
    print(get_parenting_tip())