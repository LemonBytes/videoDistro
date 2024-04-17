import time
import urllib.request
from bs4 import BeautifulSoup
import requests
from src.video import Video
from pytube import YouTube


class Downloader:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    default_download_path = "./last_video_download/video.mp4"

    def __init__(self, video: Video):
        self.video = video

    def __get_sources(self):
        sources = [
            {"domain": "youtu.be", "download_function": self.__download_from_youtube},
            {"domain": "dubz.co", "download_function": self.__download_dubz_videos},
            {
                "domain": "youtube.com",
                "download_function": self.__download_from_youtube,
            },
            {
                "domain": "gfycat.com",
                "download_function": self.__download_gfycat_videos,
            },
            {
                "domain": "streamable.com",
                "download_function": self.__download_streamable_videos,
            },
            {
                "domain": "streamin.one",
                "download_function": self.__download_streamin_videos,
            },
        ]
        return sources

    def download(self):
        try:
            if self.video.source_url is None:
                self.video.status = "error"
                return self.video
            else:
                for source in self.__get_sources():
                    if source["domain"] in self.video.source_url:
                        source["download_function"]()
                        self.video.status = "downloaded"
                        break
                else:
                    self.video.status = "error"
        except:
            self.video.status = "error"
        return self.video

    def __download_from_youtube(self, counter=0, new_url=""):
        if self.video.source_url is None:
            self.video.status = "error"
            raise Exception("No video source url")
        new_url = new_url
        try:
            if "youtu.be" in self.video.source_url and new_url == "":
                res = requests.get(self.video.source_url, allow_redirects=True)
                new_url = res.url
            yt = YouTube(self.video.source_url)
            stream = yt.streams.get_highest_resolution()
            stream.download("./last_video_download/", "video.mp4")  # type: ignore
            print("finished downloading video")
        except Exception as e:
            print(e)
            if counter > 200:
                print(e)
                raise Exception("Error downloading video")
            time.sleep(5)
            print(f"retry:{counter}")
            return self.__download_from_youtube(counter=counter + 1, new_url=new_url)

    def __download_dubz_videos(self):
        if self.video.source_url is None:
            self.video.status = "error"
            raise Exception("No video source url")
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
            self.video.status = "error"
            raise Exception("Error downloading video")

    def __download_gfycat_videos(self):
        if self.video.source_url is None:
            self.video.status = "error"
            raise Exception("No video source url")
        try:
            site = requests.get(self.video.source_url, headers=self.headers)
            soup = BeautifulSoup(site.content, "html.parser")
            video_url = soup.find("source", type="video/mp4")["src"]  # type: ignore
            urllib.request.urlretrieve(f"{video_url}", self.default_download_path)
            print("finished downloading video")
        except Exception as e:
            print(e)
            self.video.status = "error"
            raise Exception("Error downloading video")

    def __download_streamable_videos(self):
        if self.video.source_url is None:
            self.video.status = "error"
            raise Exception("No video source url")
        try:
            site = requests.get(self.video.source_url, headers=self.headers)
            soup = BeautifulSoup(site.content, "html.parser")
            video_url = soup.find("video", class_="video-player-tag")["src"]  # type: ignore
            with open("./last_video_download/video.mp4", "wb") as f_out:
                r = requests.get(f"https:{video_url}", stream=True)
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f_out.write(chunk)
            print("finished downloading video")
        except Exception as e:
            print(e)
            raise Exception("Error downloading video")

    def __download_streamin_videos(self):
        if self.video.source_url is None:
            self.video.status = "error"
            raise Exception("No video source url")
        try:
            site = requests.get(self.video.source_url, headers=self.headers)
            soup = BeautifulSoup(site.content, "html.parser")
            video_url = soup.find("video", class_="video-player-tag")["src"]  # type: ignore
            with open("./last_video_download/video.mp4", "wb") as f_out:
                r = requests.get(f"{video_url}", stream=True)
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f_out.write(chunk)
            print("finished downloading video")
        except Exception as e:
            print(e)
            raise Exception("Error downloading video")

    # def __download_reddit_videos(self):
    #     if self.video.source_url is None:
    #         self.video.status = "error"
    #         raise Exception("No video source url")
    #     try:
    #         data = requests.get(f"{self.video.source_url}.json").json()
    #         print(data)
    #         url = data[0]
    #         print(url)
    #     except Exception as e:
    #         print(e)
    #         self.video.status = "error"
    #         raise Exception("Error downloading video")
