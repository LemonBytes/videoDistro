import json
from math import floor
import os
import ffmpeg
from video import Video

class Editor:
    SEGEMENT = 55

    def __init__(self, video: Video, next_upload_number: int):
        self.video = video
        self.next_upload_number = next_upload_number
    
    def edit(self) -> Video:
        video = self.__get_meta_data()
        if video.file_size  is not None and video.length is not None:
            if video.length < 60 and video.file_size > 50:
                self.__compress_video()
                return self.video
            elif video.length > 60:
                video = self.__split_video()
                return video
            else:
                video = self.__move_video()
                return self.video
        self.video.status = "error"
        return self.video    
            

    def __get_meta_data(self) -> Video:
        self.video = self.__get_video_seconds()
        self.video = self.__get_video_file_size()
        return self.video

    def __get_video_seconds(self) -> Video:
        try:
            probe = ffmpeg.probe("./last_video_download/video.mp4")
            video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
            duration = float(video_info['duration'])
            self.video.length = duration
            return self.video
        except StopIteration:
            self.video.status = "error"
            self.video.length = 0
            return self.video
        

    def __get_video_file_size(self) -> Video:
        input = os.path.getsize("./last_video_download/video.mp4")
        mega_bytes = input / 1024 / 1024
        self.video.file_size = mega_bytes
        print(f"Video file size: {mega_bytes} MB")
        return self.video
    
        

    def __compress_video(self) -> Video:
        input_file = "./last_video_download/video.mp4"
        output_file = f"./video_upload_queue/{self.next_upload_number}_{self.video.id}/{self.video.id}_video.mp4"

        # specify output format and encoding options
        output_options = {
            "c:v": "libx264",    # video codec
            "crf": "28",         # constant rate factor, lower means higher quality (18-28 recommended)
            "preset": "medium",  # encoding speed vs. compression ratio, "medium" is a good balance
            "c:a": "copy",       # keep original audio codec and quality
        }

        # create a FFmpeg command
        ffmpeg_cmd = (
            ffmpeg
            .input(input_file)
            .output(output_file, **output_options)
            .overwrite_output()
        )

        # run the command
        ffmpeg_cmd.run()

        self.video.status = "edited"
        self.video.queue_source = output_file
        return self.video
                
                   

    def __split_video(self) -> Video:
        input_file = "./last_video_download/video.mp4"   
        output_directory = f"./video_upload_queue/{self.next_upload_number}_{self.video.id}"
        split_time = self.__get_cutting_part(self.video.length)
        segment_time = split_time

        (
            ffmpeg
            .input(input_file)
            .output(
                output_directory + f"{self.video.id}_video_part_%d.mp4",
                f="segment",
                segment_time=segment_time,
                vcodec="copy",
                acodec="copy",
                reset_timestamps=1,
                map="0:0",
            )
            .run()
        )

        self.video.video_parts = os.listdir(output_directory)
        self.video.status = "edited"
        self.video.queue_source = output_directory
        return self.video
    
       
        
    def __get_cutting_part(self, seconds, segment_time=SEGEMENT):
        if seconds % segment_time <= 1 and segment_time <= self.SEGEMENT:
            return segment_time
        elif segment_time <= 30:
            return segment_time
        return self.__get_cutting_part(seconds=seconds, segment_time=segment_time - 1)
    

 
    def __move_video(self) -> Video:
        os.rename("./last_video_download/video.mp4", f"./video_upload_queue/{self.next_upload_number}_{self.video.id}/{self.video.id}_video.mp4")
        self.video.queue_source = f"./video_upload_queue/{self.next_upload_number}_{self.video.id}/{self.video.id}_video.mp4"
        self.video.status = "edited"
        return self.video

   

       
  



# def extract_last_video():
#     with open("videos.json", "r") as f:
#         data = json.load(f)
#         videos = data["videos"]
#         last_video = videos[-1]
#         video_url = last_video["video_url"]
#         # return the last part after .com/ of the string
#         if "youtube" in video_url:
#             video_id = video_url.split("=")[-1]
#             print(video_id)
#         else:
#             video_id = video_url.split("/")[-1]
#             print(video_id)

#         video_title = last_video["video_title"]
#         video_url = last_video["video_url"]
#         return {
#             "video_id": video_id,
#             "video_title": video_title,
#             "video_url": video_url,
#         }


# def get_video_seconds():
#     try:
#         # get video length
#         cmd = "ffmpeg -i ./last_video_download/video.mp4 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
#         output = subprocess.check_output(cmd, shell=True)
#         output = output.decode("utf-8").strip()
#         print(output)
#         seconds = 0
#         for time in output.split(":"):
#             if not time:
#                 continue
#             seconds = seconds * 60 + float(time)
#         return seconds
#     except (subprocess.CalledProcessError, ValueError) as e:
#         print(f"Error getting video length: {e}")
#         return 0


