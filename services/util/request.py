import requests


class RequestUtilService:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://discord.com/api/v9"
        self.headers = {
            "authorization": 'Bot ' + token,
            "content-type": "application/json"
        }

    def make_post(self, data, endpoint_url) -> dict:
        url = self.base_url + endpoint_url
        return requests.post(url, headers=self.headers, json=data).json()
    
    def make_get(self, endpoint_url) -> dict:
        url = self.base_url + endpoint_url
        return requests.get(url, headers=self.headers).json()
