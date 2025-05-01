import requests
import random
import os

# Get access token from environment
access_token = os.getenv("ACCESS_TOKEN")
if not access_token:
    raise EnvironmentError("ACCESS_TOKEN not set in environment variables.")

headers = {
    "Authorization": f"Bearer {access_token}"
}

# Load viral posts from file
with open("viral_post.txt", "r", encoding="utf-8") as f:
    all_posts = [p.strip() for p in f.read().split("---") if p.strip()]

# Load already posted posts
posted_file = "posted_viral.txt"
if os.path.exists(posted_file):
    with open(posted_file, "r", encoding="utf-8") as f:
        posted_quotes = set(line.strip() for line in f if line.strip())
else:
    posted_quotes = set()

# Filter out already posted quotes
unposted_quotes = [q for q in all_posts if q not in posted_quotes]

if not unposted_quotes:
    print("✅ All viral posts have been posted for today.")
    exit()

# Pick a random unposted post
quote_to_post = random.choice(unposted_quotes)
print(f"📢 Posting viral quote:\n{quote_to_post}\n")

# Step 1: Create the post container
create_post_url = "https://graph.threads.net/me/threads"
params = {
    "text": quote_to_post,
    "media_type": "TEXT"
}
create_response = requests.post(create_post_url, headers=headers, params=params)
create_data = create_response.json()

creation_id = create_data.get("id")
if not creation_id:
    print("❌ Failed to get creation_id:", create_data)
    exit()

# Step 2: Publish the post
publish_url = "https://graph.threads.net/me/threads_publish"
publish_params = {
    "creation_id": creation_id
}
publish_response = requests.post(publish_url, headers=headers, params=publish_params)
print("✅ Publish response:", publish_response.json())

# Step 3: Record the posted quote
with open(posted_file, "a", encoding="utf-8") as f:
    f.write(quote_to_post + "\n")
