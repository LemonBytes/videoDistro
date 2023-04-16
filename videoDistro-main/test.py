from asyncore import loop
import json
import random
from dotenv import dotenv_values
import asyncpraw
import urllib.request
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


def download_dubz_videos(url):
    try:
        site = requests.get(url, headers=headers)
        print(site.content)
        soup = BeautifulSoup(site.content, "html.parser")
        video_url = soup.find("video")["src"]  # type: ignore
        print(video_url)
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(f"{video_url}", "./last_video_download/video.mp4")
        print("finished downloading video")
    except Exception as e:
        print(e)
        raise Exception("Error downloading video")


download_dubz_videos("https://dubz.co/video/32bfc4")
