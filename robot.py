
# TODO

"""
全局只有一个robot（单例模式）
统一获取、分配、调度robot

"""
import requests
text_url = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i={}'

text = '不告诉你'

data = requests.get(text_url.format(text)).json()
resp = {**data, 'translateResult': '\n'.join([row[0]['tgt'] for row in data['translateResult']])}

print(resp)