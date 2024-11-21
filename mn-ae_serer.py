from flask import Flask, request, jsonify
import subprocess
import os
import requests

app = Flask(__name__)
impact_received_value = None
power_received_value = None
coordinates_log = []
shock_log=[]
parse_gps_path = "./parse_gps.py"
judge_shock_path="./judge_shock.py"
IN_CSE_URL="http://127.0.0.1:3000"

# 임팩트 데이터를 받는 엔드포인트
@app.route('/post_impact', methods=['POST'])
def receive_impact_value():
    global impact_received_value
    data = request.get_json()
    if 'random_value' in data:
        impact_received_value = data['random_value']
        timestamp = data['timestamp']
        print(f"Received impact random value: {impact_received_value} at {timestamp}")

        impact_container=f"{IN_CSE_URL}/TinyIoT/cane1/impact"
        headers = {
            "Content-Type": "application/json",
            "X-M2M-RVI": "3",
            "X-M2M-Origin": "CAdmin"
        }
        payload = {'impact_value': impact_received_value, 'timestamp': timestamp}
            
        response = requests.post(impact_container, headers=headers, json=payload)
        if response.ok:
            print(f"Successfully sent impact data to {IN_CSE_URL}.")
        else:
            print(f"Failed to send impact data to {IN_CSE_URL}: {response.status_code}, {response.text}")

        try:
            result = subprocess.run(
                ['python', judge_shock_path, str(impact_received_value), str(timestamp)],
                capture_output=True, text=True, check=True
            )
            raw_judge_data = result.stdout.strip()
            judge_data = raw_judge_data.strip("()").split(",")
            impact_received_value, shock_flag, timestamp = int(judge_data[0]), int(judge_data[1]), judge_data[2]
            #timestamp=timestamp.lstrip()
            
            if shock_flag==1:
                shock_log.append({'shock_flag': shock_flag, 'timestamp': timestamp})
                print(f"Received shock at timestamp: {timestamp}")
            print("shocked", shock_log)
            SHOCK_container=f"{IN_CSE_URL}/TinyIoT/becane/shock"
            headers = {
                "Content-Type": "application/json",
                "X-M2M-RVI": "3",
                "X-M2M-Origin": "CAdmin"
            }
            payload = {'shock_flag': shock_flag, 'timestamp': timestamp}
            response = requests.post(SHOCK_container, headers=headers, json=payload)
            if response.ok:
                print(f"Successfully sent shock data to {IN_CSE_URL}.")
            else:
                print(f"Failed to send shock data to {IN_CSE_URL}: {response.status_code}, {response.text}")
            return jsonify({'status': 'Impact value received'}), 200
        except subprocess.CalledProcessError as e:
            print(f"Error executing judge_shock.py: {e}")
            return jsonify({'error': 'Failed to process judge'}), 500
    else:
        return jsonify({'error': 'No random_value provided'}), 400

# 임팩트 데이터를 조회하는 엔드포인트
@app.route('/get_impact', methods=['GET'])
def get_latest_impact_value():
    if impact_received_value is not None:
        return jsonify({'latest_random_value': impact_received_value}), 200
    else:
        return jsonify({'latest_random_value': 'No value received yet'}), 200

# 파워 데이터를 받는 엔드포인트
@app.route('/post_power', methods=['POST'])
def receive_power_value():
    global power_received_value
    data = request.get_json()
    if 'power_level' in data:
        power_received_value = data['power_level']
        status = "on" if power_received_value > 0 else "off"
        print(f"Received power value: {power_received_value}")
        
        battery_container=f"{IN_CSE_URL}/TinyIoT/cane1/battery"
        headers = {
            "Content-Type": "application/json",
            "X-M2M-RVI": "3",
            "X-M2M-Origin": "CAdmin"
        }
        payload = {'power_level': power_received_value, 'status': status}
            
        response = requests.post(battery_container, headers=headers, json=payload)
        if response.ok:
            print(f"Successfully sent power data to {IN_CSE_URL}.")
        else:
            print(f"Failed to send power data to {IN_CSE_URL}: {response.status_code}, {response.text}")
               
        return jsonify({'status': 'Power value received'}), 200
    else:
        return jsonify({'error': 'No power_level provided'}), 400

