import slack_sdk
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse

slack_client = WebClient(token="<your_bot_token>")

@slack_client.event("message")
def handle_message(event_data):
    channel = event_data["channel"]
    message = event_data["text"]
    
    # Check if the message requires an automated response
    if message == "Hello":
        response = "Hi there!"
        slack_client.chat_postMessage(channel=channel, text=response)

slack_client.start()