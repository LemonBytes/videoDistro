from typing import Optional

class Video:
    def __init__(
        self,
        id: Optional[str] = None,
        title: Optional[str] = None,
        source_url: Optional[str] = None,
        download_path: Optional[str] = None,
        edit_path: Optional[str] = None,
        upload_path: Optional[str] = None,
        file_size: Optional[float] = None,
        video_length: Optional[float] = None,
        video_parts: Optional[list] = None,
    ):
        self.id = id
        self.title = title
        self.source_url = source_url
        self.download_path = download_path
        self.edit_path = edit_path
        self.upload_path = upload_path
        self.file_size = file_size
        self.length = video_length
        self.status = "init"
        self.video_parts = video_parts or []
