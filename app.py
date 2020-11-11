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
    msg = event.message.text
    r = '很抱歉，您說什麼'

    if msg in ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了沒':
        r = '還沒，你要請我嗎?'
    elif msg == '你是誰':
        r = '我是機器人~~'
    elif msg == '誰是全世界最帥的人':
        r = '楊正裕'
    elif msg == '地址':
        r = '桃園市桃園區民生路496號8樓之一'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()