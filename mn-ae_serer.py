from flask import Flask, request, jsonify

app = Flask(__name__)
impact_received_value = None
power_received_value = None

# 임팩트 데이터를 받는 엔드포인트
@app.route('/post_impact', methods=['POST'])
def receive_impact_value():
    global impact_received_value
    data = request.get_json()
    if 'random_value' in data:
        impact_received_value = data['random_value']
        print(f"Received impact random value: {impact_received_value}")
        return jsonify({'status': 'Impact value received'}), 200
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

if __name__ == '__main__':
    app.run(port=5000)
