import json
import os
import random
from typing import Optional
from collector import Collector
from injector import Injector
from publisher import Publisher
from video import Video
from downloader import Downloader
from editor import Editor


class VideoFactory:
    def __init__(self, max_limit=1, video: Optional[Video] = None, inject:Optional[bool] = None) -> None:
        self.max_limit = max_limit
        self.limit = 0
        self.video = video
        self.inject = inject


    def start(self) -> None:
        while self.limit <= self.max_limit:
            if self.video is None and self.inject is None:
                if len(os.listdir("./video_upload_queue")) < 2:
                    print("new video queue")
                    self.video = Video(status="init")
                else:
                    if random.randint(1, 1000) == 3:
                        print("new video")
                        self.video = Video(status="init")
                    else:
                        print("queue")
                        self.video = self.__get_video_from_queue()
                        print(self.video.status)
            if self.inject:         
                injector = Injector()
                self.video = injector.injectVideo()                          
            while (
                self.video
                and isinstance(self.video, Video)
                and self.video.status not in ("done", "error")
            ):
                if self.video.status == "init":
                    print("init")
                    collector = Collector(origin="reddit", video=self.video)
                    self.video = collector.get_video()
                    self._update_video_json(self.video)
                    print(self.video.status)
                if self.video.status == "pending":
                    downloader = Downloader(video=self.video)
                    self.video = downloader.download()
                    self._update_video_json(self.video)
                    print(self.video.status)
                if self.video.status == "downloaded":
                    self.__create_folder(f"{self.video.id}")
                    editor = Editor(video=self.video)
                    self.video = editor.edit()
                    self._update_video_json(self.video)
                    print(self.video.status)
                if self.video.status == "edited" or self.video.status == "queued":
                    publisher = Publisher(video=self.video)
                    self.video = publisher.publish()
                    self._update_video_json(self.video)
                    print(self.video.status)
                if self.video.status == "done":
                    self.limit += 1
                    self.__clean_up_process(self.video)
                    print("clean up successfull")
                    break
                if self.video.status == "error":
                    print("resetting process")
                    self.limit = 0
                    self.video = Video(status="init")

            break

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

        video_exists = False
        index = 0
        for i, v in enumerate(videos):
            if v["id"] == video.id:
                video_exists = True
                index = i
                break
        if video_exists:
            videos[index] = video.__dict__
        else:
            videos.append(video.__dict__)
        with open("./videos.json", "w") as f:
            json.dump(data, f, indent=4)

    def __get_video_from_queue(self) -> Video:
        folders = os.listdir("./video_upload_queue")
        video_id = random.choice(folders)
        with open("./videos.json", "r") as f:
            data = json.load(f)
            videos = data["videos"]
        for video in videos:
            if video["id"] == video_id:
                print(video_id) 
                return Video(
                    id=video["id"],
                    title=video["title"],
                    source_url=video["source_url"],
                    file_size=video["file_size"],
                    video_length=video["length"],
                    queue_source=video["queue_source"],
                    status=video["status"],
                    video_parts=video["video_parts"],
                )
        return Video()

    def __clean_up_process(self, video: Video) -> None:
        if video.queue_source is None:
            raise Exception("Queue source is not set")
        video_paths = video.queue_source
        video_to_delete = video_paths + video.video_parts[0]
        os.remove(video_to_delete)
        folders = [f for f in os.listdir("./video_upload_queue") if not f.startswith('.')]
        for folder in folders:
            if not os.listdir(f"./video_upload_queue/{folder}"):
                os.rmdir(f"./video_upload_queue/{folder}")
        video.video_parts.pop(0)
        print(video.video_parts)
        if len(video.video_parts) > 0:
            video.status = "queued"
            self._update_video_json(video)
