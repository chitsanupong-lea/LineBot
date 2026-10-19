import os
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

# ดึงค่า Environment Variables
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    raise ValueError("กรุณาตั้งค่า LINE_CHANNEL_SECRET และ LINE_CHANNEL_ACCESS_TOKEN ใน Environment Variables")

handler = WebhookHandler(CHANNEL_SECRET)
config = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# สร้าง client instance นอก handler เพื่อ reuse connection
api_client = ApiClient(config)
line_bot_api = MessagingApi(api_client)

@app.route("/")
def home():
    return "LINE Webhook is running"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(
                    text="สวัสดีครับ LINE Bot ทำงานแล้ว"
                )
            ]
        )
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)