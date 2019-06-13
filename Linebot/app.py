from flask import Flask, render_template, session, request, abort
from flask_socketio import SocketIO,emit
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
line_bot_api = LineBotApi('SaWBAJr14nxXgAzOWm6GpyVHSMh0VBMNL2DL6KhrR9LZb6xriwq8riOPh/HLGgAl+KVWcm2QTX0wc7tFsa3FmjwgH5ZU4030AV/MinBo8vuvvlQDaCYCI9WlAT84MIDsXWTZmgTF22SwAT8AB5OF5wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3c8395d619f2321c4e607d9cd487e0fc')

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







def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()



if __name__ == "__main__":
    socketio.run(app)
