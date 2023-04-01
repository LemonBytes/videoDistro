# edit the video video.mp4 so that it shows a text war of mind
from moviepy.editor import *
import os

IMAGEMAGICK_BINARY = os.getenv(
    'IMAGEMAGICK_BINARY', 'C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe')


def edit_video():
    clip = VideoFileClip("../inputVideo/video.mp4")
    # create a subclip of the video from 0 to 55 seconds
    clip = clip.subclip(0, 55)
    # create a text clip
    txt_clip = TextClip("War of Mind", fontsize=70, color='white')
    # set the position of the text clip
    txt_clip = txt_clip.set_pos('center').set_duration(55)
    # overlay the text clip on the video clip
    video = CompositeVideoClip([clip, txt_clip])
    # write the result to a file
    video.write_videofile("../inputVideo/cutvideo.mp4", fps=25, codec='mpeg4')
