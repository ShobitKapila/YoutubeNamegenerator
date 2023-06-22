import csv
from googleapiclient.discovery import build


api_key = "AIzaSyAHmhtuqgRtvFVup07PUhc7w1F2n1Is9xg"
youtube = build("youtube", "v3", developerKey=api_key)
channel_id = "UCtFRv9O2AHqOZjjynzrv-xg"

videos = youtube.search().list(part="snippet", channelId=channel_id, maxResults=50).execute()
data = []

for video in videos["items"]:
    title = video["snippet"]["title"]
    views = "N/A"
    likes = "N/A"
    if "viewCount" in video["snippet"]:
        views = video["snippet"]["viewCount"]
    if "likeCount" in video["snippet"]:
        likes = video["snippet"]["likeCount"]
    data.append([title, views, likes])
csv_file = "learning_name.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Video Name", "Views", "Likes"])  
    writer.writerows(data) 

print("Data scraped and saved successfully to", csv_file)
