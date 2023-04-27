import json
import random
from dotenv import dotenv_values
from video import Video
import praw
import uuid

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


class Collector:
    domains = [
        "streamable.com",
        "streamin.one",
        "youtube.com",
        "youtu.be",
        "dubz.co",
        "gfycat.com",
    ]
    subreddits = [
        {
            "MMA": [
                "Full Fight",
                "FIGHT CLIP",
                "Highlights",
            ],
        },
        {
            "davidgoggins": ["Motivation", "Goggins Speaks"],
        },
        {
            "Boxing": [],
        },
    ]

    def __init__(self, origin, video: Video):
        self.origin = origin
        self.video = video

    def get_video(self) -> Video:
        if self.origin == "reddit":
            video = self.__get_reddit_video()
            return video
        else:
            self.video.status = "error"
            print("Error: Origin not found")
            return self.video

    def __get_reddit_video(self) -> Video:
        source = self.__get_subreddit()
        if len(source["flairs"]) > 0:
            chosenflair = "flair:" + random.choice(source["flairs"])
            print(f"Chosen flair: {chosenflair}")
        else:
            chosenflair = "*"
        subreddit_name = source["subreddit_name"]
        config = dotenv_values(".env")
        reddit = praw.Reddit(
            client_id=config["CLIENT_ID"],
            client_secret=config["CLIENT_SECRET"],
            user_agent="Wyzbits",
        )
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.search(chosenflair, syntax="lucene", limit=None):
            if self.__viable_video_source(post.url):
                if self.__is_video_unused(post.url, post.title):
                    self.video.source_url = post.url
                    self.video.title = post.title
                    self.video.id = self.__extract_video_id(post.url)
                    self.video.status = "pending"
                    return self.video
        self.video.status = "error"
        return self.video

    def __get_subreddit(self):
        subreddit = random.choice(self.subreddits)
        subreddit_name = list(subreddit.keys())[0]
        flairs = subreddit[subreddit_name]
        source = {"subreddit_name": subreddit_name, "flairs": flairs}
        return source

    def __viable_video_source(self, url):
        for domain in self.domains:
            if domain in url:
                return True
        return False

    def __extract_video_id(self, url):
        video_id = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
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
