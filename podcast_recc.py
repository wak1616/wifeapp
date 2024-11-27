import requests
from datetime import datetime
import random


def format_duration(milliseconds):
    """Convert milliseconds to HH:MM:SS format"""
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def format_podcast_recommendations(podcasts, topic):
    formatted_text = f"Here are some recommended podcasts about **{topic}**:\n\n"
    
    for i, podcast in enumerate(podcasts, 1):
        formatted_text += f"### {i}. {podcast['trackName']}\n"
        formatted_text += f"<img src='{podcast['artworkUrl60']}' width='160' height='160'>\n\n"
        formatted_text += f"🎙️ **Show**: {podcast['collectionName']}\n\n"
        formatted_text += f"⏱️ **Duration**: {podcast['duration']}\n\n"
        formatted_text += f"📝 **Description**: {podcast['description']}\n\n"
        formatted_text += f"🔗 [Listen Now]({podcast['viewURL']})\n\n"
        formatted_text += "---\n\n"
    
    return formatted_text

def get_podcast_recommendations():
    queries = ['parenting', 'marriage', 'mental health', 'longevity medicine', 
              'nutrition', 'health and wellness', 'self-improvement']
    
    random_query = random.choice(queries)
    
    # iTunes API request
    url = f"https://itunes.apple.com/search"
    params = {
        'term': random_query,
        'media': 'podcast',
        'entity': 'podcastEpisode',
        'attribute': 'ratingIndex',
        'limit': 30,
        'lang': 'en_us'
    }
    
    response = requests.get(url, params=params)
    results = response.json().get('results', [])
    
    # Select 3 random results without filtering by rating
    selected_results = random.sample(results, min(3, len(results)))
    
    recommendations = []
    for result in selected_results:
        artwork_url = result.get('artworkUrl60', '').replace('60x60', '160x160')
        
        recommendations.append({
            'kind': result.get('kind', 'Unknown'),
            'trackName': result.get('trackName', 'No Title'),
            'collectionName': result.get('collectionName', 'Unknown Collection'),
            'artworkUrl60': artwork_url,
            'viewURL': result.get('trackViewUrl', 'No Link'),
            'duration': format_duration(result.get('trackTimeMillis', 0)),
            'description': result.get('description', 'No description available')
        })
    
    return format_podcast_recommendations(recommendations, random_query)

if __name__ == "__main__":
    recommendations = get_podcast_recommendations()
    print(recommendations)
