import requests
import random
import time
from datetime import datetime

cnt=0
while True:
    if cnt<3:
        impact_value = random.randint(1, 100)
    elif cnt==3:
        impact_value = 95
    else:
        impact_value = 0
    timestamp = datetime.now().isoformat()
    print(f"Sending impact random value: {impact_value} at {timestamp}")
    
    # POST 요청으로 임팩트 데이터를 서버로 전송
    response = requests.post('http://localhost:5000/post_impact', json={'random_value': impact_value, 'timestamp': timestamp})
    
    if response.ok:
        print("Impact value sent successfully.")
    else:
        print("Failed to send impact value.")
    cnt+=1
    # 5초마다 임팩트 데이터 전송
    time.sleep(10)
