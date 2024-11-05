import os
import re
import requests
import pandas as pd
from datetime import datetime

print("Extract issue content")
# Extract issue content
issue_body = os.getenv("ISSUE_BODY")
lines = issue_body.splitlines()
record = {}
print("Parse fields from issue body")

# Match and extract image URL from Markdown-style image link in issue body
match = re.search(r'!\[.*\]\((https?://\S+)\)', issue_body)
image_path = ""
if match:
    image_url = match.group(1)  # Extracted URL part
    image_name = os.path.basename(image_url) + ".jpg"  # Ensure .jpg extension
    image_path = f"hezbollah-martyrs/images/{image_name}"

    print("Image URL found:", image_url)  # Debugging output

    # Download the image and save it to the specified path
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded and saved to {image_path}")
    else:
        print("Failed to download image")

# Parse fields from issue body
for line in lines:
    if line.startswith("Name:"):
        record["Name"] = line.split("Name:")[1].strip()
    elif line.startswith("Arabic Name:"):
        record["Arabic Name"] = line.split("Arabic Name:")[1].strip()
    elif line.startswith("Home Town:"):
        record["Home Town"] = line.split("Home Town:")[1].strip()
    elif line.startswith("Home Town in Arabic:"):
        record["Home Town in Arabic"] = line.split("Home Town in Arabic:")[1].strip()
    elif line.startswith("Day:"):
        record["Day"] = line.split("Day:")[1].strip()

# Add the Upload Date as the current date in dd/mm/yyyy format
record["Upload Date"] = datetime.now().strftime("%d/%m/%Y")

# Add the Image Path
record["Image Path"] = image_path

# Read the existing CSV file
print("Read the existing CSV file")
csv_file = "hezbollah-martyrs/hezbollah-martyrs.csv"
try:
    df = pd.read_csv(csv_file)
    # Set Index as the next integer after the current max index
    record["Index"] = df["Index"].max() + 1 if not df.empty else 1
except FileNotFoundError:
    # If the CSV file does not exist, create it with Index starting at 1
    df = pd.DataFrame(columns=["Index", "Name", "Arabic Name", "Home Town", "Home Town in Arabic", "Upload Date", "Image Path"])
    record["Index"] = 1

print("Parsed record:", record)  # Debugging output

# Append the new record to the DataFrame
df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)

# Save the updated CSV file
print("Save the updated CSV file")
df.to_csv(csv_file, index=False)
print("Record added to CSV successfully.")
