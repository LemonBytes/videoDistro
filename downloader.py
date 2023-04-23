import urllib.request
from bs4 import BeautifulSoup
import requests
from video import Video
from pytube import YouTube


class Downloader:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    default_download_path = "./last_video_download"

    def __init__(self, video: Video):
        self.video = video

    def download(self) -> Video:
        if  self.video.source_url is None:
          self.video.status = "error"  
          return self.video
        if "youtu.be" or "youtube.com" in self.video.source_url:
              self.__download_from_youtube()
              self.video.status = "downloaded"
        elif "streamable.com" or "streamin.one" in self.video.source_url:
              self.__download_streamable_videos()
              self.video.status = "downloaded"      
        elif "dubz.co" in self.video.source_url:
              self.__download_dubz_videos()
              self.video.status = "downloaded"
        elif "gfycat.com" in self.video.source_url:
              self.__download_gfycat_videos()
              self.video.status = "downloaded"
        else:
              self.video.status = "error"          
        return self.video      

    def __download_from_youtube(self, counter=0):
        if self.video.source_url is None:
                self.video.status = "error"
                raise Exception("No video source url")
        try:
            yt = YouTube(self.video.source_url) 
            stream = yt.streams.get_highest_resolution()
            stream.download(self.default_download_path, "video.mp4")  # type: ignore
            print("finished downloading video")
        except Exception as e:
            if counter > 10:
                self.video.status = "error"
                print(e)
                raise Exception("Error downloading video")
            self.__download_from_youtube(counter=counter+1)


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

   