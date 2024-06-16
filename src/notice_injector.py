import os
from pathlib import Path
from src.video import Video


class NoticeInjector:
    def __init__(self):
        self.url = ""
        self.title = "Wish me luck!"
        self.notice_video = self.upload_queue = Path(
            os.path.abspath(
                f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/notice_video/notice_video.mp4"
            )
        )

    def inject_notice_video(self) -> Video:

        video = Video(
            id="notice_video",
            title="notice_video",
            source_url="notice_video",
            file_size=None,
            video_length=None,
            queue_source=f"{self.notice_video}",
            status="queued",
            video_parts=None,
        )
        return video
