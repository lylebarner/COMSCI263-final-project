import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize a Bolt for Python app
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Add functionality here
@app.event("message")
def message_handler(message, say):
    # Filter out messages from the bot itself
    if message.get("subtype") is None or message.get("subtype") != "bot_message":
        text = message.get("text", "")
        if "hello" in text.lower():
            channel_id = message["channel"]
            say(channel="channel_id", text="Hello! How can I help you?")

# Start the app
if __name__ == "__main__":
    SocketModeHandler(app=app, app_token=os.getenv("SLACK_APP_TOKEN")).start()