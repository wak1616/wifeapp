import gradio as gr
from datetime import datetime
import pytz
from functools import lru_cache
from quote import get_random_quote
from tips import get_parenting_tip, get_nutrition_tip
from podcast_recc import get_podcast_recommendations

# Cache for daily content
@lru_cache()
def get_daily_content(date_string):
    """Cache content based on the date string"""
    return {
        'quote': get_random_quote(),
        'parenting_tip': get_parenting_tip(),
        'nutrition_tip': get_nutrition_tip(),
        'podcasts': get_podcast_recommendations()
    }

def get_current_content():
    # Use EST timezone (or your preferred timezone)
    tz = pytz.timezone('America/New_York')
    current_time = datetime.now(tz)
    
    # Format date as YYYY-MM-DD for caching
    date_string = current_time.strftime('%Y-%m-%d')
    
    # Get cached content for today
    daily_content = get_daily_content(date_string)
    
    return current_time, daily_content

def refresh_podcasts():
    return get_podcast_recommendations()

# Define the CSS code for a background
css_code = """
.gradio-container {
    background: linear-gradient(
        rgba(255, 255, 255, 0.9),
        rgba(255, 255, 255, 0.9)
    ),
    url('https://img.freepik.com/premium-photo/couple-love-beautiful-desktop-background_212944-31581.jpg?w=1380');
    background-size: cover;
    background-position: center;
}
"""

# Add components to the interface
with gr.Blocks(theme=gr.themes.Glass(), css=css_code) as demo:
    gr.Markdown("# ❤️ Daily Quote, Tips, and Podcast Recommendations ❤️")
    
    # Get initial content
    current_time, content = get_current_content()
    
    gr.Markdown(f"### Hello Priya, my wonderful wife! 💝\n\n### Today is {current_time.strftime('%A, %B %d')}\n\n---\n")
    gr.Markdown(f"## 💭 Daily Quote\n\n{content['quote']}\n\n---\n")
    gr.Markdown(f"## 👶 Parenting Tip\n\n{content['parenting_tip']}\n\n---\n")
    gr.Markdown(f"## 🥗 Nutrition Tip\n\n{content['nutrition_tip']}\n\n---\n")
    
    # Create podcast section with refresh button
    gr.Markdown(f"## 🎧 Podcast Recommendations:\n\n")
    podcast_output = gr.Markdown(f"{content['podcasts']}\n\n---\n")
    gr.Button("🔄 Get New Podcast Recommendations").click(
        fn=refresh_podcasts,
        outputs=podcast_output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)