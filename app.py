import gradio as gr
from datetime import datetime
from quote import get_random_quote
from tips import get_parenting_tip, get_nutrition_tip
from podcast_recc import get_podcast_recommendations

def daily_message():
    current_time = datetime.now()
    return f"Hello Priya, my wonderful wife! ❤️\n\n**Today is {current_time.strftime('%A, %B %d')}**"

def format_podcast_recommendations():
    recommendations = get_podcast_recommendations()
    formatted_text = "## 🎧 Today's Podcast Recommendations\n\n"
    
    for rec in recommendations:
        formatted_text += f"### 📌 {rec['title']}\n"
        formatted_text += f"**From:** {rec['podcast_title']} by {rec['publisher']}\n\n"
        formatted_text += f"**Published:** {rec['pub_date']} • **Duration:** {rec['duration']}\n\n"
        formatted_text += f"{rec['description']}\n\n"
        formatted_text += f"[Listen here]({rec['link']})\n\n"
        formatted_text += "---\n\n"
    
    return formatted_text

# Create the Blocks interface
demo = gr.Blocks()

# Add components to the interface
with demo:
    gr.Markdown("# ❤️ Daily Quote, Tips, and Podcast Recommendations ❤️")
    gr.Markdown(
        value=daily_message,
        label="Today's Message",
        every=86400,
    )
    gr.Textbox(
        value=get_random_quote,
        label="Daily Quote",
        every=86400,
    )
    gr.Textbox(
        value=get_parenting_tip,
        label="Daily Parenting Tip",
        every=86400,
    )
    gr.Textbox(
        value=get_nutrition_tip,
        label="Daily Nutrition Tip",
        every=86400,
    )
    gr.Markdown(
        value=format_podcast_recommendations,
        every=86400,
    )

# Launch the interface
demo.launch(
    share=True,
    show_api=False,
    server_name="0.0.0.0",
    server_port=7860,
    quiet=True
)