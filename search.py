from googleapiclient.discovery import build
from utils import write_to, write_history, YT_KEY, MAX_SEARCH
import datetime


youtube = build('youtube', 'v3', developerKey=YT_KEY)


def search_video(query):
    request = youtube.search().list(
        part='id,snippet',
        q=query,
        maxResults=MAX_SEARCH,
        type='video'
    )
    response = request.execute()
    write_to("res/response.json", response, 4, 'w', None, True)
    write_history("res/usr/search-history.txt", datetime.datetime.now(), f"Searched --> {query}\n")
    search_results = []
    for item in response['items']:
        title = item['snippet']['title']
        channel = item['snippet']['channelTitle']
        video_id = item['id']['videoId']
        video = {
            'name': title + " -> " + channel,
            'value': f'https://www.youtube.com/watch?v={video_id}'
        }
        search_results.append(video)
    search_results.append({'name': 'Return', 'value': 'none'})
    return search_results
