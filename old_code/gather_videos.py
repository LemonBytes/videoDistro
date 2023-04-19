from asyncore import loop
import json
import random
from dotenv import dotenv_values
import asyncpraw
import urllib.request
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pytube import YouTube
from old_code.edit_video import get_first_video_with_parts, write_to_queue
from publish_video import clean_up

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


def is_video_unused(url, title):
    with open("videos.json", "r") as f:
        data = json.load(f)
        videos = data["videos"]
        if (url in [video["video_url"] for video in videos]) or (
            title in [video["video_title"] for video in videos]
        ):
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


def download_youtube(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download("./last_video_download/video.mp4")  # type: ignore
    except Exception as e:
        print(e)
        raise Exception("Error downloading video")


def download_dubz_videos(url):
    try:
        site = requests.get(url, headers=headers)
        soup = BeautifulSoup(site.content, "html.parser")
        video_url = soup.find("video")["src"]  # type: ignore
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(f"{video_url}", "./last_video_download/video.mp4")
        print("finished downloading video")
    except Exception as e:
        print(e)
        raise Exception("Error downloading video")


def download_gfycat_videos(url):
    try:
        site = requests.get(url, headers=headers)
        soup = BeautifulSoup(site.content, "html.parser")
        video_url = soup.find("source", type="video/mp4")["src"]  # type: ignore
        urllib.request.urlretrieve(f"{video_url}", "./last_video_download/video.mp4")
        print("finished downloading video")
    except Exception as e:
        print(e)
        raise Exception("Error downloading video")


def download_streamable_videos(url):
    try:
        site = requests.get(url, headers=headers)
        soup = BeautifulSoup(site.content, "html.parser")
        video_url = soup.find("video", class_="video-player-tag")["src"]  # type: ignore
        with open("./last_video_download/video.mp4", "wb") as f_out:
            r = requests.get(f"https:{video_url}", stream=True)
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f_out.write(chunk)
        print("finished downloading video")
    except Exception as e:
        print(e)
        raise Exception("Error downloading video")


async def get_reddit_videos(loop):
    flair = ""
    # 50 chances to get a one of the flairs

    flairs = ["FIGHT CLIP", "Highlights", "Spoiler", "Full Fight"]
    flair = random.choice(flairs)

    print(flair)
    config = dotenv_values(".env")
    # set up reddit instance
    async with asyncpraw.Reddit(
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
        user_agent="Wyzbits",
    ) as reddit:
        subreddit = await reddit.subreddit("MMA")
        async for post in subreddit.search(
            "flair:" + flair, syntax="lucene", limit=None
        ):
            # # download the video
            if "gfycat" in post.url:
                if is_video_unused(post.url, post.title):
                    print(post.url)
                    print(post.title)
                    try:
                        download_gfycat_videos(post.url)
                        write_to_json(post.url, post.title)
                        loop.stop()
                        break
                    except Exception as e:
                        print(e)
                        continue
            if "streamable" in post.url:
                print(post.url)
                print(post.title)
                if is_video_unused(post.url, post.title):
                    try:
                        download_streamable_videos(post.url)
                        write_to_json(post.url, post.title)
                        loop.stop()
                        break
                    except Exception as e:
                        print(e)
                        continue
            if "dubz" in post.url:
                print(post.url)
                print(post.title)
                if is_video_unused(post.url, post.title):
                    try:
                        download_streamable_videos(post.url)
                        write_to_json(post.url, post.title)
                        loop.stop()
                        break
                    except Exception as e:
                        print(e)
                        continue
            if "youtube" in post.url:
                print(post.url)
                print(post.title)
                if is_video_unused(post.url, post.title):
                    try:
                        download_youtube(post.url)
                        write_to_json(post.url, post.title)
                        loop.stop()
                        break
                    except Exception as e:
                        print(e)
                        continue
