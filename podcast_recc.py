from listennotes import podcast_api
from datetime import datetime
import time
import random

def get_podcast_recommendations():
    api_key = 'b0efc938b8f444a9ace6421f62a58d5d'
    client = podcast_api.Client(api_key=api_key)
    queries = ['parenting', 'relationships', 'mental health', 'longevity medicine', 
              'nutrition', 'fitness', 'female health', 'self-improvement', 
              'female empowerment']
    query = random.choice(queries)
    
    response = client.search(
      q = f'{query}',
      sort_by_date=0,
      type='episode',
      offset=0,
      len_min=5,
      len_max=200,
      genre_ids='132, 88, 107',  # 132 designates kids and family, 88 designates health and fitness, 107 designates science
      published_before=int(time.time() * 1000),
      published_after=0,
      only_in='title,description',
      language='English',
      safe_mode=0,
      unique_podcasts=0,
      interviews_only=0,
      sponsored_only=0,
      page_size=10,
    )
    # get results from response
    results = response.json()['results']

    # Select 3 random results
    random_results = random.sample(results, min(3, len(results)))

    recommendations = []
    for result in random_results:
        # Basic episode info
        episode_id = result.get('id', '')
        title = result.get('title_original', 'No Title')
        description = result.get('description_original', 'No Description')
        listen_url = result.get('listennotes_url', 'No Listen Notes URL')
        audio_length = result.get('audio_length_sec', 0)
        image = result.get('image', 'No Image URL')
        thumbnail = result.get('thumbnail', 'No Thumbnail URL')
        link = result.get('link', 'No Link')
        itunes_id = result.get('itunes_id', 'No iTunes ID')
        audio_length_sec = result.get('audio_length_sec', 0)
        pub_date_ms = result.get('pub_date_ms', 0)

        # Podcast-specific metadata
        podcast_info = result.get('podcast', {})
        podcast_title = podcast_info.get('title_original', 'Unknown Podcast')
        podcast_publisher = podcast_info.get('publisher_original', 'Unknown Publisher')

        # Convert audio_length to hours:minutes:seconds
        hours = audio_length // 3600
        minutes = (audio_length % 3600) // 60
        seconds = audio_length % 60
        duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # Convert milliseconds timestamp to readable date
        pub_date = datetime.fromtimestamp(pub_date_ms/1000).strftime('%B %d, %Y')

        podcast_info = {
            'itunes_id': itunes_id,
            'title': title,
            'podcast_title': podcast_title,
            'publisher': podcast_publisher,
            'pub_date': pub_date,
            'duration': duration,
            'description': description[:500] + "...",
            'link': link
        }
        recommendations.append(podcast_info)
    
    return recommendations

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
