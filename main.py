import requests
import json
import datetime
import os
from configparser import ConfigParser

config = ConfigParser()
config.read('./key.cfg')
API_KEY = config.get('SSWS_Key', 'key')
thirty_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
url = f"https://okta.workjam.com/api/v1/logs?since={thirty_time.isoformat()}"
file = config.get('Log_file', 'file')
payload = {}
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': API_KEY
}
print(headers)
response = requests.request("GET", url, headers=headers, data=payload)
raw_log_list = json.loads(response.text)
if os.path.isfile(file):
    os.remove(file)
with open(file, 'x', encoding='utf-8') as f:
    for log in raw_log_list:
        print (log['displayMessage'])
        with open(file, 'a', encoding='utf-8') as Log_file:
            log['Log_type'] = 'Okta'
            json.dump(log, Log_file, ensure_ascii=False)
            Log_file.write('\n')
