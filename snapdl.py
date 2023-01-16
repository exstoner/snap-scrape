from bs4 import BeautifulSoup
import json
import requests
import urllib.request
import ssl
import os
import moviepy.editor as mp

ssl._create_default_https_context = ssl._create_unverified_context


def snapStory_downloader(url):

    # Retrieve The URL
    r = requests.get(url)

    # Scrape
    soup = BeautifulSoup(r.content, 'html.parser')
    script = soup.findAll("script", attrs={"id": "__NEXT_DATA__"})

    # Remove extra charachters from Script
    script = str(script)
    video = script.strip()[52:-10]

    # Load the scraped data in JSON
    data = json.loads(video)

    # Get data from JSON
    video_name = data['props']['pageProps']['linkPreview']['title']
    video_link = data['props']['pageProps']['preselectedStory']['premiumStory']['playerStory']['snapList']

    # Get list of links
    links = []

    for link in video_link:
        media_url = link['snapUrls']['mediaUrl']
        links.append(media_url)

    # Enumerate through the list of link and download each video
    for i, url in enumerate(links):
        file_name = 'clips/clip{}.mp4'.format(i)
        download_name = 'clip{}'.format(i)
        urllib.request.urlretrieve(url, file_name)
        print(f"Downloading {download_name}")

    print(f'{i} Clips where Downloded Successfully')
    return video_name


def concatenate_videos(dir_path, video_name):
    # Get all video files in the directory
    video_files = [f for f in os.listdir(dir_path) if f.endswith('.mp4')]
    # Sort the video files by name (using the numerical part of the filename)
    video_files = sorted(video_files, key=lambda x: int(x.split("clip")[-1].split(".")[0]))
    # Create an empty list to store the video clips
    clips = []
    # Iterate through the video files and add them to the list of clips
    for video in video_files:
        video_path = os.path.join(dir_path, video)
        clip = mp.VideoFileClip(video_path)
        clips.append(clip)
    # Concatenate the clips and create the final video
    final_video = mp.concatenate_videoclips(clips, method="compose")
    final_video.write_videofile(f"export/{video_name}.mp4",audio_codec='aac')

    
# Execute

url = input('Enter the SnapStory URL : ')
video_name = snapStory_downloader(url)
dir_path = "/Users/xxxx/Downloads/scrap-snap/clips"

if snapStory_downloader(url):
    concatenate_videos(dir_path, video_name)
    print(f'{video_name} - Video is Downloded Successfully - Check The Export Folder')
    # Delete All clips from Clips folder
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
