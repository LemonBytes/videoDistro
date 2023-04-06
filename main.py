#!/usr/bin/python
import asyncio
from get_video_seconds import get_video_seconds
from gather_videos import *
from upload import upload_video
import subprocess
from time import sleep


def main():
    loop = asyncio.get_event_loop()
    asyncio.run(get_reddit_videos(loop))
    # upload_video()


if __name__ == "__main__":
    main()
