import requests
import time
from datetime import datetime

power_level = 100
timestamp = datetime.now().isoformat()

while power_level > 0:
    print(f"Sending power level: {power_level}%")
    
    response = requests.post('http://localhost:5000/post_power', json={'power_level': power_level, 'timestamp': timestamp})
    
    if response.ok:
        print("Power level sent successfully.")
    else:
        print("Failed to send power level.")
    
    power_level -= 10
    time.sleep(5)

print("Power level is depleted.")
