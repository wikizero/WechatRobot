import os
import json

from datetime import datetime
from flask import Flask, make_response, send_from_directory
from flask import request
# from flask_session import Session
from flask import render_template

import requests

from wechatpy.utils import check_signature
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply
from wechatpy.exceptions import InvalidSignatureException

import mongo
from translate import translate

token = '123token'
secret_key = os.urandom(24)  # 生成密钥，为session服务。
print(f'secret_key: {secret_key}')
app = Flask(__name__)


def talk(msg):
    header = {
        'Referer': 'https://home.pandorabots.com/home.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }

    url = 'https://miapi.pandorabots.com/talk'
    dct = {'botkey': 'n0M6dW2XZaccDR2ye23r2QNHZ-WUXlDMgobNpgPv9060_72eKnu3Yl-o1v2nFGtSXqfwJBG2Ros~',
           'input': msg,
           'sessionid': 1380491,
           'client_name': 'home-ci-client-1584374747612-71'}

    res = requests.post(url, data=dct, headers=header)
    if res.status_code == 200:
        response = res.json()['responses']
        return response[0] if response else "Sorry, I don't understand that."
    return "There is something wrong with the server. Please try again later."


# def translate(text):
#     """
#     有道自动翻译： fanyi.youdao.com
#     :param text:
#     :return:
#     """
#     text_url = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i={}'
#     data = requests.get(text_url.format(text)).json()
#     return '\n'.join([row[0]['tgt'] for row in data['translateResult']])


def handle_msg(msg):
    """
    处理微信消息
    :param msg:
    :return:
    """
    print(msg, dir(msg))
    if not msg:
        return ''
    msg_type = msg.type
    if msg_type == 'voice':
        # Recognition 是中文信息，需要翻译
        recognition = msg.recognition
        return translate(recognition)
    elif msg_type == 'text':
        text = msg.content
        if text.startswith('ted'):
            suffix = text.replace('ted', '').strip()
            if suffix:
                return mongo.query(suffix) or 'Sorry?'
            return mongo.query('a') or 'Sorry?'
        return translate(text)
    elif msg_type == 'image':
        return "Sorry, I can't recognize the picture yet!"  # talk(msg.image)
    elif msg_type == 'link':
        return translate(msg.url)
    elif msg_type == 'location':
        return translate(msg.label)


@app.route('/token', methods=['get', 'POST'])
def token():
    if request.method == 'GET':
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echo_str = request.args.get('echostr')  # echo_str是微信用来验证服务器的参数，需原样返回
        print(signature, timestamp, nonce, echo_str)

        try:
            print('正在验证服务器签名')
            # 无法验证成功？？？
            # check_signature(token, signature, timestamp, nonce)
            print('验证签名成功')
        except InvalidSignatureException as e:
            print('检查签名出错: '.format(e))
            return 'Check Error'

        return echo_str

    # POST
    print('开始处理用户消息')
    msg = parse_message(request.data)
    reply_text = handle_msg(msg)
    reply = TextReply(message=msg)
    reply.content = reply_text
    return reply.render()


if __name__ == '__main__':
    # TODO 分配robot 或找其他robot代替
    # TODO 寻找推送资源 （简单的英文信息，推送模板 怎么定义的？）
    # TODO 单独给某个用户推送资源。做英语能力测试，然后收集英语文章信息做等级分类

    app.run(host='0.0.0.0', port=8081, debug=True)
