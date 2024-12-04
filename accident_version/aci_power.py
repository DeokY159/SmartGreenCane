import requests
import time
from datetime import datetime
import subprocess

impact_process = subprocess.Popen(['python', './aci_impact.py'])
gps_process = subprocess.Popen(['python', './aci_gps.py'])

power_level = 102.5
timestamp = datetime.now().isoformat()

while power_level > 0:
    power_level -= 2.5 #2.43
    print(f"Sending power level: {power_level:.2f}%")
    
    response = requests.post('http://localhost:5000/post_power', json={'power_level': power_level, 'timestamp': timestamp})
    
    if response.ok:
        print("Power level sent successfully.")
    else:
        print("Failed to send power level.")

    time.sleep(1)

print("Power level is depleted.")

impact_process.terminate()
gps_process.terminate()

# 프로세스 종료를 기다림
impact_process.wait()
gps_process.wait()