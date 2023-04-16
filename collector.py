import json
import random
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

    def __extract_video_id(self, url):
        if "youtube" in url:
            video_id = url.split("=")[-1]
            print(video_id)
        else:
            video_id = url.split("/")[-1]
            print(video_id)
        return video_id    

    def get_video(self):
        if self.origin == "reddit":
            return self.get_reddit_video(
                "MMA", ["FIGHT CLIP", "Highlights", "Spoiler", "Full Fight"]
            )
        self.video.status = "error"
        return self.video
    

    def is_video_unused(self, destination_url, title):
        with open("videos.json", "r") as f:
            data = json.load(f)
            videos = data["videos"]
            if (destination_url in [video["video_url"] for video in videos]) or (
                title in [video["video_title"] for video in videos]
            ):
                return False
        return True

    def get_reddit_video(self, subreddit_name, flairs) -> Video:
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
                post.url
                and ("gfycat" or "streamable" or "dubz" or "youtu.be") in post.url
            ):
                if self.is_video_unused(post.url, post.title):
                    print("Found unused video")
                    print(post.url)
                    self.video.title = post.title
                    self.video.source_url = post.url
                    self.video.id = self.__extract_video_id(post.url)
                    self.video.status = "pending"
                    return self.video
        self.video.status = "error"
        return self.video