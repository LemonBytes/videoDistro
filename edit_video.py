import ffmpeg
import os


def edit_video():
    video = ffmpeg.input("/video/video.mp4")
    duration = video
    print(duration)


edit_video()
