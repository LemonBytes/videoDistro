from src.video import Video


class NoticeInjector:
    def __init__(self):
        self.url = ""
        self.title = "Wish me luck!"

    def inject_notice_video(self) -> Video:

        video = Video(
            id="notice_video",
            title="notice_video",
            source_url="notice_video",
            file_size=None,
            video_length=None,
            queue_source="./notice_video/notice_video.mp4",
            status="queued",
            video_parts=None,
        )
        return video
