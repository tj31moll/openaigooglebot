import os
import google.cloud.dialogflow_v2 as dialogflow
#import dialogflow_v2 as dialogflow
from telegram import Bot
from google.oauth2.credentials import Credentials
from google.assistant.embedded.v1alpha2 import embedded_assistant_pb2
from google.assistant.embedded.v1alpha2 import embedded_assistant_pb2_grpc
import google.auth.transport.grpc
import google.auth.credentials

TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
DIALOGFLOW_PROJECT_ID = "YOUR_PROJECT_ID"
DIALOGFLOW_LANGUAGE_CODE = "en-US"

def detect_intent_from_text(text, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        reply = response.query_result.fulfillment_text
    except:
        reply = "Sorry, I don't understand."
    return reply

class GoogleAssistantBot:
    def __init__(self, device_model_id, device_id, language_code):
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.language_code = language_code
        self.credentials = Credentials.from_authorized_user_file('credentials.json')
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(google.auth.transport.grpc.secure_authorized_channel(self.credentials, None, 'embeddedassistant.googleapis.com'))

    def _create_assistant_request(self, text_input):
        audio_config = embedded_assistant_pb2.AudioOutConfig(encoding='LINEAR16', sample_rate_hertz=16000, volume_percentage=0)
        dialog_config = embedded_assistant_pb2.DialogStateIn(language_code=self.language_code, conversation_state=None)
        query_input = embedded_assistant_pb2.QueryInput(text=text_input)
        return embedded_assistant_pb2.AssistRequest(audio_out_config=audio_config, dialog_state_in=dialog_config, query_input=query_input)

    def _process_assistant_response(self, response):
        text_output = response.dialog_state_out.supplemental_display_text
        if response.audio_out.audio_data:
            audio_data = response.audio_out.audio_data
        return text_output

    def query(self, text_input):
        assistant_request = self._create_assistant_request(text_input)
        response = self.assistant.Assist(assistant_request)
        text_output = self._process_assistant_response(response)
        return text_output

if __name__ == '__main__':
    bot = Bot(token=TELEGRAM_TOKEN)
    assistant = GoogleAssistantBot(device_model_id='YOUR_DEVICE_MODEL_ID', device_id='YOUR_DEVICE_ID', language_code=DIALOGFLOW_LANGUAGE_CODE)

    while True:
        user_input = input('User: ')
        reply = assistant.query(user_input)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=reply)