# 파워 데이터를 조회하는 엔드포인트
@app.route('/get_power', methods=['GET'])
def get_power_value():
    if power_received_value is not None:
        return jsonify({'received_power_value': power_received_value}), 200
    else:
        return jsonify({'received_power_value': 'No value received yet'}), 200
    

# 좌표 데이터를 받는 POST 엔드포인트
@app.route('/post_coordinates', methods=['POST'])
def receive_coordinates():
    data = request.get_json()
    if 'latitude' in data and 'longitude' in data:
        latitude = data['latitude']
        longitude = data['longitude']

        gps_container=f"{IN_CSE_URL}/TinyIoT/cane1/gps"
        headers = {
            "Content-Type": "application/json",
            "X-M2M-RVI": "3",
            "X-M2M-Origin": "CAdmin"
        }
        payload = {'latitude': latitude, 'longitude': longitude}
            
        response = requests.post(gps_container, headers=headers, json=payload)
        if response.ok:
            print(f"Successfully sent GPS data to {IN_CSE_URL}.")
        else:
            print(f"Failed to send GPS data to {IN_CSE_URL}: {response.status_code}, {response.text}")

        if len(coordinates_log)!=0:
            last_coordinate_data = coordinates_log[-1]  # 리스트의 마지막 요소 가져오기    
            # pre_latitude와 pre_longitude 값 추출
            pre_latitude = last_coordinate_data['latitude']
            pre_longitude = last_coordinate_data['longitude']
        else:
            pre_latitude = 37.551605
            pre_longitude = 127.075438

        if len(coordinates_log)>=100:
            del coordinates_log[0]

        coordinates_log.append({'latitude': latitude, 'longitude': longitude})
        print(f"Received coordinate: Latitude: {latitude}, Longitude: {longitude}")
        print(f"Received coordinate: Prelatitude: {pre_latitude}, Prelongitude: {pre_longitude}")
        # parse_gps.py에 데이터 전달 및 결과 받기
        try:
            result = subprocess.run(
                ['python', parse_gps_path, str(latitude), str(longitude), str(pre_latitude), str(pre_longitude)],
                capture_output=True, text=True, check=True
            )
            parsed_data = result.stdout.strip()  # parse_gps.py의 출력값 가져오기
            latitude, longitude, speed = map(float, parsed_data.strip("()").split(","))
            coordinates_log.append({'latitude': latitude, 'longitude': longitude, 'speed': speed})
            print(f"Received coordinate: Latitude: {latitude}, Longitude: {longitude}, speed: {parsed_data}")
            print(coordinates_log)

            gps_container_be=f"{IN_CSE_URL}/TinyIoT/becane/gps"
            headers = {
                "Content-Type": "application/json",
                "X-M2M-RVI": "3",
                "X-M2M-Origin": "CAdmin"
            }
            payload = {'latitude': latitude, 'longitude': longitude}
            
            response = requests.post(gps_container_be, headers=headers, json=payload)
            if response.ok:
                print(f"Successfully sent GPS data to {IN_CSE_URL}.")
            else:
                print(f"Failed to send GPS data to {IN_CSE_URL}: {response.status_code}, {response.text}")

            speed_container=f"{IN_CSE_URL}/TinyIoT/becane/speed"
            headers = {
                "Content-Type": "application/json",
                "X-M2M-RVI": "3",
                "X-M2M-Origin": "CAdmin"
            }
            payload = {'speed': speed}
            
            response = requests.post(speed_container, headers=headers, json=payload)
            if response.ok:
                print(f"Successfully sent speed data to {IN_CSE_URL}.")
            else:
                print(f"Failed to send speed data to {IN_CSE_URL}: {response.status_code}, {response.text}")

            return jsonify({'status': 'Coordinate received', 'parsed_data': parsed_data}), 200
        except subprocess.CalledProcessError as e:
            print(f"Error executing parse_gps.py: {e}")
            return jsonify({'error': 'Failed to process coordinates'}), 500
    else:
        return jsonify({'error': 'Invalid data format'}), 400

# 좌표 데이터를 조회하는 GET 엔드포인트
@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    return jsonify(coordinates_log), 200

if __name__ == '__main__':
    app.run(port=5000)
