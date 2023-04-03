#!/usr/bin/python
from edit_video import edit_video
from gather_videos import *
from upload import upload_video
import subprocess
from time import sleep


def main():
    get_reddit_videos()
    upload_video()


if __name__ == "__main__":
    main()
