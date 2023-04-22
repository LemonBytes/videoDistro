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
        output_directory = f"./video_upload_queue/{self.next_upload_number}_{self.video.id}/"
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

        #list directory alphhabetic

        self.video.video_parts = sorted(os.listdir(output_directory))
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

   

    