import json
import random
import time
from dotenv import dotenv_values

# import asyncpraw
from video import Video
import praw

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


class Collector:
    # gather = Gathrer("reddit")
    # video = gather.get_video(eventloop)
    # nach zufallsprinzip für eine quelle entscheiden
    def __init__(self, origin, video: Video):
        self.origin = origin
        self.video = video

    def get_video(self) -> Video:
        if self.origin == "reddit":
            video = self.__get_reddit_video(
                "MMA",
                [
                    #"Full Fight",
                    "FIGHT CLIP",
                    "Highlights",
                ],
            )
            return video
        else:
            self.video.status = "error"
            return self.video

    def __extract_video_id(self, url):
        if "youtube" in url:
            video_id = url.split("=")[-1]
            if(video_id == "share"):
                video_id = url.split("/")[-2]
        else:
            video_id = url.split("/")[-1]
        return video_id

    def __is_video_unused(self, destination_url, title):
        with open("videos.json", "r") as f:
            data = json.load(f)
            videos = data["videos"]
            for video in videos:
                id = self.__extract_video_id(destination_url)
                if id == video["id"]:
                    return False
        return True

    def __get_reddit_video(self, subreddit_name, flairs) -> Video:
        chosenflair = random.choice(flairs)
        print(f"Chosen flair: {chosenflair}")
        config = dotenv_values(".env")
        reddit = praw.Reddit(
            client_id=config["CLIENT_ID"],
            client_secret=config["CLIENT_SECRET"],
            user_agent="Wyzbits",
        )
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.search(
            "flair:" + chosenflair, syntax="lucene", limit=None
        ):
            if (
                "youtube.com"
                or "youtu.be"
                or "dubz.co"
                or "gfycat.cm"
                or "streamable.com" 
                or "streamin.one"
                in post.url
            ):
                if self.__is_video_unused(post.url, post.title):
                    print("Found unused video")
                    self.video.title = post.title
                    self.video.source_url = post.url
                    self.video.id = self.__extract_video_id(post.url)
                    self.video.status = "pending"
                    return self.video

        self.video.status = "error"
        return self.video
