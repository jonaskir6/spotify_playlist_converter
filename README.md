# Playlist converter from Spotify to YouTube
* Python playlist converter that takes a spotify playlist as input and creates a YouTube Playlist containing the playlists songs
* Private Usage only
### Technology needed
* Python https://www.python.org/downloads/
### Private Usage (Limited)
* Clone the repository
* Create your Google API and and Spotify API 
* You will need: Spotify Client ID & Secret, YouTube API_Key & client_secret.json
* Add your Key, ID's and Secrets to your .env file
* Your .env file should contain (With the exact names):
- spotify_CLIENT_ID
- spotify_CLIENT_SECRET
- youtube_API_KEY
- yt_client_secret_path="client_secret/client_secret_youtube_api.json"
* Add your client_secret.json to client_secret folder
* Run app.py
#### Useful links to tutorials
* https://www.youtube.com/watch?v=noF-QBRLf4o&ab_channel=FineGap
* https://www.youtube.com/watch?v=c5sWvP9h3s8&ab_channel=ImdadCodes
### Issues
* The amount of requests to the Google API is limited to somewhere under 100 so right now it only works for small Playlists
