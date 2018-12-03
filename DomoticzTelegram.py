# This script controls Domoticz via Telegram Messages

import telebot
import requests
import base64

API_TOKEN = '<api_token>'
Ip = '<ip>'
Port = '<port>'
Username = '<username>'
Password = '<password>'


def encode(username, password):
    userPwdCombo = username+':'+password
    bytes = userPwdCombo.encode()
    encodedPwd = base64.b64encode(bytes)
    return 'Basic ' + encodedPwd.decode("utf-8")


headers = {'Authorization': encode(Username, Password)}

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, Weclome to the Domoticz bot!.\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    messageText = message.text
    messageSplit = messageText.split()
    r = requests.get('http://'+Ip+':'+Port+'/json.htm?type=command&param=switchlight&idx='+messageSplit[0]+'&switchcmd='+messageSplit[1], headers=headers)
    if(r.status_code == 200):
        bot.reply_to(message, message.text)
    else:
        bot.reply_to(message, 'Unable to execute action')


bot.polling()
