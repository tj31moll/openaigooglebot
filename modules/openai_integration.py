import openai
import os

# Set up OpenAI API credentials
openai.api_key = "YOUR_API_KEY"

# Define a function to generate a chatbot response using the OpenAI API
def get_chatbot_response(text):
    # Generate a response from the OpenAI API
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the response text from the API response
    response_text = response.choices[0].text.strip()

    return response_text
