import os
import slack_sdk
from slack_sdk.rtm_v2 import RTMClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

slack_token = os.getenv("SLACK_BOT_TOKEN")
rtm_client = RTMClient(token=slack_token)

@rtm_client.on("message")
def handle_message(event):
    channel_id = event.get("channel")
    user_id = event.get("user")
    
    # Ignore messages from the bot itself
    if user_id == os.getenv("SLACK_BOT_USER_ID"):
        return

    text = event.get("text")
    
    if "hello" in text.lower():
        try:
            response = rtm_client.web_client.chat_postMessage(
                channel=channel_id,
                text="Hello there! How can I assist you today?"
            )
        except SlackApiError as e:
            print(f"Error posting message: {e.response['error']}")

if __name__ == "__main__":
    rtm_client.start()