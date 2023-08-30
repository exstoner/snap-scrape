from bs4 import BeautifulSoup
import json
import requests
import ssl
import os
import subprocess
import time

def download_snapchat_video():
    ssl._create_default_https_context = ssl._create_unverified_context

    # Get the URL from the user
    url = input("Please enter the Snapchat URL: ")

    print("Fetching and processing video... ", end="", flush=True)
    
    try:
        # Retrieve The URL
        r = requests.get(url)

        # Scrape
        soup = BeautifulSoup(r.content, 'html.parser')
        script = soup.find("script", attrs={"id": "__NEXT_DATA__"})

        # Extract and clean the JSON-like string
        script_text = script.contents[0].strip()
        json_start = script_text.index("{")
        json_end = script_text.rindex("}") + 1
        json_str = script_text[json_start:json_end]

        # Load the extracted JSON string
        data = json.loads(json_str)

        video_name = data['props']['pageProps']['linkPreview']['title']
        video_link = data['props']['pageProps']['preselectedStory']['premiumStory']['playerStory']['snapList']

        # Declare the media_url variable outside of the loop
        media_url = None

        # Iterate through the snapList items and find the one with snapIndex 0
        for item in video_link:
            if item['snapIndex'] == 0:
                media_url = item['snapUrls']['mediaUrl']
                break

        # Download
        if media_url is not None:
            # Create output folder if they don't exist
            os.makedirs("Videos", exist_ok=True)

            # Convert m3u8 to mp4 using subprocess
            subprocess.run(["ffmpeg", "-i", media_url, "-c", "copy", os.path.join("Videos", f"{video_name}.mp4")])
            
            print("Done!")
            print(f"Video saved as 'Videos/{video_name}.mp4'")
        else:
            print("Error: Media URL is not available.")
    
    except Exception as e:
        print("\nAn error occurred:", str(e))

# Call the function
download_snapchat_video()
