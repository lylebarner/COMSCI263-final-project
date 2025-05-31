import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize your app with your bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listen to messages in channels
@app.message("")
def handle_message(message, say):
    user = message.get('user')
    text = message.get('text')
    channel = message.get('channel')
    # Example automated response
    response = f"Hi <@{user}>, you said: {text}"
    say(response)

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()