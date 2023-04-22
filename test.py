import json
import random
from dotenv import dotenv_values
import asyncpraw
import urllib.request
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pytube import YouTube


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

url = "https://youtu.be/6U6yaWLTmEM"
def __download_streamin_videos(url):
        default_download_path = "./last_video_download"
        try:
            yt = YouTube(url) 
            stream = yt.streams.get_highest_resolution()
            stream.download(default_download_path, "video.mp4")  # type: ignore
            print("finished downloading video")
        except Exception as e:
            __download_streamin_videos(url)
            print(e)
            
         
           

__download_streamin_videos(url)
