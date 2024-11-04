import os
import pandas as pd
print("Extract issue content")
# Extract issue content
issue_body = os.getenv("ISSUE_BODY")
lines = issue_body.splitlines()
record = {}
print("Parse fields from issue body")

match = re.search(r'!\[.*\]\((https?://\S+)\)', issue_body)
image_path = ""
if match:
    image_url = match.group(1)  # Extracted URL part
    image_name = os.path.basename(image_url)+".jpg"
    image_path = f"hezbollah-martyrs/images/{image_name}"

    print("Image URL found:", image_url)  # Debugging output

# Parse fields from issue body
for line in lines:
    if line.startswith("**Name**:"):
        record["Name"] = line.split("**Name**:")[1].strip()
    elif line.startswith("**Arabic Name**:"):
        record["Arabic Name"] = line.split("**Arabic Name**:")[1].strip()
    elif line.startswith("**Home Town**:"):
        record["Home Town"] = line.split("**Home Town**:")[1].strip()
    elif line.startswith("**Home Town in Arabic**:"):
        record["Home Town in Arabic"] = line.split("**Home Town in Arabic**:")[1].strip()
    elif line.startswith("**Funeral Town**:"):
        record["Funeral Town"] = line.split("**Funeral Town**:")[1].strip()
    elif line.startswith("**Funeral Town in Arabic**:"):
        record["Funeral Town in Arabic"] = line.split("**Funeral Town in Arabic**:")[1].strip()
    elif line.startswith("**Day**:"):
        record["Day"] = line.split("**Day**:")[1].strip()
    elif line.startswith("**Hour**:"):
        record["Hour"] = line.split("**Hour**:")[1].strip()
    elif line.startswith("**Image Path**:"):
        record["Image Path"] = image_path
# Read the existing CSV file
print("Read the existing CSV file")
csv_file = "hezbollah-martyrs/hezbollah-losses-escalation.csv"
df = pd.read_csv(csv_file)
print("Append the new record")
# Append the new record
df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
# Save the updated CSV file
print("Save the updated CSV file")
df.to_csv(csv_file, index=False)
