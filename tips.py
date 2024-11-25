from huggingface_hub import InferenceClient
import random
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
    prompt = f"Provide a brief and useful {topic} tip. [Run ID: {random.randint(1, 1000)}]"
    return client.text_generation(
        prompt,
        max_new_tokens=300,
        do_sample=True,
        temperature=0.6,
    )

def get_nutrition_tip():
    return get_tip("nutrition or healthy eating")

def get_parenting_tip():
    return get_tip("parenting")

if __name__ == "__main__":
    print("Getting nutrition tip...")
    print("-" * 40)
    print(get_nutrition_tip())
    print("\nGetting parenting tip...")
    print("-" * 40)
    print(get_parenting_tip()) 