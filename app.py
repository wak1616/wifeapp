import gradio as gr
from datetime import datetime
import json
import os
from quote import get_random_quote
from tips import get_parenting_tip, get_nutrition_tip
from podcast_recc import get_podcast_recommendations

CACHE_FILE = "daily_cache.json"

def daily_message():
    current_time = datetime.now()
    return f"## 💝 Daily Message\n\n**Hello Priya, my wonderful wife!** ❤️\n\nToday is **{current_time.strftime('%A, %B %d')}**\n\n---\n"

def format_podcast_recommendations(recommendations, query):
    formatted_text = f"## 🎧 Today's Podcast Recommendations (Searched for '{query}')\n\n"
    for i, rec in enumerate(recommendations):
        if i == 1:
            formatted_text += "___\n\n"
            
        formatted_text += f"### [![thumbnail]({rec['thumbnail']})]({rec['link']}) {rec['title']}\n"
        formatted_text += f"**From:** {rec['podcast_title']} by {rec['publisher']}\n\n"
        formatted_text += f"**Published:** {rec['pub_date']} • **Duration:** {rec['duration']}\n\n"
        formatted_text += f"{rec['description']}\n\n"
        
        if i == 1:
            formatted_text += "___\n\n"
    return formatted_text

def generate_daily_content():
    try:
        recommendations, query = get_podcast_recommendations()
        content = {
            "message": daily_message(),
            "quote": f"## 💭 Daily Quote\n\n{get_random_quote()}\n\n---\n",
            "parenting_tip": f"## 👶 Parenting Tip\n\n{get_parenting_tip()}\n\n---\n",
            "nutrition_tip": f"## 🥗 Nutrition Tip\n\n{get_nutrition_tip()}\n\n---\n",
            "podcasts": format_podcast_recommendations(recommendations, query),
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return None
    
    # Save to cache
    with open(CACHE_FILE, "w") as f:
        json.dump(content, f)
    
    return content

def get_cached_content():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                content = json.load(f)
            
            # Check if cache is from today
            cached_date = datetime.fromisoformat(content["generated_at"]).date()
            if cached_date == datetime.now().date():
                return [
                    content["message"],
                    content["quote"],
                    content["parenting_tip"],
                    content["nutrition_tip"],
                    content["podcasts"]
                ]
            # If cache is from a different day, it falls through to generate new content
    except Exception as e:
        print(f"Cache error: {str(e)}")
    
    # Generate new content if:
    # 1. Cache doesn't exist
    # 2. Cache is from a different day
    # 3. There was an error reading the cache
    content = generate_daily_content()
    if content:
        return [
            content["message"],
            content["quote"],
            content["parenting_tip"],
            content["nutrition_tip"],
            content["podcasts"]
        ]
    return ["Error loading content"] * 5

# Create the Gradio interface
demo = gr.Blocks(theme=gr.themes.Glass())

# Add components to the interface
with demo:
    gr.Markdown("# ❤️ Daily Quote, Tips, and Podcast Recommendations ❤️")
    message = gr.Markdown()
    quote = gr.Markdown()
    parenting = gr.Markdown()
    nutrition = gr.Markdown()
    podcasts = gr.Markdown()
    
    demo.load(
        fn=get_cached_content,
        outputs=[message, quote, parenting, nutrition, podcasts]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
    quiet=True
    )