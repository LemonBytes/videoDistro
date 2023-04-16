#!/usr/bin/python
import asyncio
from video_factory import VideoFactory


def main():
    # asyncio.run(get_reddit_videos(loop))
    video_factory = VideoFactory(max_limit=1)
    video_factory.start()

    # VideoFactory().loop(loop=loop)
    # edit_video()
    # publish_video()


if __name__ == "__main__":
    main()
