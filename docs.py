import os
import shutil
import requests


class Downloader:
    def __init__(self, source_url, download_path):
        self.source_url = source_url
        self.download_path = download_path

    def download(self):
        with requests.get(self.source_url, stream=True) as r:
            r.raise_for_status()
            with open(self.download_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)


class Editor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def edit(self):
        # Example editing process
        shutil.copyfile(self.input_path, self.output_path)


class Uploader:
    def __init__(self, destination_url, upload_path):
        self.destination_url = destination_url
        self.upload_path = upload_path

    def upload(self):
        with open(self.upload_path, "rb") as f:
            r = requests.post(self.destination_url, files={"file": f})
            r.raise_for_status()


class Video:
    def __init__(
        self,
        title,
        source_url,
        download_path,
        edit_path,
        upload_path,
        destination_url,
        file_size,
        video_length,
        video_parts,
    ):
        self.title = title
        self.source_url = source_url
        self.download_path = download_path
        self.edit_path = edit_path
        self.upload_path = upload_path
        self.destination_url = destination_url
        self.file_size = file_size
        self.video_length = video_length
        self.status = "pending"
        self.video_parts = video_parts


class Main:
    def __init__(self, video_list):
        self.video_list = video_list

    def run(self):
        for video in self.video_list:
            video.status = "downloading"
            video.download()

            video.status = "editing"
            video.edit()

            video.status = "uploading"
            video.upload()

            video.status = "complete"
