import sys
import requests
import time
from datetime import datetime

def fetch_speed_log():
    try:
        response = requests.get('http://127.0.0.1:5000/get_coordinates')
        if response.status_code == 200:
            gps_log = response.json()
            return gps_log
        else:
            return []
    except Exception as e:
        print(f"Error fetching speed log: {e}")
        return []

def fetch_shock_log():
    try:
        response = requests.get('http://127.0.0.1:5000/get_impact')
        if response.status_code == 200:
            shock_log = response.json()
            return shock_log
        else:
            print(f"Failed to fetch shock log: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching shock log: {e}")
        return []

def check_ac(gps_log, shock_log):
    if shock_log and shock_log[-1].get('shock')=="is":
        if len(gps_log)<5:
            return False
        else:
            recent_gps = gps_log[-5:]
            speeds = [entry['speed'] for entry in recent_gps]
            if all(speed < 1 for speed in speeds):
                return True
    return False

def judge_shock(impact, timestamp):
    shock_threshold=80
    shock_flag="not"
    
    gps_log=fetch_speed_log()
    shock_log=fetch_shock_log()

    if check_ac(gps_log, shock_log)==True:
        shock_flag="ac"
    elif impact>=shock_threshold:
        shock_flag="is"
    return (impact, shock_flag, timestamp)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Invalid number of arguments")
        sys.exit(1)

    impact = int(sys.argv[1])
    timestamp = sys.argv[2]

    result = judge_shock(impact, timestamp)

    print(result)  