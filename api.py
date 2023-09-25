import requests
from flask import session


# curl -X POST "https://accounts.spotify.com/api/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "grant_type=client_credentials&client_id=3b6c1dbfd64b4469a6a851f900ed8ede&client_secret=b0f17c9b67034b3bb49acb049068a04b"

# {"access_token":"BQCTm_ORYBshGLgEArx6-6Cnx_ww1uzb_wJYPD-nLGRe6cc2hPazSbfPaG3XeCuTpt6L_ZY3NzUUri5PTvTdZF7W1g3MgErywfqtBFwvNtDqZQhTMTg","token_type":"Bearer","expires_in":3600}

def get_user_access_token():
    """Fetch the user's access token from the session or another source."""
    access_token = session.get(
        "BQCTm_ORYBshGLgEArx6-6Cnx_ww1uzb_wJYPD-nLGRe6cc2hPazSbfPaG3XeCuTpt6L_ZY3NzUUri5PTvTdZF7W1g3MgErywfqtBFwvNtDqZQhTMTg")
    return access_token


def get_available_genres(access_token):
    """Fetch available genres using the Spotify API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://api.spotify.com/v1/recommendations/available-genre-seeds", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("genres", [])
    else:
        return []


def get_top_artists(access_token, time_range='medium_term', limit=10):
    """Fetch the user's top artists using the Spotify API."""

    # Define the endpoint URL
    url = 'https://api.spotify.com/v1/top/artists'

    # Define the headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Define the query parameters
    params = {
        'time_range': time_range,
        'limit': limit
    }

    # Make the API request to get top artists
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        artists = data['items']
    else:
        artists = []

    return artists


def get_top_tracks(access_token):
    """fetch top tracks from spotify api"""
    endpoint = "https://api.spotify.com/v1/top-tracks"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "limit": 10
    }

    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        tracks = data["items"]
    else:
        tracks = []

    return tracks
