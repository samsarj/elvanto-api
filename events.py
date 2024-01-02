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
response = requests.get(f"https://api.elvanto.com/v1/calendar/events/getAll.json?apikey={api_key}&start={datetime.now().strftime("%Y-%m-%d")}&end={(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")}")
items = response.json()["events"]["event"]

event_titles_and_times = []

last_month = None

for item in items:
    # Parse the date string
    date_obj = datetime.strptime(item["start_date"], "%Y-%m-%d %H:%M:%S")
    
    # Extract day and month information
    day_number = date_obj.strftime("%d")
    month_short_name = date_obj.strftime("%b")
    
    # Format event start time as "7pm" or "8:45am"
    event_start_time = date_obj.strftime("%I:%M%p").lower().lstrip('0').replace(':00', '')
    
    # Skip 'Sunday Service' and 'Equip'
    if item["name"] in ['Sunday Service', 'Equip']:
        continue
    
    # Construct the event title and time
    event_title_and_time = [month_short_name, day_number, item["name"], event_start_time]
    
    # Only append if it's the first instance of the month or a new month
    if last_month is None or month_short_name != last_month:
        event_titles_and_times.append(event_title_and_time)
        last_month = month_short_name
    else:
        event_titles_and_times.append(['', day_number, item["name"], event_start_time])

# Now, event_titles_and_times contains lists with month, day, event title, and event start time
cols = ['Month', 'Day', 'Event Title', 'Event Start Time']
df_events = pd.DataFrame(data=event_titles_and_times, columns=cols)

print(df_events)

df_events.to_csv("./csv/events.csv", sep=',', index=False)
