from dotenv import load_dotenv
import os
import base64
from requests import get, post
import json
import time

load_dotenv()


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

token_expiration = 0


def get_token():
    global token_expiration
    global token
    current_time = time.time()

    if token_expiration - current_time < 60:
        auth_string = client_id + ":" + client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}

        response = post(url, headers=headers, data=data)
        json_response = json.loads(response.content)

        if "access_token" in json_response:
            token = json_response["access_token"]
            token_expiration = current_time + 3600
        else:
            print("Access token not found in response:", json_response)

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist):
    base_url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"?q={artist}&type=artist&limit=1"

    query_url = base_url + query
    response = get(query_url, headers=headers)
    json_response = json.loads(response.content)["artists"]["items"]
    if len(json_response) == 0:
        print("No artist found")
        return None

    else:
        return json_response[0]


def get_songs_by_artist(token, artist_id):
    base_url = "https://api.spotify.com/v1/artists/"
    headers = get_auth_header(token)

    query = f"{artist_id}/top-tracks?market=US"

    query_url = base_url + query
    response = get(query_url, headers=headers)
    json_response = json.loads(response.content)["tracks"]

    return json_response


def search_for_song(token, song_name):
    base_url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    params = {
        "q": song_name,
        "type": "track",
        "limit": 10
    }

    response = get(base_url, params=params, headers=headers)
    json_response = json.loads(response.content)["tracks"]["items"]

    return json_response


def get_song_info(token, spotify_id):
    base_url = "https://api.spotify.com/v1/tracks/"
    headers = get_auth_header(token)

    query_url = f"{base_url}{spotify_id}"
    response = get(query_url, headers=headers)

    if response.status_code == 200:
        json_response = json.loads(response.content)
        return {
            "title": json_response.get("name"),
            "artist": json_response["artists"][0].get("name"),
            "album": json_response.get("album", {}).get("name"),
            "image": json_response.get("album", {}).get("images", [{}])[0].get("url"),
            "release_date": json_response.get("album", {}).get("release_date"),
            "preview": json_response.get("preview_url")
        }
    print(
        f"Failed to fetch song info for ID {spotify_id}. Status code: {response.status_code}")
    return None


def get_genres(token):
    base_url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = get_auth_header(token)

    response = get(base_url, headers=headers)
    available_genres = json.loads(response.content)["genres"]

    return available_genres


def get_songs_by_genre(token, genre):
    base_url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = get_auth_header(token)

    response = get(base_url, headers=headers)
    available_genres = json.loads(response.content)["genres"]

    if genre not in available_genres:
        print("Genre not found")
        return None

    recommendations_url = "https://api.spotify.com/v1/recommendations"
    params = {
        "seed_genres": genre,
        "limit": 25
    }

    response = get(recommendations_url, params=params, headers=headers)
    tracks = json.loads(response.content)["tracks"]

    return tracks


def is_valid_spotify_id(token, spotify_id):
    base_url = "https://api.spotify.com/v1/tracks/"
    headers = get_auth_header(token)

    query_url = f"{base_url}{spotify_id}"
    response = get(query_url, headers=headers)

    if response.status_code == 200:
        return True
    return False


_token = get_token()
