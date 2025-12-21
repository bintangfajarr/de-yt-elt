import requests
import os
from dotenv import load_dotenv
import json
from datetime import date
load_dotenv()

YOUR_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
max_results=50
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


def get_video_ids(playlistId):
    base_url=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistId}&key={YOUR_API_KEY}"
    pageToken=None
    video_ids=[]
    try:
        while True:
            url=base_url
            if pageToken:
                url+=f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data=response.json()
            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            pageToken=data.get("nextPageToken")
            if not pageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e
    
def batch_list(input_id_list,batch_size):
    for video_id in range(0, len(input_id_list), batch_size):
        yield input_id_list[video_id:video_id + batch_size]
    'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id=dd&key=[YOUR_API_KEY]'
    
def extract_video_data(video_ids):
    extracted_data=[]
    try:
        for batch in batch_list(video_ids,max_results):
            video_ids_str= ",".join(batch)
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={YOUR_API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data=response.json()
            for item in data.get("items", []):
                video_id=item["id"]
                snippet=item["snippet"]
                contentDetails=item["contentDetails"]
                statistics=item["statistics"]
            video_data={
                "video_id":video_id,
                "title":snippet.get("title"),
                "publishedAt":snippet.get("publishedAt"),
                "duration":contentDetails.get("duration"),
                "viewCount":statistics.get("viewCount"),
                "likeCount":statistics.get("likeCount"),
                "commentCount":statistics.get("commentCount")
            }
            extracted_data.append(video_data)
        return extracted_data
            
    except requests.exceptions.RequestException as e:
        raise e
def save_to_json(extracted_data):
    file_path=f"./data/YT_data_{date.today()}.json"
    
    with open(file_path,"w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data,json_outfile, indent=4,ensure_ascii=False)
if __name__ == "__main__":
    print("get playlist id")
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    video_data=extract_video_data(video_ids)
    save_to_json(video_data)