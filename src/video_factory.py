import json
import os
import random
from typing import Optional
from src.fetch_upcomming import FetchUpcomming
from src.injector import Injector
from src.notice_injector import NoticeInjector
from src.publisher import Publisher
from src.video import Video
from src.downloader import Downloader
from src.editor import Editor
from pathlib import Path


class VideoFactory:
    def __init__(
        self, max_limit=1, video: Optional[Video] = None, inject: Optional[bool] = None
    ) -> None:
        self.max_limit = max_limit
        self.limit = 0
        self.video = video
        self.inject = inject
        self.upload_queue = Path(
            os.path.abspath(
                f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/video_upload_queue/"
            )
        )
        self.video_folder = Path(
            os.path.abspath(
                f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/videos.json"
            )
        )

    def start(self) -> None:

        while self.limit <= self.max_limit:
            # folder has atleast on file because of git keep
            injector = Injector()
            if (
                len(os.listdir(self.upload_queue)) == 1
                and injector.get_len_of_upcomming() == 0
            ):
                notice_injector = NoticeInjector()
                fetch_upcomming = FetchUpcomming()
                self.video = notice_injector.inject_notice_video()
                fetch_upcomming.download_new_list()
                print("notice")
            elif len(os.listdir(self.upload_queue)) < 5:
                self.video = injector.inject_video()
                print("inject")
            if self.video is None:
                print("queue")
                self.video = self.__get_video_from_queue()
            while (
                self.video
                and isinstance(self.video, Video)
                and self.video.status not in ("done", "error")
            ):
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
                    quit()
                if self.video.status == "error":
                    print("resetting process")
                    self.limit = 0
                    self.video = Video(status="init")

            break

    def __create_folder(self, folder_name: str) -> None:
        try:
            os.mkdir(f"{self.upload_queue}/{folder_name}")
        except Exception as e:
            print(e)

    def _update_video_json(self, video: Video) -> None:
        with open(self.video_folder, "r") as f:
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
        with open(self.video_folder, "w") as f:
            json.dump(data, f, indent=4)

    def __get_video_from_queue(self) -> Video:
        folders = os.listdir(self.upload_queue)
        folders[:] = [firstchar for firstchar in folders if firstchar[0] != "."]

        video_id = random.choice(folders)
        with open(self.video_folder, "r") as f:
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
        folders = [f for f in os.listdir(self.upload_queue) if not f.startswith(".")]
        for folder in folders:
            if not os.listdir(f"{self.upload_queue}/{folder}"):
                os.rmdir(f"{self.upload_queue}/{folder}")
        video.video_parts.pop(0)
        print(video.video_parts)
        if len(video.video_parts) > 0:
            video.status = "queued"
            self._update_video_json(video)
