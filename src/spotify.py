from dotenv import load_dotenv

import os
import base64
from requests import post, get
import json
import re
import demoji

load_dotenv()
client_id = os.getenv("spotify_CLIENT_ID")
client_secret = os.getenv("spotify_CLIENT_SECRET")


# Cleans the string from all random characters and emojis
# Returns str: cleaned string
def clean(text):
    match = re.search(r"b'(.*?)\\", text)
    if match:
        cleaned_string = match.group(1)
    else:
        # If there is no backslash, return the whole string without the prefix "b'"
        cleaned_string = re.sub(r"b'(.*?)'", r"\1", text)

    return cleaned_string


# Cleans string from common emojis
# Returns str: cleaned string
def remove_emojis(input_string):
    input_string = str(input_string)
    input_string = clean(input_string)
    return demoji.replace(input_string, '')


# Gets the access token for the spotify api
# Returns json: Access token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # Parse access token from json data
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


spotify_token = get_token()


# Gets the Authorization header from the spotify access token
# Returns str: auth header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


# Gets the Playlist uri to access the playlist data like track names
# Returns str: playlist uri
def get_playlist_id(token, playlist_name, user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)

    remove_emojis(playlist_name)

    result = get(url, headers=headers)
    response = result.json()

    # filters the playlist_id of the playlist_name in argument
    for item in response['items']:
        if remove_emojis(item['name'].encode("utf-8")) == playlist_name:
            return item['id']


# Gets the whole spotify playlist tracklist as a str-list
# Returns list[str]: Tracklist
def get_playlist_track_list(playlist_id, token):
    # Trim Playlist URI
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?"
    headers = get_auth_header(token)

    tracklist = []

    while True:
        result = get(url, headers=headers)
        response = result.json()

        total_tracks = response['total']
        items = response['items']

        for item in items:
            if item['track'] is not None:
                track_name = item['track']['name']
                artist_name = item['track']['artists'][0]['name']

                # Check if track_name and artist_name are not None
                if track_name is not None and artist_name is not None:
                    track_name = clean(str(track_name))
                    artist_name = clean(str(artist_name))
                    # print(clean(f"{artist_name} - {track_name}\n"))
                    tracklist.append(f"{artist_name} - {track_name}")
            else:
                break

        # Check if there are more tracks to fetch
        if response['next']:
            url = response['next']  # Set the URL to the next batch of tracks
        else:
            break  # Exit the loop if there are no more tracks

    tracklist_string = "\n".join(tracklist)

    # There is an issue reading some Tracks
    if total_tracks == tracklist_string.count('\n') + 1:
        print("Success: " + str(tracklist_string.count('\n') + 1) + " of " + str(total_tracks) + "Tracks read")
    else:
        print("Warning: Only " + str(tracklist_string.count('\n') + 1) + " of " + str(total_tracks) + "Tracks read")

    return tracklist
