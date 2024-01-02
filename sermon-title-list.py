import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv("API_KEY")

# Check if the API key is present
if api_key is None:
    raise ValueError("API key not found. Make sure to set it in the .env file.")

# Use the API key in your request
response = requests.get(f"https://api.elvanto.com/v1/services/getAll.json?apikey={api_key}&service_types=620ce043-7fb6-4e3f-a422-b97f577c20ff&fields[0]=series_name")
items = response.json()["services"]["service"]

sermon_titles = []

for item in items:
    # Parse the date string
    date_obj = datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S")
    
    # Extract day and month information
    day_number = date_obj.strftime("%d")
    month_short_name = date_obj.strftime("%b")
    
    # Split series name if it contains " | "
    series_parts = item["series_name"].split(" | ")
    
    # Construct the sermon title
    sermon_title = [month_short_name, day_number, series_parts[0]]
    
    # Add an additional column if there is a second part of the series name
    if len(series_parts) > 1:
        sermon_title.append(series_parts[1])
    else:
        sermon_title.append("")  # If no second part, add an empty string
    
    # Print and append to the list
    sermon_titles.append(sermon_title)

# Now, sermon_titles contains lists with day number, month short name, first part of series name, and second part of series name (if any)
cols = ['Month', 'Day', 'Passage', 'Title']
df = pd.DataFrame(data=sermon_titles, columns=cols)
print(df)

df.to_csv("./csv/sermon-titles.csv", sep=',', index=False)
