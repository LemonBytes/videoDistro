import urllib
from bs4 import BeautifulSoup
import requests
from video import Video
from pytube import YouTube


class Downloader:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    default_download_path = "./last_video_download/video.mp4"

    def __init__(self, video: Video) -> None:
        self.video = video

    def download(self) -> Video:
        if "youtu.be" in self.video.source_url:
            self.__download_from_youtube()
        elif "dubz" in self.video.source_url:
            self.__download_dubz_videos()
        elif "gfycat" in self.video.source_url:
            self.__download_gfycat_videos()
        self.video.status = "downloaded"
        return self.video

    def __download_from_youtube(self):
        try:
            yt = YouTube(self.video.source_url)
            stream = yt.streams.get_highest_resolution()
            stream.download(self.default_download_path)  # type: ignore
        except Exception as e:
            print(e)
            raise Exception("Error downloading video")

    def __download_dubz_videos(self):
        try:
            site = requests.get(self.video.source_url, headers=self.headers)
            print(site.content)
            soup = BeautifulSoup(site.content, "html.parser")
            video_url = soup.find("video")["src"]  # type: ignore
            print(video_url)
            opener = urllib.request.build_opener()
            opener.addheaders = [("User-agent", "Mozilla/5.0")]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(f"{video_url}", self.default_download_path)
            print("finished downloading video")
        except Exception as e:
            print(e)
            raise Exception("Error downloading video")

    def __download_gfycat_videos(self):
        try:
            site = requests.get(self.video.source_url, headers=self.headers)
            soup = BeautifulSoup(site.content, "html.parser")
            video_url = soup.find("source", type="video/mp4")["src"]  # type: ignore
            urllib.request.urlretrieve(f"{video_url}", self.default_download_path)
            print("finished downloading video")
        except Exception as e:
            print(e)
            raise Exception("Error downloading video")
