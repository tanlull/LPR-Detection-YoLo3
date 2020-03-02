import requests
 
url = "https://api.aiforthai.in.th/lpr-v2"
payload = {'crop': '1', 'rotate': '1'}
files = {'image':open('C:/Users/tan/git/LPR-Detection-YoLo3/output/20200302/20200302155427_detect.jpeg', 'rb')}
 
headers = {
    'Apikey': "buZ5tUWbWGNK35jLesFoFwkZ3Cn5gvbB",
    }
 
response = requests.post( url, files=files, data = payload, headers=headers)
 
print(response.json())