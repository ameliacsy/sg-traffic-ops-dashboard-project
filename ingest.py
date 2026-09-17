import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

LTA_KEY = os.getenv("LTA_API_KEY")
HEADERS = {"AccountKey": LTA_KEY, "accept": "application/json"}

def fetch_traffic_speed():
    url = "https://datamall2.mytransport.sg/ltaodataservice/v4/TrafficSpeedBands"
    all_data = []
    skip = 0

    while True:
        paginated_url = f"{url}?$skip={skip}"
        response = requests.get(paginated_url, headers=HEADERS)

        if response.status_code == 200:
            batch = response.json().get("value", [])
            if not batch:
                break
            all_data.extend(batch)
            skip += 500
        else:
            print(f"Error {response.status_code}: {response.text}")
            break
            
    df = pd.DataFrame(all_data)

    for col in ["StartLat", "StartLon", "EndLat", "EndLon"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df
         

def fetch_incidents():
    url = "https://datamall2.mytransport.sg/ltaodataservice/TrafficIncidents"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json().get("value", [])
        return pd.DataFrame(data)
    return pd.DataFrame()

if __name__ == "__main__":
    speed_df = fetch_traffic_speed()
    incidents_df = fetch_incidents()
    print(f"Fetched {len(speed_df)} speed segments and {len(incidents_df)} incidents.")