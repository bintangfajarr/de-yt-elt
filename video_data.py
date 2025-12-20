import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()

YOUR_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
def get_playlist_id():
    try:
        url=f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle=MrBeast&key={YOUR_API_KEY}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # print(json.dumps(data, indent=4))

        channel_items=data["items"][0]
        channel_playlists=channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlists)
        return channel_playlists
    except requests.exceptions.RequestException as e:
        raise e
if __name__ == "__main__":
    print("get playlist id")
    get_playlist_id()
