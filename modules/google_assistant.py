import os
import grpc
import json
import logging
from google.auth.transport.grpc import secure_authorized_channel
from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc,
    query_input_pb2
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the Google Assistant config
language_code = 'en-US'
device_id = 'your-device-id'
device_model_id = 'your-device-model-id'
api_endpoint = 'embeddedassistant.googleapis.com'
grpc_deadline = 60 * 3 + 5

# Set up the Google Assistant credentials
#credentials = None
credentials = None
if os.path.isfile('credentials.json'):
    with open('credentials.json', 'r') as f:
        credentials_info = json.load(f)
        credentials = google.auth.credentials.Credentials.from_authorized_user_info(
            credentials_info,
            google.auth.transport.requests.Request()
        )

else:
    logging.error('Credentials file not found')

# Set up the Google Assistant config
config = embedded_assistant_pb2.AssistConfig(
    audio_out_config=embedded_assistant_pb2.AudioOutConfig(encoding='LINEAR16', sample_rate_hertz=16000, volume_percentage=0),
    dialog_state_in=embedded_assistant_pb2.DialogStateIn(language_code=language_code),
    device_config=embedded_assistant_pb2.DeviceConfig(device_id=device_id, device_model_id=device_model_id)
)

# Define a function to handle user input and pass it to the Google Assistant for processing
def handle_user_input(text, assistant):
    if text.startswith("ask google "):
        # Remove the "ask google" prefix and send the rest of the text to the Google Assistant
        query = text[11:]
        response_text = assistant.Assist(
            embedded_assistant_pb2.AssistRequest(
                text_query=query
            )
        ).text_response
        logging.info(response_text)

# Create a new secure authorized channel with the Google Assistant API
channel = secure_authorized_channel(credentials, api_endpoint, ssl_credentials=None)
# Create a new Google Assistant instance with the defined config
assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(channel)

# Start listening for user input and pass it to the Google Assistant for processing
while True:
    try:
        text = input("Enter text: ")
        handle_user_input(text, assistant)
    except KeyboardInterrupt:
        break
