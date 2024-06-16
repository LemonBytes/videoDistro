import json
import os
from pathlib import Path
import uuid
from src.video import Video


class Injector:
    def __init__(self):
        self.url = ""
        self.title = "Wish me luck!"
        self.directory = os.getcwd()
        self.upcoming_videos = self.upload_queue = Path(
            os.path.abspath(
                f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/upcoming_videos.json"
            )
        )

    def inject_video(self) -> Video:
        self.__inject_url()
        id = self.__extract_video_id(self.url)

        video = Video(
            id=id,
            title=self.title,
            source_url=self.url,
            file_size=None,
            video_length=None,
            queue_source=None,
            status="pending",
            video_parts=None,
        )
        return video

    def get_len_of_upcomming(self):
        with open(self.upcoming_videos, "r") as f:
            data = json.load(f)
            videos = data["upcoming_videos"]

        return len(videos)

    def __inject_url(self):
        with open(self.upcoming_videos, "r") as f:
            data = json.load(f)
            videos = data["upcoming_videos"]

        if len(videos) > 0:
            self.url = videos[0]
            videos.pop(0)
        with open(self.upcoming_videos, "w") as f:
            json.dump(data, f, indent=4)

    def __extract_video_id(self, url):
        video_id = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
        return video_id
