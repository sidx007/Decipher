from googleapiclient.discovery import build
import json
import isodate
import os

if not os.path.exists('bot_home/decipher_bot/result_files'):
    os.makedirs('bot_home/decipher_bot/result_files')

PATH = 'bot_home/decipher_bot/result_files/'
API_KEY = "AIzaSyD5umLSZk_a6O89JDYGfugjJjzRyFB7fnw"
def searchQuery(query, max_results=10):

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Call the search.list method to retrieve results matching the specified query term
    search_response = youtube.search().list(
        q=query,
        part='id',
        type='video',  # Ensure we are only looking for videos
        maxResults=max_results
    ).execute()

    # Extract the video IDs from the search response
    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

    if not video_ids:
        return []

    # Get the details of the videos including their duration
    videos_response = youtube.videos().list(
        id=','.join(video_ids),
        part='id,snippet,contentDetails'
    ).execute()

    # Initialize a list to store video information
    videos = []

    # Filter out videos that are less than 60 seconds (likely Shorts)
    for video in videos_response.get('items', []):
        duration = isodate.parse_duration(video['contentDetails']['duration'])
        if duration.total_seconds() >= 60:
            video_data = {
                'title': video['snippet']['title'],
                'videoId': video['id'],
                'description': video['snippet']['description'],
                'thumbnail': video['snippet']['thumbnails']['default']['url']
            }
            videos.append(video_data)

    title_file = open(PATH+"ytresultsTitle.txt", 'w', encoding='utf-8', errors='ignore')
    links_file = open(PATH+"ytresultsLinks.txt", 'w', encoding='utf-8', errors='ignore')

    for video in videos:
        # print(f"Title: {video['title']}")
        # print(f"Video ID: {video['videoId']}")
        # print(f"Description: {video['description']}")
        # print(f"Thumbnail: {video['thumbnail']}")
        # print("\n")
        title_file.write(f"{video['title']}\n")

        links_file.write(f"https://www.youtube.com/watch?v={video['videoId']}\n")
    title_file.close()
    links_file.close()
