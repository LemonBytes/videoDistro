from video import Video
from video_factory import VideoFactory

video =  Video(
                    id="3d8b85f1-a399-56bc-bcaf-38785d889549",
                    title="BKFC Michael Venom Page vs. Mike Perry",
                    source_url="https://www.youtube.com/watch?v=LREGoZInYCo",
                    file_size=None,
                    video_length=None,
                    queue_source=None,
                    status="pending",
                    video_parts=None,
                )
def main():

    video_factory = VideoFactory(max_limit=1, video=video)
    video_factory.start()


if __name__ == "__main__":
    main()
