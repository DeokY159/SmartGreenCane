import requests

IN_CSE_URL= "http://127.0.0.1:3000"
url = f"{IN_CSE_URL}/TinyIoT"

payload = "{\n    \"m2m:ae\": {\n        \"rn\": \"cane1\",\n        \"api\": \"Nmyapp3\",\n        \"lbl\": [\n            \"key1\",\n            \"key2\"\n        ],\n        \"srv\": [\n            \"3\"\n        ],\n        \"rr\": true\n    }\n}\n\n"
headers = {
  'Accept': 'application/vnd.onem2m-res+json;ty=2',
  'X-M2M-RI': 'create_ae',
  'X-M2M-origin': 'CAdmin1',
  'Content-Type': 'application/json;ty=2',
  'X-M2M-RVI': '2a'
}
response = requests.request("POST", url, headers=headers, data=payload)

payload = "{\n    \"m2m:ae\": {\n        \"rn\": \"becane\",\n        \"api\": \"Nmyapp3\",\n        \"lbl\": [\n            \"key1\",\n            \"key2\"\n        ],\n        \"srv\": [\n            \"3\"\n        ],\n        \"rr\": true\n    }\n}\n\n"
headers = {
  'Accept': 'application/vnd.onem2m-res+json;ty=2',
  'X-M2M-RI': 'create_ae',
  'X-M2M-origin': 'CAdmin2',
  'Content-Type': 'application/json;ty=2',
  'X-M2M-RVI': '2a'
}
response = requests.request("POST", url, headers=headers, data=payload)

url = f"{IN_CSE_URL}/TinyIoT/cane1"

payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"gps\",\n    \"lbl\": [\"key1\", \"key2\"],\n    \"mbs\": 16384\n  }\n}"
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': 'create_cnt',
  'X-M2M-Origin': 'CAdmin',
  'Content-Type': 'application/json;ty=3',
  'X-M2M-RVI': '3'
}
response = requests.request("POST", url, headers=headers, data=payload)

payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"impact\",\n    \"lbl\": [\"key1\", \"key2\"],\n    \"mbs\": 16384\n  }\n}"
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': 'create_cnt',
  'X-M2M-Origin': 'CAdmin',
  'Content-Type': 'application/json;ty=3',
  'X-M2M-RVI': '3'
}
response = requests.request("POST", url, headers=headers, data=payload)

payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"battery\",\n    \"lbl\": [\"key1\", \"key2\"],\n    \"mbs\": 16384\n  }\n}"
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': 'create_cnt',
  'X-M2M-Origin': 'CAdmin',
  'Content-Type': 'application/json;ty=3',
  'X-M2M-RVI': '3'
}
response = requests.request("POST", url, headers=headers, data=payload)

payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"sound\",\n    \"lbl\": [\"key1\", \"key2\"],\n    \"mbs\": 16384\n  }\n}"
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': 'create_cnt',
  'X-M2M-Origin': 'CAdmin',
  'Content-Type': 'application/json;ty=3',
  'X-M2M-RVI': '3'
}
response = requests.request("POST", url, headers=headers, data=payload)

url = f"{IN_CSE_URL}/TinyIoT/becane"

payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"gps\",\n    \"lbl\": [\"key1\", \"key2\"],\n    \"mbs\": 16384\n  }\n}"
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': 'create_cnt',
  'X-M2M-Origin': 'CAdmin',
  'Content-Type': 'application/json;ty=3',
  'X-M2M-RVI': '3'
}
response = requests.request("POST", url, headers=headers, data=payload)

payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"speed\",\n    \"lbl\": [\"key1\", \"key2\"],\n    \"mbs\": 16384\n  }\n}"
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': 'create_cnt',
  'X-M2M-Origin': 'CAdmin',
  'Content-Type': 'application/json;ty=3',
  'X-M2M-RVI': '3'
}
response = requests.request("POST", url, headers=headers, data=payload)

payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"shock\",\n    \"lbl\": [\"key1\", \"key2\"],\n    \"mbs\": 16384\n  }\n}"
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': 'create_cnt',
  'X-M2M-Origin': 'CAdmin',
  'Content-Type': 'application/json;ty=3',
  'X-M2M-RVI': '3'
}
response = requests.request("POST", url, headers=headers, data=payload)

payload = "{\n  \"m2m:cnt\": {\n    \"rn\": \"onoff\",\n    \"lbl\": [\"key1\", \"key2\"],\n    \"mbs\": 16384\n  }\n}"
headers = {
  'Accept': 'application/json',
  'X-M2M-RI': 'create_cnt',
  'X-M2M-Origin': 'CAdmin',
  'Content-Type': 'application/json;ty=3',
  'X-M2M-RVI': '3'
}
response = requests.request("POST", url, headers=headers, data=payload)
