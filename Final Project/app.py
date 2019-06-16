from flask import Flask, render_template, session, request, abort
from flask_socketio import SocketIO,emit
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
import sys
import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials as SAC


# Channel Access Token
line_bot_api = LineBotApi('請輸入Channel Access Token')
# Channel Secret
handler = WebhookHandler('請輸入Channel Secret')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
re_token = ""
@app.route('/')
def index():
    return render_template('index.html')



@socketio.on('client_event')
def client_msg(msg):
    if(msg['token']!=""):
        GDriveJSON = 'FinTech.json'
        GSpreadSheet = 'FinTech'
        try:
            scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
                     "https://www.googleapis.com/auth/drive"]
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).sheet1
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
        d = json.dumps(datetime.datetime.now(), default=myconverter)
        worksheet.append_row((d, 'IM', msg['userid'], msg['data']))
        print('新增一列資料到試算表', GSpreadSheet)
        line_bot_api.reply_message(msg['token'], TextSendMessage(text=msg['data']))
    else:
        emit('server_msg', {'data': "暫無客戶在線上"})


@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_msg', {'data': msg['data']})

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # your code is here
    repmsg = ""
    text = event.message.text
    userid = event.source.user_id
    reply_token = event.reply_token
    # GDriveJSON就輸入下載下來Json檔名稱
    # GSpreadSheet是google試算表名稱
    GDriveJSON = 'FinTech.json'
    GSpreadSheet = 'FinTech'
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]
        key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open(GSpreadSheet).worksheet('sheet2')
    except Exception as ex:
        print('無法連線Google試算表', ex)
        sys.exit(1)

    index = 0
    flowid = 0
    name = ''
    values_list = worksheet.col_values(1)
    if (userid in values_list):
        index = values_list.index(userid)+1
        flowid = int(worksheet.acell('B'+str(index)).value)
        name = worksheet.acell('C'+str(index)).value
        print('狀態:',flowid)
    if(text == '野村投信開戶流程'):
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
    elif (text == '即時客服' or flowid > 0):
        if (flowid==0):
            repmsg = "客戶您好，請問該怎麼稱呼您呢?"
            flowid += 1
            if (index != 0):
                cellsite = 'B' + str(index)
                worksheet.update_acell(cellsite, flowid)
            else:
                worksheet.append_row((userid, flowid))
        elif (flowid==1):
            repmsg = text+"，您好，請問有什麼能為您服務的嗎?"
            flowid += 1
            worksheet.update_acell('B' + str(index), flowid)
            worksheet.update_acell('C' + str(index), text)
            socketio.emit('server_msg', {'data': "客戶 "+text+"，已在線上。",'token':event.reply_token}, broadcast=True)
        else:
            if (text == "再見" or text == "Bye"):
                flowid = 0
                cellsite = 'B' + str(index)
                worksheet.update_acell(cellsite, flowid)
                repmsg = "很高興為您服務"
                socketio.emit('server_response', {'data': text, 'token': '','userid':'','name' : name}, broadcast=True)
                socketio.emit('server_msg', {'data': '客戶'+name+'已結束對話。'}, broadcast=True)
            else:
                socketio.emit('server_response', {'data': text,'token':event.reply_token,'userid':userid,'name' : name}, broadcast=True)

        if(repmsg!=""):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=repmsg))
        if text != "":
            pass
            while True:
                try:
                    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
                    key = SAC.from_json_keyfile_name(GDriveJSON, scope)
                    gc = gspread.authorize(key)
                    worksheet = gc.open(GSpreadSheet).sheet1
                except Exception as ex:
                    print('無法連線Google試算表', ex)
                    sys.exit(1)
                textt = ""
                textt += text
                if textt != "":
                    d = json.dumps(datetime.datetime.now(), default=myconverter)
                    worksheet.append_row((d, 'Customer', userid, textt))
                    print('新增一列資料到試算表', GSpreadSheet)
                    if repmsg != "":
                        d = json.dumps(datetime.datetime.now(), default=myconverter)
                        worksheet.append_row((d, 'IM', userid, repmsg))
                        print('新增一列資料到試算表', GSpreadSheet)
                    return textt
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="客戶您好，請利用下方選單選取您所需要的服務:)"))


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







def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()



if __name__ == "__main__":
    socketio.run(app)
