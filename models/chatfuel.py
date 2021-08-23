import json
import sys

import requests

class Chatfuel:
    base_url: str
    token: str
    bot_id: str

    def __init__(self, token, bot_id, chatfuel_base_url):
        self.base_url = chatfuel_base_url
        self.token = token
        self.bot_id = bot_id
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def send_chatfuel_block(self, url):
        response = requests.post(
            url=url,
            headers=self.headers,
        )

        results = json.loads(response.text)
        return results


class ChatfuelDTO:
    messenger_user_id: str
    first_name: str
    last_name: str
    genger: str
