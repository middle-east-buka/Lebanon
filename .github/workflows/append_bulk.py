import os
import re
import requests
import pandas as pd
from datetime import datetime

# Extract issue content from the ISSUE_BODY environment variable
issue_body = os.getenv("ISSUE_BODY")
print("Issue body content:", issue_body)  # Debugging output

# Paths
csv_file = "hezbollah-martyrs/hezbollah-martyrs.csv"
image_dir = "hezbollah-martyrs/images/"

# Regex pattern to match individual records in the issue body
record_pattern = re.compile(r'### Record \d+\s+[-*] Name:\s*(.*?)\s+[-*] Arabic Name:\s*(.*?)\s+[-*] Home Town:\s*(.*?)\s+[-*] Home Town in Arabic:\s*(.*?)\s+[-*] Day \(dd/mm/yyyy\):\s*(.*?)\s+[-*] Image Path:\s*(!\[[^\]]*\]\((https?://[^\)]+)\))?', re.DOTALL)

# Read the existing CSV file or create a new one if it doesn't exist
try:
    df = pd.read_csv(csv_file)
    next_index = df["Index"].max() + 1 if not df.empty else 1
except FileNotFoundError:
    df = pd.DataFrame(columns=["Index", "Name", "Arabic Name", "Home Town", "Home Town in Arabic", "Day", "Upload Date", "Image Path"])
    next_index = 1

# Process each matched record
records = []
for match in record_pattern.findall(issue_body):
    name, arabic_name, home_town, home_town_arabic, day, _, image_url = match
    record = {
        "Index": next_index,
        "Name": name.strip(),
        "Arabic Name": arabic_name.strip(),
        "Home Town": home_town.strip(),
        "Home Town in Arabic": home_town_arabic.strip(),
        "Day": day.strip(),
        "Upload Date": datetime.now().strftime("%d/%m/%Y"),
        "Image Path": ""
    }

    # If an image URL is provided, download and save it
    if image_url:
        image_name = f"{os.path.basename(image_url)}_{next_index}.jpg"  # Ensure a unique filename
        image_path = os.path.join(image_dir, image_name)
        
        print("Image URL found:", image_url)  # Debugging output
        
        response = requests.get(image_url)
        if response.status_code == 200:
            # Ensure the image directory exists
            os.makedirs(image_dir, exist_ok=True)
            
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded and saved to {image_path}")
            record["Image Path"] = image_path
        else:
            print(f"Failed to download image for record {next_index}")

    # Add the record to the list of records to append
    records.append(record)
    next_index += 1  # Increment index for each new record

# Append all new records to the DataFrame
df = pd.concat([df, pd.DataFrame(records)], ignore_index=True)

# Save the updated CSV file
print("Save the updated CSV file")
df.to_csv(csv_file, index=False)
print("All records added to CSV successfully.")

