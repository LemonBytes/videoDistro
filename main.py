from gather_videos import *
from edit_video import *
from upload_video_to_insta import *
from upload_video_to_tiktok import *
from upload_video_to_youtube import *
import subprocess


def main():

    get_reddit_videos()
    process = subprocess.Popen(["../tieUp.sh"])
    process.wait()
    # execute the edit_video function
    # edit_video()
    # upload_video_to_instagram()
    upload_video_to_youtube()


if __name__ == "__main__":
    main()
