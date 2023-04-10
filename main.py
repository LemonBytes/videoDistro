#!/usr/bin/python
import asyncio
from edit_video import edit_video
from gather_videos import *
from upload import upload_video
import subprocess
from time import sleep


def main():
    #loop = asyncio.get_event_loop()
    #asyncio.run(get_reddit_videos(loop))
    edit_video()
    upload_video()


if __name__ == "__main__":
    main()