# def update_json_parts(video_id):
#     video = extract_last_video()
#     parts = []
#     # list the files alpabetically
#     for file in sorted(os.listdir(f"./video_parts/{video_id}")):
#         if file.endswith(".mp4"):
#             parts.append(file)
#     with open("video_parts.json", "r") as f:
#         data = json.load(f)
#         videos = data["video_parts"]
#         videos.append(
#             {
#                 "video_id": video["video_id"],
#                 "video_title": video["video_title"],
#                 "video_url": video["video_url"],
#                 "parts": parts,
#             }
#         )
#     with open("video_parts.json", "w") as f:
#         json.dump(data, f, indent=4)


# def get_first_video_with_parts():
#     with open("video_parts.json", "r") as file:
#         data = json.load(file)
#         videos = data["video_parts"]
#         for video in videos:
#             if len(video["parts"]) > 0:
#                 return f"./video_parts/{video['video_id']}/{video['parts'][0]}"


# def get_video_file_size():
#     # get video file size with ff
#     cmd_str = "du -h ./last_video_download/video.mp4 | cut -f1"
#     output = subprocess.check_output(cmd_str, shell=True)
#     output = output.decode("utf-8")
#     output = output.replace("M", "")
#     # return output as float
#     return float(output)


# def create_folder(video_id):
#     create_folder_cmd = f"mkdir ./video_parts/{video_id}"
#     subprocess.run(create_folder_cmd, shell=True)


# def cut_video(video_id, seconds_split):
#     cut_video_cmd = f"ffmpeg -i ./last_video_download/video.mp4 -f segment -segment_time {seconds_split} -vcodec copy -acodec copy -reset_timestamps 1 -map 0:0 -map 0:1 ./video_parts/{video_id}/{video_id}_video_part_%d.mp4"
#     subprocess.run(cut_video_cmd, shell=True)


# def compress_video():
#     compress_video_cmd = f"ffmpeg -i ./last_video_download/video.mp4 -vcodec libx264 -crf 23 ./edit_video/video.mp4 "
#     subprocess.run(compress_video_cmd, shell=True)


# def write_to_queue(scrFolder, video_folder_src, title):
#     cmd = f"mv {scrFolder} ./video_upload_queue/{video_folder_src}"
#     # write to queue json
#     with open("queue.json", "r") as f:
#         data = json.load(f)
#         queue = data["queue"]
#         queue.append(
#             {
#                 "video_src": video_folder_src,
#                 "video_title": title,
#             }
#         )
#     with open("queue.json", "w") as f:
#         json.dump(data, f, indent=4)
#     subprocess.run(cmd, shell=True)


# def clean_up_by_id(video_id):
#     with open("video_parts.json", "r") as f:
#         data = json.load(f)
#         videos = data["video_parts"]
#         for video in videos:
#             if video["video_id"] == video_id:
#                 video["parts"].pop(0)
#     with open("video_parts.json", "w") as f:
#         json.dump(data, f, indent=4)


# def delete_video():
#     delete_video_cmd = "rm -rf ./last_video_download/video.mp4"
#     subprocess.run(delete_video_cmd, shell=True)


# def get_cutting_part(seconds, segment_time=SEGEMENT):
#     if seconds % segment_time <= 1 and segment_time <= SEGEMENT:
#         return segment_time
#     elif segment_time <= 30:
#         return segment_time
#     return get_cutting_part(seconds=seconds, segment_time=segment_time - 1)


# def edit_video():
#     video_id = extract_last_video()["video_id"]
#     title = extract_last_video()["video_title"]
#     file_size = get_video_file_size()
#     seconds = get_video_seconds()
#     if seconds <= 60 and file_size > 50:
#         compress_video()
#         write_to_queue("./edit_video/video.mp4", f"{video_id}_video.mp4", title)
#     elif seconds > 60:
#         segment_time = get_cutting_part(seconds)
#         create_folder(video_id)
#         cut_video(video_id, segment_time)
#         update_json_parts(video_id)
#         delete_video()
#         write_to_queue(
#             f"video_parts/{video_id}/{video_id}_video_part_0.mp4",
#             f"{video_id}_video_part_0.mp4",
#             title + " - Part 1 ",
#         )
#         clean_up_by_id(video_id)
#     else:
#         write_to_queue(
#             "./last_video_download/video.mp4", f"{video_id}_video.mp4", title
#         )