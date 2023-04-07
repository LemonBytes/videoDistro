import json
from math import floor
import subprocess
from ffmpeg import FFmpeg
import re
import os

# import sys

# sys.setrecursionlimit(10000)

SEGEMENT = 59


def extract_last_video():
    with open("videos.json", "r") as f:
        data = json.load(f)
        videos = data["videos"]
        last_video = videos[-1]
        video_url = last_video["video_url"]
        # return the last part after .com/ of the string
        video_id = video_url.split("/")[-1]
        video_title = last_video["video_title"]
        video_url = last_video["video_url"]
        return {"video_id": video_id, "video_title": video_title, "video_url": video_url}


def get_video_seconds():
    # get video length
    cmd_str = 'ffmpeg -i ./last_video_download/video.mp4 2>&1 | grep "Duration" | cut -d " " -f 4 | sed s/,//'
    # out = subprocess.run(cmd_str, shell=True, capture_output=True)
    output = subprocess.check_output(cmd_str, shell=True)
    output = output.decode("utf-8")
    seconds = 0
    for time in output.split(":"):
        seconds = seconds * 60 + float(time)
    return seconds


def update_json_parts(video_id):
    video = extract_last_video()
    parts = []
    #list the files alpabetically
    for file in sorted(os.listdir(f"./video_parts/{video_id}")):
        if file.endswith(".mp4"):
            parts.append(file)
    with open("video_parts.json", "r") as f:
        data = json.load(f)
        videos = data["video_parts"]
        videos.append(
            {
                "video_id": video["video_id"],
                "video_title": video["video_title"],
                "video_url": video["video_url"],
                "parts": parts,
            }
        )
    with open("video_parts.json", "w") as f:
        json.dump(data, f, indent=4)


    


def get_video_file_size():
    # get video file size
    cmd_str = "du -h ./last_video_download/video.mp4 | cut -f1"
    output = subprocess.check_output(cmd_str, shell=True)
    output = output.decode("utf-8")
    output = output.replace("M", "")
    # return output as float
    return float(output)


def create_folder(video_id):
    create_folder_cmd = f"mkdir ./video_parts/{video_id}"
    subprocess.run(create_folder_cmd, shell=True)


def cut_video(video_id, seconds_split):
    cut_video_cmd = f"ffmpeg -i ./last_video_download/video.mp4 -f segment -segment_time {seconds_split} -vcodec copy -acodec copy -reset_timestamps 1 -map 0:0 -map 0:1 ./video_parts/{video_id}/output_video_part_%d.mp4"
    subprocess.run(cut_video_cmd, shell=True)


def compress_video():
    compress_video_cmd = f"ffmpeg -i ./last_video_download/video.mp4 -vcodec libx264 -crf 23 ./last_video_download/video.mp4"
    subprocess.run(compress_video_cmd, shell=True)


def get_cutting_part(seconds, rest, segment_time=SEGEMENT, depth=1):
    # print(f"seconds: {seconds}")
    # print(f"segment_time: {segment_time}")
    # print(f"rest: {rest}")
    # print(f"depth: {depth}")

    base_approximation = 25 * (SEGEMENT / 60)

    approximation = base_approximation / depth

    if segment_time - rest < 3 and rest <= SEGEMENT and segment_time <= SEGEMENT:
        return segment_time
    parts = floor(seconds / segment_time)
    if not depth % 2 == 0:
        segment_time = segment_time - approximation
        rest += parts * approximation
    else:
        segment_time = segment_time + approximation
        rest -= parts * approximation
    return get_cutting_part(seconds, rest, segment_time, depth + 1)


def edit_video():
    video_id = extract_last_video()["video_id"]
    file_size = get_video_file_size()
    seconds = get_video_seconds()
    print(video_id)

    if (seconds <= 60 and file_size > 50):
        seconds = get_video_seconds()
    else:
        segment_time = get_cutting_part(seconds, seconds % SEGEMENT)
        create_folder(video_id)
        cut_video(video_id, segment_time)
        update_json_parts(video_id)



edit_video()
