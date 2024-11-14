import requests
import time

# Function to generate a path from start to end point using OSRM API
def generate_path(start_coords, end_coords):
    try:
        base_url = "http://router.project-osrm.org/route/v1/walking/"
        coordinates = f"{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}"
        url = f"{base_url}{coordinates}?overview=full&geometries=geojson"
        response = requests.get(url)
        if response.status_code != 200:
            print("No directions found for walking.")
            return []
        data = response.json()
        route = data['routes'][0]['geometry']['coordinates']
        path_coords = [(coord[1], coord[0]) for coord in route]
        return path_coords
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to supply coordinates at regular intervals and send to server
def supply_coords(coords, interval=10):
    for coord in coords:
        print(f"Sending coordinate: Latitude: {coord[0]}, Longitude: {coord[1]}")
        
        # 서버로 좌표 전송
        response = requests.post('http://localhost:5000/post_coordinates', json={'latitude': coord[0], 'longitude': coord[1]})
        
        if response.ok:
            print("Coordinate sent successfully.")
        else:
            print("Failed to send coordinate.")
        
        time.sleep(interval)

# Define starting point (Sejong University main gate)
start_lat, start_lng = 37.5514, 127.0752
start_coords = (start_lat, start_lng)

# Define destination coordinates (for example, let's use another landmark's coordinates)
end_lat, end_lng = 37.5665, 126.9780  # Seoul City Hall as an example
end_coords = (end_lat, end_lng)

# Generate path from Sejong University to Seoul City Hall
path_to_city_hall = generate_path(start_coords, end_coords)

# Generate path from Seoul City Hall back to Sejong University
path_back_to_sejong = generate_path(end_coords, start_coords)

# Combine the paths to create a round trip
full_path_coords = path_to_city_hall + path_back_to_sejong

# Supply coordinates at regular intervals
if full_path_coords:
    supply_coords(full_path_coords, interval=10)
