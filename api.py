import os
import requests


def get_spotify_access_token(authorization_code):
    """Exchange authorization code for an access token"""

    client_id = os.environ.get("3b6c1dbfd64b4469a6a851f900ed8ede")
    client_secret = os.environ.get("b0f17c9b67034b3bb49acb049068a04b")
    redirect_uri = os.environ.get("http://localhost:3000/")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(
        url,
        headers=headers,
        data=data,
        auth=(client_id, client_secret)
    )

    return response.json()["access_token"]
