import json


def save_as_json():
    videos = [
        
    ]
    with open('texts/downloaded_videos.txt', 'r') as f:
       for line_no, line in enumerate(f):
           videos.append(
             {
            "video_url":line,
            "video_title": ""
            }, 
        )
      
         
    with open('texts/titles.txt', 'r') as f:
        for line_no, line in enumerate(f):
            videos[line_no]["video_title"] = line    # The content of the line is in variable 'line'

    with open('videos.json', 'w') as f:
        json.dump(videos, f, indent=4)
    
    
save_as_json()        