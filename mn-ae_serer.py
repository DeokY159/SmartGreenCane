from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
impact_received_value = None
power_received_value = None
coordinates_log = []
shock_log=[]
parse_gps_path = "./parse_gps.py"
judge_shock_path="./judge_shock.py"


# 임팩트 데이터를 받는 엔드포인트
@app.route('/post_impact', methods=['POST'])
def receive_impact_value():
    global impact_received_value
    data = request.get_json()
    if 'random_value' in data:
        impact_received_value = data['random_value']
        timestamp = data['timestamp']
        print(f"Received impact random value: {impact_received_value} at {timestamp}")
        try:
            result = subprocess.run(
                ['python', judge_shock_path, str(impact_received_value), str(timestamp)],
                capture_output=True, text=True, check=True
            )
            raw_judge_data = result.stdout.strip()
            judge_data = raw_judge_data.strip("()").split(",")
            impact_received_value, shock_flag, timestamp = int(judge_data[0]), int(judge_data[1]), judge_data[2]
            if shock_flag==1:
                shock_log.append({'shock_flag': shock_flag, 'timestamp': timestamp})
                print(f"Received shock at timestamp: {timestamp}")
            print("shocked", shock_log)
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
        print(f"Received power value: {power_received_value}")
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
