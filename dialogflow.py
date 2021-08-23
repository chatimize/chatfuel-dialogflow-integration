import dialogflow_v2 as dialogflow
import requests
from flask import Flask, request
from google.protobuf import json_format

class DialogFlow:
    def __init__(self, project_id: str = '', service_account_json: str = None):
        self.project_id = project_id
        self.service_account_json = service_account_json

    def detect_intent(self, session_id, texts, language_code):
        if self.service_account_json:
            session_client = dialogflow.SessionsClient.from_service_account_json(self.service_account_json)

        else:
            session_client = dialogflow.SessionsClient()

        session = session_client.session_path(self.project_id, session_id)

        for text in texts:
            text_input = dialogflow.types.TextInput(
                text=text,
                language_code=language_code
            )

            query_input = dialogflow.types.QueryInput(
                text=text_input
            )

            response = session_client.detect_intent(
                session=session,
                query_input=query_input
            )

            return response

