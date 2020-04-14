import requests
 
url = "https://api.aiforthai.in.th/lpr-v2"
payload = {'crop': '1', 'rotate': '1'}
#filename='/Volumes/USB256/git/LPR-Detection-YoLo3/output/20200320/20200320134633_crop.jpeg'
filename='C:/Users/tan/git/LPR-Detection-YoLo3/output/20200303/20200303122201_crop.jpeg'

files = {'image':open(filename, 'rb')}
 
headers = {
    'Apikey': "buZ5tUWbWGNK35jLesFoFwkZ3Cn5gvbB",
    }
 
response = requests.post( url, files=files, data = payload, headers=headers)
 
print(str(response.json()))

#Error : UnicodeEncodeError: 'ascii' codec can't encode characters in position --> use this
#print(str(response.json()).encode('utf-8'))