from typing import Optional


class Video:
    def __init__(
        self,
        id: Optional[str] = None,
        title: Optional[str] = None,
        source_url: Optional[str] = None,
        file_size: Optional[float] = None,
        video_length: Optional[float] = None,
        queue_source: Optional[str] = None,
        status: Optional[str] = None,
        video_parts: Optional[list] = None,
    ):
        self.id = id
        self.title = title
        self.source_url = source_url
        self.file_size = file_size
        self.length = video_length
        self.queue_source = queue_source
        self.status = status
        self.video_parts = video_parts or []
