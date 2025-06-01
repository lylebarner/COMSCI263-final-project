import os
import slack_sdk
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.web import WebClient

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]  # starts with 'xapp-'

client = WebClient(token=SLACK_BOT_TOKEN)

def handle_message(event_data):
    channel = event_data.get("channel")
    user = event_data.get("user")
    text = event_data.get("text", "")
    bot_user_id = client.auth_test()["user_id"]

    # Ignore messages from the bot itself
    if user == bot_user_id:
        return
    
    # Example: auto-respond to any message containing "hello"
    if "hello" in text.lower():
        response = f"Hi <@{user}>! How can I help you today?"
        client.chat_postMessage(channel=channel, text=response)

def process_events(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        event = req.payload["event"]
        if event.get("type") == "message" and "subtype" not in event:
            handle_message(event)
        # Acknowledge the event to Slack
        client.ack(req)

if __name__ == "__main__":
    socket_client = SocketModeClient(
        app_token=SLACK_APP_TOKEN,
        web_client=client
    )
    socket_client.socket_mode_request_listeners.append(process_events)
    socket_client.connect()
    print("Slack bot is running...")
    import threading, time
    while True:
        time.sleep(10)
