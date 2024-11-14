from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/help', methods=['POST'])
def receive_gps():
    try:
        gps_data = request.data.decode('utf-8')
        print(f"Received GPS Data: {gps_data}")

        parsed_data = parse_gps_data(gps_data)
        if parsed_data:
            print(f"Parsed Data: {parsed_data}")

            server_url = "https://127.0.0.1" #mobius 주소
            send_to_server(parsed_data, server_url)

            return jsonify({"status": "success", "data": parsed_data}), 200
        else:
            return jsonify({"status": "fail", "message": "Invalid GPS data"}), 400
    except Exception as e:
        print(f"Error processing GPS data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


#"$GPGGA,114455.532,3735.0079,N,12701.6446,E,1,03,7.9,48.8,M,19.6,M,0.0,0000*48"

def parse_gps_data(data):
    try:
        main_data, checksum = data.strip('$').split('*')
        fields = main_data.split(',')

        parsed_data = {
            "message_id": fields[0],       # GPGGA
            "utc_time": fields[1],        # UTC 시간
            "latitude": fields[2],        # 위도
            "latitude_dir": fields[3],    # 위도 방향 (N/S)
            "longitude": fields[4],       # 경도
            "longitude_dir": fields[5],   # 경도 방향 (E/W)
            "gps_quality": fields[6],     # GPS 품질 (0=유효하지 않음, 1=GPS 고정 등)
            "num_satellites": fields[7],  # 사용 가능한 위성 수
            "hdop": fields[8],            # 수평 정밀도 (HDOP)
            "altitude": fields[9],        # 고도 (미터)
            "altitude_unit": fields[10],  # 고도 단위 (M)
            "geoid_height": fields[11],   # 지오이드 높이
            "geoid_unit": fields[12],     # 지오이드 단위 (M)
            "dgps_data_age": fields[13],  # DGPS 데이터 연령
            "dgps_station_id": fields[14],# DGPS 스테이션 ID
            "checksum": checksum          # 체크섬
        }
        return parsed_data
    except Exception as e:
        print(f"Error parsing GPS data: {e}")
        return None

def send_to_server(parsed_data, server_url):

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(server_url, data=json.dumps(parsed_data), headers=headers)
        
        if response.status_code == 200:
            print("Data sent")
        else:
            print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending data to server: {e}")