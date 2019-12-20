
#Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage ,ImageSendMessage
import queue
import threading
import random
import time
import random, requests
import DAN
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi('bywfHFLgGHO4VkQ+JS+FPFMBqE9WF9x4q9VG7tJ32u5X+18H9qm7sQfpuHZKSwLZnNOEIHpSOR32JiGbV0qMR5oCxFEUTRLJ32CnZi0Jzp65xCU57bsrXyF11/R3yTxxEhhhFzBMaeWhUWrXUye+JQdB04t89/1O/w1cDnyilFU=') #LineBot's Channel access token
handler = WebhookHandler('d40058f56b8e615b8a9c9ddc045b5bce')        #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)


def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))   # Reply API example
    
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)
def Print(arg):
    while True:
        try:
            
            NUM = DAN.pull('HKA_MSG_NUM')
            print(NUM)
            NUM = str(NUM)
            NUM = NUM.replace("[","")
            NUM = NUM.replace("]","")
            NUM = NUM.replace("'","")
            
            String = DAN.pull('HKA_MSG_STRING')
            print(String)
            String = str(String)
            String = String.replace("[","")
            String = String.replace("]","")
            String = String.replace("'","")

            for userId in user_id_set:
                if NUM != 'None' and String != 'None':
                    line_bot_api.push_message(userId, TextSendMessage(text = NUM +' 時間: '+ String))  # Push API example
            time.sleep(0.5)
        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)  

   
if __name__ == "__main__":
    ServerURL = 'https://6.iottalk.tw' #with SSL connection
    Reg_addr = 'egjpegnwpdbnweigwpgo' #if None, Reg_addr = MAC address

    DAN.profile['dm_name']='HKA_MSG'
    DAN.profile['df_list']=['HKA_MSG_I','HKA_MSG_NUM','HKA_MSG_STRING']
    DAN.profile['d_name']='MSG'
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    idList = loadUserId()
    if idList: user_id_set = set(idList)
    image_url ='https://img.ltn.com.tw/Upload/news/600/2019/12/18/3012910_2_1.jpg'
    try:
        for userId in user_id_set:
            #line_bot_api.push_message(userId, TextSendMessage(text='早安'))  # Push API example
            line_bot_api.push_message(userId,ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
    except Exception as e:
        print(e)
    t = threading.Thread(target=Print,args=(user_id_set,))
    t.daemon = True     # this ensures thread ends when main process ends
    t.start()

    
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

    

