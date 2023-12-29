import streamlit as st
from googleapiclient.discovery import build

def calculate_playlist_duration(playlist_url):
    api_key = "YOUR API HERE"
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    playlist_id = playlist_url.split('list=')[1]
    
    playlist_items = youtube.playlistItems().list(
        playlistId=playlist_id,
        part='contentDetails',
        maxResults=50
    ).execute()

    video_ids = [item['contentDetails']['videoId'] for item in playlist_items['items']]

    total_duration = 0
    for video_id in video_ids:
        video_info = youtube.videos().list(
            id=video_id,
            part='contentDetails'
        ).execute()

        duration = video_info['items'][0]['contentDetails']['duration']

        if 'H' in duration:
            hours_index = duration.find('H')
            hours = int(duration[2:hours_index])
            minutes_index = duration.find('M')
            minutes = int(duration[hours_index + 1:minutes_index])
            seconds_index = duration.find('S')
            seconds = int(duration[minutes_index + 1:seconds_index]) if 'S' in duration else 0
            total_duration += (hours * 60) + minutes + (seconds / 60)
        elif 'M' in duration:
            minutes_index = duration.find('M')
            minutes = int(duration[2:minutes_index])
            seconds_index = duration.find('S')
            seconds = int(duration[minutes_index + 1:seconds_index]) if 'S' in duration else 0
            total_duration += minutes + (seconds / 60)
        else:
            seconds = int(duration[2:-1]) if duration.startswith('PT') else 0
            total_duration += seconds / 60

    return total_duration

st.title('YouTube Playlist Duration Calculator')

playlist_url = st.text_input('Enter YouTube Playlist URL:')
if st.button('Calculate Duration'):
    if playlist_url:
        try:
            total_duration = calculate_playlist_duration(playlist_url)
            st.success(f"Total duration of the playlist: {total_duration:.2f} minutes")
        except Exception as e:
            st.error("An error occurred. Please check the playlist URL.")
    else:
        st.warning("Please enter a YouTube Playlist URL.")
