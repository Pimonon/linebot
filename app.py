from flask import Flask, request, abort

import tempfile
import os
import sys

from feature.CarAnalytics import LicencePlate

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage,
   ImageMessage, VideoMessage, AudioMessage,
   StickerMessage,StickerSendMessage, JoinEvent, SourceGroup
)

import oil_price

app = Flask(__name__)

latest_image_path = ""
#pimonon
#line_bot_api = LineBotApi('pm6p/yGQjd0IYTvNC0aO4fDsIIwVJb4IPhwVAirn93xHlOiPte+OQ946eotXFZwKiTIqFiflqomCTAStOuhFNMgFv4N27ZuEm97sdjUzXEulb8vKmmGu5AR+GXaJIXsQ/O+QLxkW+i8CyvcpD6yo4AdB04t89/1O/w1cDnyilFU=')
#handler = WebhookHandler('e75dea7b89d456da3305287879331d0e')

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
   print('Specify LINE_CHANNEL_SECRET as environment variable.')
   sys.exit(1)
if channel_access_token is None:
   print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
   sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#hippopo
line_bot_api = LineBotApi('B9J4tYqzVR6NERpWMjzIP5bZ9SNSJESwzeFUi5zDTGsqqdz7lgjuGNyeA383nu3AtEJoRYULmtwVeOKSqv3pDZEtRlA5eUjP5HvhBXydWYYtz2XsYbaDyAALD/+aMniR1UZWWTqmx9vFFJKQL6PHdQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0cb6b5c6311053662e07b9538a896be8')

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/", methods=['GET'])
def default_action():
    l = oil_price.get_prices()
    s = ""
    for p in l:
        s += "%s %f บาท\n"%(p[0],p[1])
    return s

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



@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
   # Handle webhook verification
   if event.reply_token == '00000000000000000000000000000000':
       return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
   # group_id = event.source.group_id
   # line_bot_api.get_group_member_profile(group_id,member_id)
   # member_ids_res = line_bot_api.get_group_member_ids(group_id)
   # print(member_ids_res.member_ids)
   # print(member_ids_res.next)

   try:
       profile = line_bot_api.get_group_member_profile(
           event.source.group_id,'U89b516d04f46a34859942624d4a57a79'
       )
       line_bot_api.reply_message(
           event.reply_token,
           [
               TextSendMessage(text='ดีดี'),
               StickerSendMessage(
                   package_id=1,
                   sticker_id=2
               )
           ]
       )        
   except LineBotApiError as e:
       print(e.status_code)
       print(e.error.message)
       print(e.error.details)
       line_bot_api.reply_message(
           event.reply_token,
           [
               TextSendMessage(text='หัวหน้าไม่อยู่ในห้องนี้\nไปละค่ะ\nบัย'),
           ]
       )
       line_bot_api.leave_group(event.source.group_id)
   
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global latest_image_path

    if event.reply_token == 'ffffffffffffffffffffffffffffffff':
       return 'OK'

    if event.message.text == 'ไปเหอะ':
       if isinstance(event.source,SourceGroup):
           if event.source.user_id == 'U89b516d04f46a34859942624d4a57a79':
               line_bot_api.reply_message(
                   event.reply_token,
                   TextMessage(text='บะบายค่า')
               )
               line_bot_api.leave_group(event.source.group_id)
           else:
               line_bot_api.reply_message(
                   event.reply_token,
                   TextMessage(text='ไม่')
               )
    
    elif event.message.text == 'profile':
       user_id = event.source.user_id
       profile = line_bot_api.get_profile(user_id)
       # image_message = ImageSendMessage(
       #             original_content_url=profile.picture_url,
       #             preview_image_url=profile.picture_url
       #         )

       line_bot_api.reply_message(
           event.reply_token,
           [
               TextSendMessage(text=profile.display_name),
               TextSendMessage(text=profile.user_id),
               TextSendMessage(text=profile.picture_url),
               TextSendMessage(text=profile.status_message),
               # image_message
           ]
       )
    
    if event.message.text == 'ราคาน้ำมัน':
        l = oil_price.get_prices()
        s = ""
        for p in l:
            s += "%s %.2f บาท\n"%(p[0],p[1])

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=s))
    elif event.message.text == 'วิเคราะห์รูป':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='สักครู่ค่ะ')
            ])

        # Process image
        try:
            lp = LicencePlate()
            result = lp.process(latest_image_path)
            s = lp.translate(result)

            line_bot_api.push_message(
                event.source.user_id, [
                    TextSendMessage(text=s)
                ])
        except Exception as e:
            print('Exception:',type(e),e)
            line_bot_api.push_message(
                event.source.user_id, [
                    TextSendMessage(text='ไม่สามารถวิเคราะห์รูปได้นะคะ')
                ])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text+'จ้า'))

@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    global latest_image_path

    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    # Save image path
    latest_image_path = dist_path
    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='เก็บรูปให้แล้วค่ะ')
        ])




if __name__ == "__main__":
    app.run()