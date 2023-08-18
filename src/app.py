import youtube
import spotify

spotify_playlist_name = input("Enter the Spotify playlist name: ")
new_playlist_name = input("Enter a name for your new YouTube Playlist: ")
user_id = input("Enter the playlist owners Spotify user ID: ")

# Gets Spotify playlist's tracklist
spotify_tracklist = spotify.get_playlist_track_list(
    spotify.get_playlist_id(spotify.spotify_token,
                            spotify_playlist_name,
                            user_id),
    spotify.spotify_token)

# Gets YouTube playlist ID
yt_playlist = youtube.create_youtube_playlist(new_playlist_name)

# Adds videos to the new YouTube playlist
for track in spotify_tracklist:
    youtube.search_and_add_video(track, yt_playlist)
