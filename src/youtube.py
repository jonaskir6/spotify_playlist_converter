from dotenv import load_dotenv
from googleapiclient.errors import HttpError

from src.google import create_service
import os
import time
import sys

load_dotenv()

yt_client_secret_path = os.getenv("yt_client_secret_path")
API_KEY = os.getenv("youtube_API_KEY")

# setting up the Google api service to communicate with my YouTube api
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']
api_service = create_service(yt_client_secret_path, API_NAME, API_VERSION, SCOPES)


# Creates the new YouTube playlist with the given title
# Returns str: id of the created playlist
def create_youtube_playlist(title):
    request_body = {
        "snippet": {
            "title": title,
            "description": "Created from Google API",
            "defaultLanguage": "en"
        }
    }
    try:
        response = api_service.playlists().insert(part="snippet", body=request_body).execute()
        id = response['id']

        print(f"Playlist '{title}' created successfully. Playlist ID: {id}")
        return id

    except Exception as e:
        print(f"Error creating playlist due to an exception: {e}")
        return None


# Counter for retries if YouTube API Quota is exceeded
retried = [0]


# Searches for the music video and adds it to the given YouTube playlist
def search_and_add_video(video_title, playlist_id):
    global retried
    # Adding "music" to improve search results
    search_query = f"{video_title} music"

    video_id = None
    try:
        response = api_service.search().list(part="snippet", q=search_query, type="video").execute()
        if response["items"]:
            video_id = response["items"][0]["id"]["videoId"]
    except Exception as e:
        print(f"Error searching for youtube video due to an exception: {e}")

    item_body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }
    try:
        api_service.playlistItems().insert(part="snippet", body=item_body).execute()

    # Separate error-handling due to low maximum API Quota -> program will stop after exceeding it
    except HttpError as e:
        error_message = e.content.decode("utf-8")
        if "quota" in error_message:
            if retried[0] == 1:
                sys.exit("Stopping the program, API Quota Exceeded")
            print("API Quota exceeded. Retrying after 1 Minute")
            time.sleep(10)
            retried[0] += 1
    except Exception as e:
        print(f"Error adding youtube video to playlist due to an exception: {e}")
