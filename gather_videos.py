# create a script which downloads all the videos from a reddit thread
# and saves them to a folder
import praw
import urllib.request
import os
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}


def is_video_unused(url):
    with open('texts/downloaded_videos.txt', 'r') as f:
        if url in f.read():
            return False
    return True


def write_to_file(url):
    with open('texts/downloaded_videos.txt', 'a') as f:
        f.write(url + '\n')


def download_gfycat_videos(url):
    # get the video url
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    video_url = soup.find('source', type='video/mp4')['src']

    # download the video
    urllib.request.urlretrieve(video_url, os.path.basename("video.mp4"))
    # save the video to a folder
    os.rename(os.path.basename("video.mp4"),  os.path.basename("../inputVideo/video.mp4"))
    write_to_file(url)
    return True


def download_streamable_videos(url):
    # get the video url
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    try:
        video_url = soup.find('video', class_='video-player-tag')['src']
    except:
        return False
    
    with open('../inputVideo/video.mp4', 'wb') as f_out:
        r = requests.get("https:" + video_url, stream=True)
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f_out.write(chunk)
    write_to_file(url)
    return True


def get_reddit_videos():
    flair = ""
    # 50 chances to get a one of the flairs
    import random
    if random.random() < 0.5:
        flair = "FIGHT CLIP"
    else:
        flair = "Highlights"

    print(flair)

    # set up reddit instance
    reddit = praw.Reddit(client_id='m7zKZuiCyIz4XCQ45k8EuA',
                         client_secret='4grB2eRbkOkcVPCKv-_9cRjIlwJ7pQ', user_agent='wyzbits')
    # get the subreddit
    for post in reddit.subreddit("MMA").search('flair:' + flair, syntax='lucene', limit=100):
        # download the video
        if "gfycat" in post.url:
            if is_video_unused(post.url):
                if download_gfycat_videos(post.url):
                    # write the title to /texts/titles.txt
                    with open('texts/titles.txt', 'a') as f:
                        f.write(post.title + '\n')
                    break
        if "streamable" in post.url:
            if is_video_unused(post.url):
                if download_streamable_videos(post.url):
                    with open('texts/titles.txt', 'a') as f:
                        f.write(post.title + '\n')
                    break
