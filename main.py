"""
Author: Moiz Lakdawala
"""
import os
import json
import datetime
from configparser import ConfigParser

import requests


class OktaLogger:
    """A class for logging Okta events"""
    
    def __init__(self):
        """Initializes OktaLogger with configuration, headers, and URL"""
        # Load Configuration
        self.config = ConfigParser()
        self.config.read('./key.cfg')
        
        # Set API Key, URL, and file from configuration
        self.api_key = self.config.get('SSWS_Key', 'key')
        self.thirty_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
        self.url = f"https://<okta domain>/api/v1/logs?since={self.thirty_time.isoformat()}"
        self.file = self.config.get('Log_file', 'file')
        
        # Set headers for request
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        
    def get_logs(self):
        """
        Gets logs from Okta.
        
        Returns:
            list: A list of logs obtained from Okta.
        
        Raises:
            HTTPError: If the GET request fails.
        """
        # Perform GET request to obtain logs
        response = requests.get(self.url, headers=self.headers)
        
        # Check response status code
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            response.raise_for_status()
            
    def write_logs(self, logs):
        """
        Writes the obtained logs to a file.
        
        Args:
            logs (list): A list of logs to write to the file.
        """
        # Remove existing log file if it exists
        if os.path.isfile(self.file):
            os.remove(self.file)
        
        # Open file and write logs to it
        with open(self.file, 'w', encoding='utf-8') as log_file:
            for log in logs:
                log['Log_type'] = 'Okta'
                json.dump(log, log_file, ensure_ascii=False)
                log_file.write('\n')

    def execute(self):
        """Executes the log fetching and writing process."""
        # Get logs and write them to a file
        logs = self.get_logs()
        self.write_logs(logs)


if __name__ == "__main__":
    # Create OktaLogger instance and execute it
    logger = OktaLogger()
    logger.execute()
