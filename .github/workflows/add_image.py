import os
import re
import requests

# Extract image URL from issue body (assuming it’s included as a direct URL)
issue_body = os.getenv("ISSUE_BODY")
image_urls = re.findall(r'(https?://\S+\.(?:jpg|jpeg|png|gif))', issue_body)

if image_urls:
    image_url = image_urls[0]  # Use the first image URL found
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
