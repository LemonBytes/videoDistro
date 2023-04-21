import json
import os
from collector import Collector
from video import Video
from downloader import Downloader
from editor import Editor
import asyncio


class VideoFactory:
    next_upload_number = 0

    def __init__(self, max_limit=1) -> None:
        self.max_limit = max_limit
        self.limit = 0
        self.video_list = []

    def __get_next_upload_part(self):
        all_folders = os.listdir("./video_upload_queue")
        next_folder_by_number = 0
        for folder in all_folders:
            folder_number = folder.split("_")[0]
            if int(folder_number) > next_folder_by_number:
                next_folder_by_number = int(folder_number)
        self.next_upload_number = next_folder_by_number + 1

    def __create_folder(self, folder_name: str) -> None:
        try:
            os.mkdir(f"./video_upload_queue/{folder_name}")
        except Exception as e:
            print(e)

    def _update_video_json(self, video: Video) -> None:
        with open("./videos.json", "r") as f:
            data = json.load(f)
            videos = data["videos"]

        if len(videos) == 0:
            videos.append(video.__dict__)

        for json_video in videos:
            if json_video["id"] == video.id:
                json_video = video.__dict__
                break
            else:
                videos.append(video.__dict__)
                break

        with open("./videos.json", "w") as f:
            json.dump(data, f, indent=4)

    def start(self) -> None:
        while self.limit <= self.max_limit:
            if len(self.video_list) == 0:
                self.video_list.append(Video())
            for video in self.video_list:
                if video and isinstance(video, Video):
                    while video.status != "error" or video.status != "done":
                        self.__get_next_upload_part()
                        if video.status == "init":
                            collector = Collector(origin="reddit", video=video)
                            video = collector.get_video()
                            self._update_video_json(video)
                            break
                        elif video.status == "pending":
                            downloader = Downloader(video=video)
                            video = downloader.download()
                            print(video.status)
                        elif video.status == "downloaded":
                            self.__create_folder(
                                f"{self.next_upload_number}_{video.id}"
                            )
                            editor = Editor(
                                next_upload_number=self.next_upload_number, video=video
                            )
                            video = editor.edit()
                            self._update_video_json(video)
                            print(video.status)
                            self.limit = self.limit + 1
                            break
                        elif video.status == "edited" or video.status == "":
                            break
            break
