import requests
import random
import time

while True:
    random_value = random.randint(1, 100)
    print(f"Sending impact random value: {random_value}")
    
    # POST 요청으로 임팩트 데이터를 서버로 전송
    response = requests.post('http://localhost:5000/post_impact', json={'random_value': random_value})
    
    if response.ok:
        print("Impact value sent successfully.")
    else:
        print("Failed to send impact value.")
    
    # 10초마다 임팩트 데이터 전송
    time.sleep(10)
