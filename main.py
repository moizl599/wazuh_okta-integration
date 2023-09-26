import os
import json
import datetime
from configparser import ConfigParser

import requests


class OktaLogger:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('./key.cfg')
        self.api_key = self.config.get('SSWS_Key', 'key')
        self.thirty_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
        self.url = f"https://<okta domain>/api/v1/logs?since={self.thirty_time.isoformat()}"
        self.file = self.config.get('Log_file', 'file')
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }

    def get_logs(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            response.raise_for_status()

    def write_logs(self, logs):
        if os.path.isfile(self.file):
            os.remove(self.file)

        with open(self.file, 'w', encoding='utf-8') as log_file:
            for log in logs:
                log['Log_type'] = 'Okta'
                json.dump(log, log_file, ensure_ascii=False)
                log_file.write('\n')

    def execute(self):
        logs = self.get_logs()
        self.write_logs(logs)


if __name__ == "__main__":
    logger = OktaLogger()
    logger.execute()
