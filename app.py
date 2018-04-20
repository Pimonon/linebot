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
import oil_price

line_bot_api = LineBotApi('pm6p/yGQjd0IYTvNC0aO4fDsIIwVJb4IPhwVAirn93xHlOiPte+OQ946eotXFZwKiTIqFiflqomCTAStOuhFNMgFv4N27ZuEm97sdjUzXEulb8vKmmGu5AR+GXaJIXsQ/O+QLxkW+i8CyvcpD6yo4AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e75dea7b89d456da3305287879331d0e')

@app.route("/", methods=['GET'])
def default_action():
    return 'Hi'

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
        abort(400)

    return 'OK'




 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'ราคาน้ำมัน':
        l = oil_price.get_prices()
        s = ""
        for p in l:
            s += "%s %.2f บาท\n"%(p[0],p[1])

        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=s))
    else:
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=event.message.text+'เปลียนจากค่ะ เป็นจ้า'))
    

if __name__ == "__main__":
    app.run()