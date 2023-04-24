import json
import os
import random
from collector import Collector
from publisher import Publisher
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
        first_folder = sorted(os.listdir("./video_upload_queue"))[0]
        video_id = first_folder.split("_")[1]
        with open("./videos.json", "r") as f:
            data = json.load(f)
            videos = data["videos"]
        for video in videos:
            if video["id"] == video_id:
                print(video)
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

    def __clean_up_video(self, video: Video) -> None:
        if video.queue_source is None:
            raise Exception("Queue source is not set")
        video_paths = os.listdir(video.queue_source)
        video_to_delete = os.path.join(video.queue_source, video_paths[0])
        os.remove(video_to_delete)
        video_path_after_clean_up = os.listdir(video.queue_source)
        if len(video_path_after_clean_up) == 0:
            os.rmdir(video.queue_source)
        if len(video.video_parts) > 0:
            video.video_parts.pop(0)
            self._update_video_json(video)

    def start(self) -> None:
        while self.limit <= self.max_limit:
            if len(self.video_list) == 0:
                random_number = random.randrange(1, 4)
                if random_number == 2:
                    print("new video")
                    self.video_list.append(Video(status="init"))
                else:
                    print("queue")
                    video = self.__get_video_from_queue()
                    self.video_list.append(video)

            for video in self.video_list:
                if video and isinstance(video, Video):
                    while video.status != "error" or video.status != "done":
                        self.__get_next_upload_part()
                        if video.status == "init":
                            collector = Collector(origin="reddit", video=video)
                            video = collector.get_video()
                            self._update_video_json(video)
                            print(video)
                        elif video.status == "pending":
                            print("3")
                            downloader = Downloader(video=video)
                            video = downloader.download()
                            self._update_video_json(video)
                            print(video)
                        elif video.status == "downloaded":
                            self.__create_folder(
                                f"{self.next_upload_number}_{video.id}"
                            )
                            editor = Editor(
                                next_upload_number=self.next_upload_number, video=video
                            )
                            video = editor.edit()
                            self._update_video_json(video)
                            print(video)
                        elif video.status == "edited" or video.status == "queued":
                            publisher = Publisher(video=video)
                            video = publisher.publish()
                            self._update_video_json(video)
                            print(video)
                        elif video.status == "done" or video.status == "queued":
                            self.__clean_up_video(video)
                            self.limit += 1
                            print(video)
                            break
            break
