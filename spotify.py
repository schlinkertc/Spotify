import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config

client_credentials_manager = SpotifyClientCredentials(
    client_id=config.client_id,
    client_secret=config.client_secret
)

sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager
)

def get_artistTracks(artist_name=None,artist_id=None):
    if artist_name:
        artist = sp.search(q=artist_name,type='artist')['artists']['items'][0]
        artist_id = artist['id']
    albums = sp.artist_albums(artist['id'])['items']
    
    album_ids = [ 
        {'id':x['id'],'album_name':x['name']} for x in albums 
    ]
    
    album_tracks = [ sp.album_tracks(x['id']) for x in album_ids ]
    
    # item for sublist in list for item in sublist 
    tracks = [ 
        {
            'name':item['name'],
            'id':item['id'],
            'artists':[x['name'] for x in item['artists']]
        }
        for album in album_tracks 
        for item in album['items']
        if artist['name'] in [ x['name'] for x in item['artists'] ]
    ]
    
    return tracks
