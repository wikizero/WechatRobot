import requests


def translate(text):
    """
    有道自动翻译： fanyi.youdao.com
    :param text:
    :return:
    """
    url = 'https://fanyi.youdao.com/openapi.do?keyfrom=11pegasus11&key=273646050&type=data&doctype=json&version=1.1&q={}'
    data = requests.get(url.format(text)).json()
    ret = f"{data.get('translation')[0]}\n"
    if 'basic' in data:
        print(data)
        ret += f"{data['basic'].get('phonetic')}\n"
        ret += '\n'.join(data['basic'].get('explains')) + '\n'

    if 'web' in data:
        ret += '\n扩展:\n'
        ret += '\n'.join([f"{line.get('key')} {line.get('value')[0]}" for line in data.get('web')])

    return ret


if __name__ == '__main__':
    print(translate('love you'))
