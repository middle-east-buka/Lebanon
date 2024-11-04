import os
import re
import requests

# Extract issue content
issue_body = os.getenv("ISSUE_BODY")
print("Issue body content 88 :", issue_body)  # Debugging output

# Regex pattern to match image URL in Markdown format
match = re.search(r'!\[.*\]\((https?://\S+)\)', issue_body)

if match:
    image_url = match.group(1)  # Extracted URL part
    image_name = os.path.basename(image_url)+".jpg"
    image_path = f"hezbollah-martyrs/images/{image_name}"

    print("Image URL found:", image_url)  # Debugging output

    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved to {image_path}")
    else:
        raise Exception("Failed to download image")
else:
    print("No image URL found in the issue body")
    raise Exception("No image URL found in the issue body")
