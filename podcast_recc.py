from listennotes import podcast_api
from datetime import datetime
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_podcast_recommendations():
    api_key = os.getenv('LISTENNOTES_API_KEY')
    if not api_key:
        raise ValueError("LISTENNOTES_API_KEY environment variable is not set")
        
    client = podcast_api.Client(api_key=api_key)
    queries = ['parenting', 'relationships', 'mental health', 'longevity medicine', 
              'nutrition', 'fitness', 'female health', 'self-improvement', 
              'female empowerment']
    
    random_query = random.choice(queries)
    response = client.search(
      q=random_query,
      sort_by_date=0,
      type='episode',
      len_min=5,
      len_max=200,
      genre_ids='132, 88, 107',
      published_before=int(time.time() * 1000),
      language='English',
      page_size=10,
    )
    
    results = response.json()['results']

    # Select 3 random results
    random_results = random.sample(results, min(3, len(results)))

    recommendations = []
    for result in random_results:
        audio_length = result.get('audio_length_sec', 0)
        hours = audio_length // 3600
        minutes = (audio_length % 3600) // 60
        seconds = audio_length % 60
        
        podcast_info = result.get('podcast', {})
        recommendations.append({
            'thumbnail': result.get('thumbnail', 'No Thumbnail'),
            'title': result.get('title_original', 'No Title'),
            'podcast_title': podcast_info.get('title_original', 'Unknown Podcast'),
            'publisher': podcast_info.get('publisher_original', 'Unknown Publisher'),
            'pub_date': datetime.fromtimestamp(result.get('pub_date_ms', 0)/1000).strftime('%B %d, %Y'),
            'duration': f"{hours:02d}:{minutes:02d}:{seconds:02d}",
            'description': result.get('description_original', 'No Description')[:500] + "...",
            'link': result.get('link', 'No Link')
        })
    
    return recommendations, random_query

if __name__ == "__main__":
    recommendations = get_podcast_recommendations()
    for rec in recommendations:
        print(f"iTunes ID: {rec['itunes_id']}")
        print(f"Title: {rec['title']}")
        print(f"Podcast: {rec['podcast_title']} by {rec['publisher']}")
        print(f"Published: {rec['pub_date']}")
        print(f"Duration: {rec['duration']}")
        print(f"Description: {rec['description']}")
        print(f"Link: {rec['link']}")
        print("-" * 40)
