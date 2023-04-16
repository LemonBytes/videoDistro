class Video:
    def __init__(
        self,
        title=None,
        source_url=None,
        download_path=None,
        edit_path=None,
        upload_path=None,
        file_size=None,
        video_length=None,
        video_parts=None,
    ):
        self.title = title
        self.source_url = source_url
        self.download_path = download_path
        self.edit_path = edit_path
        self.upload_path = upload_path
        self.file_size = file_size
        self.video_length = video_length
        self.status = "init"
        self.video_parts = video_parts or []
