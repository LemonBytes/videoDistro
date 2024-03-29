from video import Video
from video_factory import VideoFactory


def main():
    video_factory = VideoFactory(max_limit=1, inject=None)
    video_factory.start()


if __name__ == "__main__":
    main()
