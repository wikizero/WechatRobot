import os
import json

from datetime import datetime
from flask import Flask, make_response, send_from_directory
from flask import request
# from flask_session import Session
from flask import render_template

from wechatpy.utils import check_signature
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply
from wechatpy.exceptions import InvalidSignatureException

token = '123token'
secret_key = os.urandom(24)  # 生成密钥，为session服务。
print(f'secret_key: {secret_key}')
app = Flask(__name__)


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
            #check_signature(token, signature, timestamp, nonce)
            print('验证签名成功')
        except InvalidSignatureException as e:
            print('检查签名出错: '.format(e))
            return 'Check Error'

        return echo_str

    print('开始处理用户消息')
    msg = parse_message(request.data)
    print(msg, msg.content)
    xml = TextReply(context='xxxx', message=msg).render()
    xml = xml.replace('<Content><![CDATA[]]></Content>', '<Content><![CDATA[hello world]]></Content>')
    print(type(xml))
    print(xml)
    return xml 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
