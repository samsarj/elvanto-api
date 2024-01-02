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
response = requests.get(f"https://api.elvanto.com/v1/services/getAll.json?apikey={api_key}&service_types=620ce043-7fb6-4e3f-a422-b97f577c20ff&start={datetime.now().strftime("%Y-%m-%d")}&end={(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")}&fields[4]=plans")


items = []

for item in response.json()["services"]["service"][0]["plans"]["plan"][0]["items"]["item"]:
    if item["when"] == "before":
        continue

    if item["song"]:
        items.append("Song: "+ item["title"])
        print("Song:", item["title"])
        continue
    items.append(item["title"])
    print(item["title"])

print(items)

df = pd.DataFrame(data=items)
df.to_csv("./csv/plan.csv", sep=',',index=False)