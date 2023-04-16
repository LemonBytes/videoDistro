from collector import Collector
from video import Video
from downloader import Downloader
from editor import Editor
import asyncio


class VideoFactory:
    def __init__(self, max_limit=1) -> None:
        self.max_limit = max_limit
        self.limit = 0
        self.video_list = []

    def start(self) -> None:
        while self.limit <= self.max_limit:
            if len(self.video_list) == 0:
                self.video_list.append(Video())

            # gibt es videos in der queue?
            # geh durch die queue und lade pro video den nächsten part hoch

            for video in self.video_list:
                print("Iterator")
                if video and isinstance(video, Video):
                    while video.status != "error" or video.status != "done":
                        if video.status == "init":
                            print("EL COLECTOR")
                            collector = Collector(origin="reddit", video=video)
                            video = collector.get_video()
                            print(video.status)
                        elif video.status == "pending":
                            downloader = Downloader(video=video)
                            video = downloader.download()
                            print(video.status)
                        elif video.status == "downloaded":
                            editor = Editor(video=video)
                            video = editor.edit ()
                            self.limit = self.limit + 1
                            break
            break    
        