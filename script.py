# Import necessary libraries
import os
import re
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8080/callback'

# Define Spotify API scopes
read_scope = "playlist-read-private"
modify_scope = "playlist-modify-private"

def create_auth_object(scope):
    # Create Spotify API clients with different scopes
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                        client_id=CLIENT_ID,
                                                        client_secret=CLIENT_SECRET,
                                                        redirect_uri=REDIRECT_URI))
    return sp
# sp_read = create_auth_object(read_scope)
# sp_modify = create_auth_object(modify_scope)


def get_existing_playlists(sp_read):
    # initialize variables
    offset = 0
    total = 1
    playlists = []

    # retrieve all playlists
    while offset < total:
        results = sp_read.current_user_playlists(limit=50, offset=offset)
        playlists.extend(results["items"])
        offset += len(results["items"])
        total = results["total"]

    # Create a list of existing playlists
    existing_playlists = []
    for playlist in playlists:
        existing_playlists.append(playlist["name"])   
    return existing_playlists,playlists                                     

# Print the total number of existing playlists
# print(len(existing_playlists))

def read_file(file):
    '''Reads WhatsApp text file into a string'''
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


def get_uri_list(chat):
    # Define regex pattern to extract Spotify track links from the text file
    spotify_pattern = r'(https://open\.spotify\.com/track/[a-zA-Z0-9]+)(?=[^a-zA-Z0-9]|$)'

    # Find all Spotify track links in the chat string using regex pattern
    links_list = re.findall(spotify_pattern, chat, re.DOTALL)
    uri_list = []

    # Convert Spotify track links to track URIs
    for link in links_list:
        track_id = re.search(r'track/([^\?]+)', link).group(1)
        uri = f"spotify:track:{track_id}"
        uri_list.append(uri)
    return uri_list
# uri_list = get_uri_list(chat)

# Create a new private playlist with the given name, or use an existing one with the same name


def add_playlists(chat,playlist_id,sp_modify):
    '''Add tracks to the playlist in chunks of 100'''
    user_id = sp_modify.me()['id']
    uri_list = get_uri_list(chat)
    chunk_size = 100
    for i in range(0, len(uri_list), chunk_size):
        sp_modify.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=uri_list[i:i+chunk_size])

def create_playlist(chat,playlist_name,playlist_id=None):
    sp_read = create_auth_object(read_scope)
    sp_modify = create_auth_object(modify_scope)

    user_id = sp_modify.me()['id']
    existing_playlists,playlists = get_existing_playlists(sp_read)
    playlist_exists = playlist_name in existing_playlists

    if not playlist_exists:
        # Create a new playlist if it doesn't exist
        playlist = sp_modify.user_playlist_create(user=user_id, name=playlist_name, public=False)
        playlist_id = playlist['id']
        print(f'Created new playlist "{playlist_name}" with ID {playlist_id}')
        add_playlists(chat,playlist_id,sp_modify) # Add tracks to the new playlist
    else:
        # Replace tracks in the existing playlist if it exists
        for playlist in playlists:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                break
        print(f'Using existing playlist "{playlist_name}" with ID {playlist_id}')
        sp_modify.user_playlist_replace_tracks(user=user_id, playlist_id=playlist_id, tracks=[])
        add_playlists(chat,playlist_id,sp_modify) # Add tracks

if __name__ == '__main__':
    chat = read_file('txts/example.txt')
    playlist_name = 'example playlist'
    create_playlist(chat,playlist_name)