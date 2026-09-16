import os
import requests
import pandas as pd

LTA_KEY = "3M8VhbVtSM2QSGu2tG5MwQ=="
HEADERS = {"AccountKey": LTA_KEY, "accept": "application/json"}

def fetch_traffic_speed():
    url = "https://datamall2.mytransport.sg/ltaodataservice/v4/TrafficSpeedBands"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json().get("value", [])
        df = pd.DataFrame(data)

        for col in ["StartLat", "StartLon", "EndLat", "EndLon"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    else:
        print(f"Error {response.status_code}: {response.text}")
        return pd.DataFrame()

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