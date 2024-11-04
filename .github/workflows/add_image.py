import os
import re
import requests

# Extract the image URL from Markdown syntax (e.g., ![alt-text](URL))
issue_body = os.getenv("ISSUE_BODY")
match = re.search(r'!\[.*\]\((https?://\S+\.(?:jpg|jpeg|png|gif))\)', issue_body)

if match:
    image_url = match.group(1)  # Extracted URL part
    image_name = os.path.basename(image_url)
    image_path = f"hezbollah-martyrs/images/{image_name}"

    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception("Failed to download image")

else:
    raise Exception("No image URL found in the issue body")
