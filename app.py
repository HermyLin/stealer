# 載入需要的模組
from __future__ import unicode_literals
import os
import time
import json
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.exceptions import LineBotApiError
from linebot.models import *


#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.exc import IntegrityError
import csv
import re
import requests
import pandas as pd

#載入我們的py檔
from msg_template import Flex_template, Result_flex

#----------------資料庫設定-----------------

'''
ENV = 'prod'

if ENV == 'dev':
    from dotenv import load_dotenv
    load_dotenv()
    SQLALCHEMY_DATABASE_URI_PRIVATE = os.getenv("SQLALCHEMY_DATABASE_URI_PRIVATE")
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_PRIVATE
else:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# # #https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
'''
#----------------------------------------------------------------
#LINE聊天機器人的基本資料(取用heroku的環境變數)
app = Flask(__name__)

#line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
#handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

line_bot_api = LineBotApi('6miWE3Y5LfGTx4CIcVCGoapWfimm+8T0t6CoD5ZHqp0WUE59+/C3TgnJWqlqO6/m/H1yO8TUY+uabMjAmDTdWtc1EED8Y/1xkI/rp4BF3WOK6G32Oc6Gh1kHveeSCR0lntMHLnywb6m3bvMRLElZYAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d8854482344a37ad58e7b512629cc206')
line_bot_api.push_message('Ub91b0ca857ac49515bcfce296d54baf6', TextSendMessage(text='讓我們開始吧！'))

# 定義function與基礎設置
#---------------car type------------------
car_type_list = ['汽車','機車','腳踏車']
#----------------時間設定-------------------
time_label = ['上午','下午']
times = ['00:00-01:59','02:00-03:59','04:00-05:59','06:00-07:59','08:00-09:59','10:00-11:59','12:00-13:59','14:00-15:59','16:00-17:59','18:00-19:59','20:00-21:59','22:00-23:59']

# 開始串接linebot

#--------接收LINE資訊-------------------
@app.route("/", methods=['POST'])

def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    #print("Request body: " + body, "Signature: " + signature)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#----------------回覆訊息介面-----------------
@handler.add(MessageEvent, message=TextMessage) 
def handle_message(event):
 
    if event.message.text in == "機車":
        car_type = event.message.text    
        text_message_location = TextSendMessage(text='請分享位置給我，讓我守護您愛車的安全\udbc0\udc2e', 
                                quick_reply=QuickReply(items=[
                                QuickReplyButton(action=LocationAction(label="點點我分享"))]))    
        line_bot_api.reply_message(event.reply_token,text_message_location)
    elif event.message.text == "問題回報":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "先這樣"))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "先這樣"))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text= Text_template.user_report()))
        #製作問題回報表單(google)
    else:
        line_bot_api.reply_message(event.reply_token,"Oops!小守找不到您的資訊呢～")
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Oops!小守找不到您的資訊呢～"))
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text = Text_template.keyword_warning_text()))

#主程式        
#if __name__ == 'main':
#    app.run() 
#    app.run(debug=True) 
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)          #0000>所有人皆可連線
