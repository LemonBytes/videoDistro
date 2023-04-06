from asyncore import loop
import json
from dotenv import dotenv_values
import asyncpraw
import urllib.request
import os
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
}


def is_video_unused(url, title):
    with open("videos.json", "r") as f:
        data = json.load(f)
        videos = data["videos"]
        for video in videos:
            if video["video_url"] == url:
                return False
    return True


def write_to_json(url, title):
    with open("videos.json", "r") as f:
        data = json.load(f)
        videos = data["videos"]
        videos.append(
            {"video_url": url, "video_title": title},
        )
    with open("videos.json", "w") as f:
        json.dump(data, f, indent=4)


def download_gfycat_videos(url):
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    try:
        video_url = soup.find("source", type="video/mp4")["src"]
        urllib.request.urlretrieve(video_url, "./videos/video.mp4")
        print("finished downloading video")
    except Exception as e:
        raise Exception("Error downloading video")


def download_streamable_videos(url):
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    try:
        video_url = soup.find("video", class_="video-player-tag")["src"]
        with open("./videos/video.mp4", "wb") as f_out:
            r = requests.get("https:" + video_url, stream=True)
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f_out.write(chunk)
        print("finished downloading video")
    except Exception as e:
        raise Exception("Error downloading video")


async def get_reddit_videos(loop):
    flair = ""
    # 50 chances to get a one of the flairs
    import random

    if random.random() < 0.4:
        flair = "FIGHT CLIP"
    else:
        flair = "Highlights"

    print(flair)
    config = dotenv_values(".env")
    # set up reddit instance
    async with asyncpraw.Reddit(
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
        user_agent="wyzbits",
    ) as reddit:
        subreddit = await reddit.subreddit("MMA")
        async for post in subreddit.search(
            "flair:" + flair, syntax="lucene", limit=None
        ):
            # # download the video
            if "gfycat" in post.url:
                if is_video_unused(post.url, post.title):
                    try:
                        download_gfycat_videos(post.url)
                        write_to_json(post.url, post.title)
                        loop.stop()
                        break
                    except Exception as e:
                        print(e)
                        continue
            if "streamable" in post.url:
                if is_video_unused(post.url, post.title):
                    try:
                        download_streamable_videos(post.url)
                        write_to_json(post.url, post.title)
                        loop.stop()
                        break
                    except Exception as e:
                        print(e)
                        continue
