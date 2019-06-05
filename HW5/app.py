from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, CarouselContainer, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    FlexSendMessage, ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent
)
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))


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

@handler.add(PostbackEvent)
def handle_postback(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    data = event.postback.data
    if data == '開立投信帳戶(1-4項)':
        buttons_template = ButtonsTemplate(
            title='野村開立投信帳戶表單。', text='親愛的投資朋友，您好：開立投信帳戶將包含以下1-4的表單。',
            actions=[
                PostbackAction(label='表一, 開戶申請書', data='開戶申請書'),
                PostbackAction(label='表二, 投資人風險屬性評估表', data='投資人風險屬性評估表'),
                PostbackAction(label='表三, 自我證明表', data='自我證明表'),
                PostbackAction(label='表四, 個人資料相關告知事項', data='蒐集、處理及利用個人資料告知事項'),
            ])
        template_message = TemplateSendMessage(
            alt_text='野村投信您好！這是我們野村開立投信帳戶表單。', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)
    elif data == '開立投信帳戶(5-6項)':
        buttons_template = ButtonsTemplate(
            title='野村開立投信帳戶表單。', text='親愛的投資朋友，您好：開立投信帳戶將包含以下5-6的表單。',
            actions=[
                PostbackAction(label='表五, 投信身分證明文件聲明書', data='野村投信身分證明文件聲明書'),
                PostbackAction(label='表六, 投信基金扣款轉帳授權書', data='投信基金扣款轉帳授權書'),
            ])
        template_message = TemplateSendMessage(
            alt_text='野村投信您好！這是我們野村開立投信帳戶表單。', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)
    elif data == '開立投信+境外帳戶':
        buttons_template = ButtonsTemplate(
            title='野村開立投信帳戶+境外帳戶。', text='親愛的投資朋友，您好：請先確認您已填寫開立投信帳戶表單, 再進行以下流程:', 
            actions=[
                PostbackAction(label='我尚未填寫野村開立投信帳戶表單', data='開立投信帳戶(1-4項)'),
                # PostbackAction(label='我尚未填寫野村開立投信帳戶表單(5-6)', data='開立投信帳戶(5-6項)'),
                PostbackAction(label='我已填寫野村開立投信帳戶表單', data='境外帳戶')
            ])
        template_message = TemplateSendMessage(
            alt_text='野村投信您好！我們將進行境外帳戶的流程。', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)
    elif data == '境外帳戶':
        buttons_template = ButtonsTemplate(
            title='野村開立境外帳戶。', text='親愛的投資朋友，您好：開立野村境外帳戶需填寫以下表單。', 
            actions=[
                PostbackAction(label='表七, 境外基金帳授權書(外幣)', 
                                data='境外基金授權書(外幣)'),
                PostbackAction(label='表八, 境外基金授權書(台幣)', 
                                data='境外基金授權書(台幣)')
            ])
        template_message = TemplateSendMessage(
            alt_text='野村投信您好！這是我們野村開立境外帳戶表單。', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)
    elif data == '舊戶升級加開境外帳戶':
        buttons_template = ButtonsTemplate(
            title='舊戶升級加開境外帳戶。', text='親愛的投資朋友，您好：欲辦理舊戶升級加開境外帳戶,請依循下列方式:', 
            actions=[
                PostbackAction(label='請填寫服務異動申請書', 
                                data='請填寫服務異動申請書'),
                PostbackAction(label='請洽客服專線索取申請書', 
                                data='請洽客服專線索取申請書')
            ])
        template_message = TemplateSendMessage(
            alt_text='野村投信您好！這是我們野村舊戶升級加開境外帳戶流程。', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)
    elif data == '開戶申請書':
        line_bot_api.push_message(user_id, TextSendMessage(text='以下開立投信帳戶流程將包含4個項目, 請詳閱。'))
        message = ImageSendMessage('https://i.imgur.com/03BsqWKl.png','https://i.imgur.com/03BsqWKt.png')
        line_bot_api.reply_message(reply_token, message)
    elif data == '投資人風險屬性評估表':
        line_bot_api.push_message(user_id, TextSendMessage(text='以下投資人風險屬性評估表將包含2頁, 請詳閱。'))
        message = ImageSendMessage('https://imgur.com/ebig8EHl.png', 'https://imgur.com/ebig8EHt.png')
        line_bot_api.push_message(user_id, message)
        message = ImageSendMessage('https://i.imgur.com/nLEKdLgl.png', 'https://i.imgur.com/nLEKdLgt.png')
        line_bot_api.reply_message(reply_token, message)
    elif data == '自我證明表':
        line_bot_api.push_message(user_id, TextSendMessage(text='以下為自我證明表, 請詳閱。'))
        message = ImageSendMessage('https://imgur.com/nLEKdLgl.png', 'https://imgur.com/nLEKdLgt.png')
        line_bot_api.reply_message(reply_token, message)
    elif data == '蒐集、處理及利用個人資料告知事項':
        line_bot_api.push_message(user_id, TextSendMessage(text='以下為蒐集、處理及利用個人資料告知事項, 請詳閱。'))
        message = ImageSendMessage('https://imgur.com/nYlDwwql.png', 'https://imgur.com/nYlDwwqt.png')
        line_bot_api.reply_message(reply_token, message)
    elif data == '野村投信身分證明文件聲明書':
        line_bot_api.push_message(user_id, TextSendMessage(text='以下為野村投信身分證明文件聲明書, 請詳閱。'))
        message = ImageSendMessage('https://i.imgur.com/13GhNm0l.png', 'https://i.imgur.com/13GhNm0t.png')
        line_bot_api.reply_message(reply_token, message)        
    elif data == '投信基金扣款轉帳授權書':
        line_bot_api.push_message(user_id, TextSendMessage(text='以下為投信基金扣款轉帳授權書將包含2頁, 請詳閱。'))
        message = ImageSendMessage('https://i.imgur.com/krxXqUwl.png', 'https://i.imgur.com/krxXqUwt.png')
        line_bot_api.push_message(user_id, message)
        message = ImageSendMessage('https://i.imgur.com/dnpQlzUl.png', 'https://i.imgur.com/dnpQlzUt.png')
        line_bot_api.reply_message(reply_token, message)    
    elif data == '境外基金授權書(外幣)':
        line_bot_api.push_message(user_id, TextSendMessage(text='以下為境外基金授權書(外幣)將包含2頁, 請詳閱。'))
        message = ImageSendMessage('https://imgur.com/fx9ma4Rl.jpg', 'https://imgur.com/fx9ma4Rt.jpg')
        line_bot_api.push_message(user_id, message)
        message = ImageSendMessage('https://imgur.com/g4pXszOl.jpg', 'https://imgur.com/g4pXszOt.jpg')
        line_bot_api.reply_message(reply_token, message)
    elif data == '境外基金授權書(台幣)':
        line_bot_api.push_message(user_id, TextSendMessage(text='以下為境外基金授權書(台幣)將包含2頁, 請詳閱。'))
        message = ImageSendMessage('https://imgur.com/q0UBhhX.jpg', 'https://imgur.com/q0UBhhX.jpg')
        line_bot_api.push_message(user_id, message)
        message = ImageSendMessage('https://imgur.com/ty9GFc7.jpg', 'https://imgur.com/ty9GFc7.jpg')
        line_bot_api.reply_message(reply_token, message)    


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    reply_token = event.reply_token
    if text != '客服':
        buttons_template = ButtonsTemplate(
            title='野村投信線上表單。', text='親愛的投資朋友，您好：感謝您選擇野村投信做為您的理財夥伴，以下將為您介紹我們的三種開戶方式。', 
            actions=[
                PostbackAction(label='開立投信帳戶(1-4項)', data='開立投信帳戶(1-4項)'),
                PostbackAction(label='開立投信帳戶(5-6項)', data='開立投信帳戶(5-6項)'),
                PostbackAction(label='開立投信+境外帳戶', data='開立投信+境外帳戶'),
                PostbackAction(label='舊戶升級加開境外帳戶', data='舊戶升級加開境外帳戶'),
            ])
        template_message = TemplateSendMessage(
            alt_text='野村投信您好！這是我們目前提供的線上表單。', template=buttons_template)
        line_bot_api.reply_message(reply_token, template_message)
    else:
        # TODO
        print('連接外部聊天室')

if __name__ == "__main__":
    app.run()
