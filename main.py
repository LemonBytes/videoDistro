from gather_videos import *
from edit_video import *
from upload_video_to_insta import *
from upload_video_to_tiktok import *
from upload_video_to_youtube import *
import subprocess


def main():

    get_reddit_videos()
    subprocess.call("../tieUp.sh")
    # execute the edit_video function
    # edit_video()
    # upload_video_to_instagram()
    upload_video_to_youtube()


if __name__ == "__main__":
    main()
