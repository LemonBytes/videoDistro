from pathlib import Path
import time
from src.video import Video
from src.video_factory import VideoFactory
import os
from sys import platform


def main():
    video_factory = VideoFactory(max_limit=1, inject=True)
    video_factory.start()


if __name__ == "__main__":
    main()
