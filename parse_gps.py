import sys
import math
import time

def haversine(latitude, longitude, pre_latitude, pre_longitude):
    R=6371.0
    # 위도와 경도를 라디안으로 변환
    phi1 = math.radians(latitude)
    phi2 = math.radians(pre_latitude)
    delta_phi = math.radians(latitude - pre_latitude)
    delta_lambda = math.radians(longitude - pre_longitude)
    # Haversine 공식
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R*c

def parse_gps(latitude, longitude, pre_latitude, pre_longitude):
    time_diff=10
    distance = haversine(latitude, longitude, pre_latitude, pre_longitude)
    speed = distance/time_diff *3600 #km/h
    return (latitude, longitude, speed)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Error: Invalid number of arguments")
        sys.exit(1)

    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])
    pre_latitude = float(sys.argv[3])
    pre_longitude = float(sys.argv[4])

    result = parse_gps(latitude, longitude, pre_latitude, pre_longitude)

    print(result)  