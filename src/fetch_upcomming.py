import gdown


class FetchUpcomming:
    def __init__(self):
        self.url = "https://drive.google.com/file/d/19LeIAd_HvAaWVrAxht1gcclWyNh9V85U/view?usp=drive_link"
        self.output = "./upcoming_videos.json"

    def download_new_list(self):
        gdown.download(url=self.url, output=self.output, fuzzy=True)
