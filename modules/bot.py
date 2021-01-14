import requests


class Bot:
    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot{}/'.format(token)
        try:
            resp = requests.get(url=self.url + 'getMe').json()
        except Exception:
            raise
        else:
            if resp['ok'] is False:
                raise Exception('{} {}'.format({resp["error_code"]}, {resp["description"]}))

    def get_updates(self, offset=None, timeout=30):
        params = {'timeout': timeout, 'offset': offset}
        while True:
            try:
                response = requests.get(url=self.url + 'getUpdates', params=params).json()
            except:
                pass
            else:
                if response['ok'] is False:
                    raise Exception('{} {}'.format(response["error_code"], response["description"]))
                else:
                    print('Получено сообщение')
                    if len(response['result']) == 0:
                        pass
                    else:
                        return {'updates': response['result'], 'last_update_id': response['result'][-1]['update_id']}

    def send_message(self, chat_id, message):
        params = {'chat_id': chat_id, 'text': message}
        try:
            response = requests.get(url=self.url + 'sendMessage', params=params).json()
        except Exception:
            raise
        else:
            if response['ok'] is False:
                raise Exception('{} {}'.format(response["error_code"], response["description"]))

    def send_animation(self, chat_id, animation):
        params = {'chat_id': chat_id}
        files = {'animation': animation}
        try:
            response = requests.post(url=self.url + 'sendAnimation', params=params, files=files).json()
        except Exception:
            raise
        else:
            if response['ok'] is False:
                raise Exception('{} {}'.format(response["error_code"], response["description"]))


class Update:
    def __init__(self, update):
        self.chat_id = update['message']['chat']['id']
        if 'text' in update['message']:
            self.text = update['message']['text']
        else:
            self.text = None
