import os
import grpc
from google.auth.transport.grpc import secure_authorized_channel
from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the Google Assistant config
language_code = 'en-US'
device_id = 'your-device-id'
device_model_id = 'your-device-model-id'
api_endpoint = 'embeddedassistant.googleapis.com'
grpc_deadline = 60 * 3 + 5

# Set up the Google Assistant credentials
credentials = None
if os.path.isfile('credentials.json'):
    with open('credentials.json', 'r') as f:
        credentials = google.auth.credentials.Credentials.from_authorized_user_info(
            google.auth.transport.requests.Request(), 
            json.load(f)
        )
else:
    logging.error('Credentials file not found')

# Set up the Google Assistant config
#config = embedded_assistant_pb2.AssistConfig(
#    audio_out_config=embedded_assistant_pb2.AudioOutConfig(),
#    dialog_state_in=embedded_assistant_pb2.DialogStateIn(
#        language_code='en-US'
#    ),
#    device_config=embedded_assistant_pb2.DeviceConfig(),
#    text_query_config=embedded_assistant_pb2.QueryConfig(
#        language_code='en-US'
#    )
#)


# Set up the Google Assistant config
config = embedded_assistant_pb2.AssistConfig(
    audio_out_config=embedded_assistant_pb2.AudioOutConfig(encoding='LINEAR16', sample_rate_hertz=16000, volume_percentage=0),
    dialog_state_in=embedded_assistant_pb2.DialogStateIn(language_code='en-US'),
    device_config=embedded_assistant_pb2.DeviceConfig(device_id=device_id, device_model_id=device_model_id),
    text_query_config=embedded_assistant_pb2.QueryInput(
        text=embedded_assistant_pb2.TextInput(
            text=text_query, language_code='en-US'
        )
    )
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
channel = secure_authorized_channel(credentials, config)

# Create a new Google Assistant instance with the defined config
assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(channel)

# Start listening for user input and pass it to the Google Assistant for processing
while True:
    try:
        text = input("Enter text: ")
        handle_user_input(text, assistant)
    except KeyboardInterrupt:
        break
