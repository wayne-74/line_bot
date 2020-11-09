from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('zrSOi6P42cHjQcjwaUS/oQFB8WtRZVi1EVs65WOG5+K25XiphGWSWGE9iEZ6hIyMnmX3nmAvOmCYZsY+XH/TQhFKOwt+A+6WrjwleLVXvwG2L38JOYAM94DTrz5V6h4aJG0fXiX8lErfGA09lj1sKwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f2cf95f9639f32f6c73cf41ed22b158a')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()