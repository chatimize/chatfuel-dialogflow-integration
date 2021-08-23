'''
    This code is a bridge between Chatfuel and Dialogflow.
    You can use it to handle the text input that Chatfuel does not understand with Dialogflow.
'''

import json
import sys
import dialogflow_v2 as dialogflow
import requests
from flask import Flask, request
from google.protobuf import json_format

from models.chatfuel import Chatfuel
from models.dialogflow import DialogFlow
from models.dto import FromChatfuelDTO


# FILL IN THE RIGHT VALUES FOR THE VARIABLES BELOW
CHATFUEL_API_KEY = "YOUR_CHATFUEL_API_KEY"
CHATFUEL_BOT_ID = "YOUR_CHATFUEL_BOT_ID"
DIALOGFLOW_PROJECT_ID = "YOUR_DIALOGFLOW_PROJECT_ID"

CHATFUEL_BASE_URL = "https://api.chatfuel.com/bots/"
CHATFUEL_USERID_REQUEST_KEY = "messenger_user_id"
CHATFUEL_LANGUAGE_REQUEST_KEY = "language_code"
CHATFUEL_INPUT_REQUEST_KEY = "last_input"

app = Flask(__name__)

@app.route('/', methods=['POST'])
def send_to_dialogflow():
    if request.method == 'POST':
        print('Request received.', file=sys.stderr)
        data = request.get_json()
        custom_fields = {}

        dto = FromChatfuelDTO(data[CHATFUEL_USERID_REQUEST_KEY], data[CHATFUEL_LANGUAGE_REQUEST_KEY],
                              data[CHATFUEL_INPUT_REQUEST_KEY])

        dialogflow = DialogFlow(project_id=DIALOGFLOW_PROJECT_ID, service_account_json='./config.json')

        chatfuel = Chatfuel(token=CHATFUEL_API_KEY, bot_id=CHATFUEL_BOT_ID, chatfuel_base_url=CHATFUEL_BASE_URL)

        dialogflow_response = dialogflow.detect_intent(session_id=dto.user_id,
                                                       texts=[dto.input_text],
                                                       language_code=dto.language_code)

        dialogflow_response_dict = json_format.MessageToDict(dialogflow_response)
        if dialogflow_response_dict['queryResult']['parameters']:
            for key, value in dialogflow_response_dict['queryResult']['parameters'].items():
                val = dialogflow_response_dict['queryResult']['parameters'][key]
                k = str(key)
                if val and val != '':
                    custom_fields[k] = val

        for message in dialogflow_response.query_result.fulfillment_messages:
            if len(message.payload.fields.items()) > 0:
                for key, value in message.payload.fields.items():
                    if key == 'block':
                        url = generate_chatfuel_url(CHATFUEL_BOT_ID, dto.user_id, CHATFUEL_API_KEY, value, "", custom_fields)
                        chatfuel.send_chatfuel_block(url)

        response = {
            'version': 'v2',
            'content': {
                'messages': ["Succeeded"]
            }
        }
        return response


def generate_chatfuel_url(bot_id, user_id, chatfuel_token, chatfuel_blockname, chatfuel_messagetag, custom_fields):
    url = CHATFUEL_BASE_URL
    url += bot_id
    url += "/users/"
    url += user_id
    url += "/send?chatfuel_token="
    url += chatfuel_token

    if chatfuel_messagetag:
        print("message tag")

    url += "&chatfuel_block_id="
    url += chatfuel_blockname.string_value

    for k in custom_fields:
        v = custom_fields[k]
        print('k', k, file=sys.stderr)
        print('v', v, file=sys.stderr)
        url += '&%s=%s' % (k, v)

    return url

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
