from typing import Union
import json
import os
import pafy
from pafy.util import GdataError
from dotenv import load_dotenv
from googleapiclient.errors import HttpError

load_dotenv(os.path.join(os.getcwd(), 'res', 'usr', '.env'))


class COLORS:
    # Purple
    HEADER = '\033[95m'
    # Blue
    OKBLUE = '\033[94m'
    # Light Blue
    OKCYAN = '\033[96m'
    # Green
    OKGREEN = '\033[92m'
    # Light Yellow
    WARNING = '\033[93m'
    # Red
    FAIL = '\033[91m'
    # Default
    ENDC = '\033[0m'
    # Bold
    BOLD = '\033[1m'
    # Underlined
    UNDERLINE = '\033[4m'


YT_KEY = os.environ['YOUTUBE_API_KEY']
MAX_PLAYLIST = os.environ['MAX_PLAYLIST_ITEM']
MAX_SEARCH = os.environ['MAX_SEARCH_ITEM']


def write_to(filepath: str, data: Union['str', 'dict'], indent: int, mode: str, encoding, is_json: bool):
    if mode == 'r':
        with open(filepath, mode=mode, encoding=encoding) as file:
            if is_json:
                return json.load(file)
            return file.read()
    if mode == 'w' or mode == 'a':
        with open(filepath, mode=mode, encoding=encoding) as file:
            if is_json:
                return json.dump(data, file, indent=indent)
            return file.write(data)


def write_history(filepath: str, timestamp, data: str):
    with open(filepath, 'a') as file:
        file.write(f"{timestamp} - {data.encode('utf-8')}")


def load_playlist_name(playlist_name):
    data = load_playlist_file()
    for item in data:
        if item.get("name").lower() == playlist_name.lower():
            return item
    return None


def remove_playlist_name(playlist_name):
    data = load_playlist_file()
    for i, playlist in enumerate(data):
        if playlist.get("name").lower() == playlist_name.lower():
            n = data.pop(i)
            with open("res/usr/playlist.json", 'w') as file:
                json.dump(
                    {
                        "Playlist": data
                    },
                    file, indent=4
                )
            return n
    return None


def load_playlist_file():
    with open("res/usr/playlist.json", 'r') as file:
        data = json.load(file)['Playlist']
    return data


def add_playlist(playlist_name, value, title, channel):
    with open("res/usr/playlist.json", 'r') as file:
        data = json.load(file)
    for item in data['Playlist']:
        if item.get('name').lower() == playlist_name.lower():
            item.get('videos').append((title, value, channel))
            with open("res/usr/playlist.json", 'w') as file:
                json.dump(data, file, indent=4)
            return
    data['Playlist'].append(
        {
            "name": playlist_name.capitalize(),
            "videos": [(title, value, channel)]
        }
    )
    with open("res/usr/playlist.json", 'w') as file:
        json.dump(data, file, indent=4)


def get_video_details(link):
    try:
        video = pafy.new(link)
    except (HttpError, GdataError, ValueError):
        return None, 0, 0
    title = video.title
    channel = video.author
    return title, link, channel
