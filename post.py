import requests
import os
from datetime import datetime

# Get access token from environment
access_token = os.getenv("ACCESS_TOKEN")
if not access_token:
    raise EnvironmentError("ACCESS_TOKEN not set in environment variables.")

headers = {
    "Authorization": f"Bearer {access_token}"
}

# Load exactly 4 viral posts from file
with open("viral_post.txt", "r", encoding="utf-8") as f:
    all_posts = [p.strip() for p in f.read().split("---") if p.strip()]

if len(all_posts) != 4:
    raise ValueError(f"Expected exactly 4 viral posts, found {len(all_posts)}.")

# Determine time-based index: 0 for 00:00, 1 for 06:00, etc.
utc_hour = datetime.utcnow().hour
index = (utc_hour // 6) % 4
quote_to_post = all_posts[index]

print(f"🕒 Current UTC hour: {utc_hour}")
print(f"📢 Posting quote #{index + 1}:\n{quote_to_post}\n")

# Step 1: Create post container
create_post_url = "https://graph.threads.net/me/threads"
params = {
    "text": quote_to_post,
    "media_type": "TEXT"
}
create_response = requests.post(create_post_url, headers=headers, params=params)
create_data = create_response.json()

creation_id = create_data.get("id")
if not creation_id:
    print("❌ Failed to create post:", create_data)
    exit()

# Step 2: Publish the post
publish_url = "https://graph.threads.net/me/threads_publish"
publish_params = {
    "creation_id": creation_id
}
publish_response = requests.post(publish_url, headers=headers, params=publish_params)

print("✅ Publish response:", publish_response.json())
