from huggingface_hub import InferenceClient
import random
import os
from dotenv import load_dotenv

load_dotenv()

def get_nutrition_tip():
    # Get token from environment variable
    token = os.getenv("HUGGING_FACE_TOKEN")
    if not token:
        raise ValueError("HUGGING_FACE_TOKEN environment variable is not set")
        
    client = InferenceClient(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        token=token
    )
    prompt = f"Provide a brief and useful tip related to healthy eating or nutrition. [Run ID: {random.randint(1, 1000)}]"
    return client.text_generation(
        prompt,
        max_new_tokens=300,
        do_sample=True,
        temperature=0.9,
    )

if __name__ == "__main__":
    print(get_nutrition_tip())