import os
from pathlib import Path
import gdown


class FetchUpcomming:
    def __init__(self):
        self.url = "https://drive.google.com/file/d/19LeIAd_HvAaWVrAxht1gcclWyNh9V85U/view?usp=drive_link"
        self.upcoming_videos = self.upload_queue = Path(
            os.path.abspath(
                f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/last_video_download/video.mp4"
            )
        )

    def download_new_list(self):
        gdown.download(url=self.url, output=self.upcoming_videos, fuzzy=True)
