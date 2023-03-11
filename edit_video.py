# edit the video video.mp4 so that it shows a text war of mind
from moviepy.editor import *
import os

IMAGEMAGICK_BINARY = os.getenv(
    'IMAGEMAGICK_BINARY', 'C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe')


def edit_video():
    clip = VideoFileClip("video.mp4")
    clip = clip.fx(vfx.mirror_x)
    (w, h) = clip.size

    crop_width = h * 9/16
    # x1,y1 is the top left corner, and x2, y2 is the lower right corner of the cropped area.

    x1, x2 = (w - crop_width)//1.6, (w+crop_width)//1.6
    y1, y2 = 0, h
    cropped_clip = vfx.crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)
    txt_clip = TextClip("War of Mind", fontsize=20,
                        color='black', font="Impact", kerning=5)
    txt_clip = txt_clip.set_pos('bottom').set_duration(clip.duration)
    result = CompositeVideoClip([cropped_clip, txt_clip])
    result.write_videofile("edited_video.mp4")
