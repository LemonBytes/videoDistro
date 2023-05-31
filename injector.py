import uuid
from video import Video


class Injector:
    def __init__(self):
        self.url = ""
        self.title = ""

    def injectVideo(self) -> Video:
        self.__take_user_input()
        id = self.__extract_video_id(self.url)    

        video =  Video(
                    id=id,
                    title=self.title,
                    source_url=self.url,
                    file_size=None,
                    video_length=None,
                    queue_source=None,
                    status="pending",
                    video_parts=None,
                )
        return video  


    def __take_user_input(self):
        self.url  = input("Enter url:")
        self.title = input("Enter title:")


    def __extract_video_id(self, url):
        video_id = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
        return video_id