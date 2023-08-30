from bs4 import BeautifulSoup
import json
import requests
import ssl
import os
import urllib.request
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context

# Retrieve The URL
url = "https://www.snapchat.com/p/f3b6407f-4e84-4622-8974-c834d8cda0c3/2556654971109376"
r = requests.get(url)

# Scrape
soup = BeautifulSoup(r.content, 'html.parser')
script = soup.find("script", attrs={"id": "__NEXT_DATA__"})

# Extract and clean the JSON-like string
script_text = script.contents[0].strip()  # Extract the text content of the script tag
json_start = script_text.index("{")  # Find the starting point of the JSON object
json_end = script_text.rindex("}") + 1  # Find the ending point of the JSON object
json_str = script_text[json_start:json_end]

# Load the extracted JSON string
data = json.loads(json_str)

#### Save the data as a JSON file ####
# output_file_path = "output.json"
# with open(output_file_path, "w") as output_file:
#     json.dump(data, output_file, indent=4)
# print("Data saved to", output_file_path)

video_name = data['props']['pageProps']['linkPreview']['title']
video_link = data['props']['pageProps']['preselectedStory']['premiumStory']['playerStory']['snapList']

# Declare the media_url variable outside of the loop
media_url = None

# Iterate through the snapList items and find the one with snapIndex 0
for item in video_link:
    if item['snapIndex'] == 0:
        media_url = item['snapUrls']['mediaUrl']
        print("mediaUrl:", media_url)
        break  # Stop iterating


# download function
def download():
    if media_url is not None:
        # Create output folder if they don't exist
        os.makedirs("Videos", exist_ok=True)

        # Convert m3u8 to mp4 using subprocess
        subprocess.run(["ffmpeg", "-i", media_url, "-c", "copy", f"{video_name}.mp4"])
        
    else:
        print("Media URL is not available.")

# Call the download function
download()