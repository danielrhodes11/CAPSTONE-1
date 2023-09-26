from dotenv import load_dotenv
import os
import base64
from requests import get, post
import json

load_dotenv()


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
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
    access_token = json_response["access_token"]

    return access_token


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


token = get_token()
response = search_for_artist(token, "The Beatles")
artist_id = response["id"]

print(response["name"])

tracks = get_songs_by_artist(token, artist_id)

for track in tracks:
    print(track["name"])
