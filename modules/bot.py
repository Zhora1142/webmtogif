import requests


class Bot:
    def __init__(self, token):
        self.url = 'https://api.telegram.org/bot{}/'.format(token)
        try:
            response = requests.get(url=self.url + 'getMe').json()
        except Exception as e:
            raise e
        else:
            if response['ok'] is False:
                raise Exception('{} {}'.format({response["error_code"]}, {response["description"]}))

    def get_updates(self, offset=None, timeout=30):
        params = {'timeout': timeout, 'offset': offset}
        while True:
            try:
                response = requests.get(url=self.url + 'getUpdates', params=params).json()
            except Exception as e:
                return {'status': 'error', 'error': e}
            else:
                if response['ok'] is False:
                    return {'status': 'error', 'error': '{} {}'.format(response['error_code'], response['description'])}
                else:
                    if len(response['result']) != 0:
                        return {'status': 'ok', 'updates': response['result'],
                                'last_update_id': response['result'][-1]['update_id']}

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        try:
            response = requests.get(url=self.url + 'sendMessage', params=params).json()
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            if response['ok'] is False:
                return {'status': 'error', 'error': '{} {}'.format(response['error_code'], response['description'])}
            else:
                return {'status': 'ok', 'message_id': response['result']['message_id']}

    def send_animation(self, chat_id, animation_path):
        params = {'chat_id': chat_id}
        try:
            file = open(animation_path, 'rb')
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            pass
        files = {'animation': file}
        try:
            response = requests.post(url=self.url + 'sendAnimation', params=params, files=files).json()
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            if response['ok'] is False:
                return {'status': 'error', 'error': '{} {}'.format(response['error_code'], response['description'])}
            else:
                return {'status': 'ok'}

    def send_video(self, chat_id, video_path):
        params = {'chat_id': chat_id}
        try:
            file = open(video_path, 'rb')
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            pass
        files = {'video': file}
        try:
            response = requests.post(url=self.url + 'sendVideo', params=params, files=files).json()
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            if response['ok'] is False:
                return {'status': 'error', 'error': '{} {}'.format(response['error_code'], response['description'])}
            else:
                return {'status': 'ok'}

    def delete_message(self, chat_id, message_id):
        params = {'chat_id': chat_id, 'message_id': message_id}
        try:
            response = requests.get(url=self.url + 'deleteMessage', params=params).json()
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            if response['ok'] is False:
                return {'status': 'error', 'error': '{} {}'.format(response['error_code'], response['description'])}
            else:
                return {'status': 'ok'}

    def edit_message(self, chat_id, message_id, text):
        params = {'chat_id': chat_id, 'message_id': message_id, 'text': text}
        try:
            response = requests.get(url=self.url + 'editMessageText', params=params).json()
        except Exception as e:
            return {'status': 'error', 'error': e}
        else:
            if response['ok'] is False:
                return {'status': 'error', 'error': '{} {}'.format(response['error_code'], response['description'])}
            else:
                return {'status': 'ok'}


class Update:
    def __init__(self, update):
        self.chat_id = update['message']['chat']['id']
        if 'text' in update['message']:
            self.text = update['message']['text']
        else:
            self.text = None

        self.isCommand = False
        self.command = None
        self.command_offset = None
        self.command_length = None

        if 'entities' in update['message'] and update['message']['entities'][0]['type'] == 'bot_command':
            self.isCommand = True
            self.command_offset = update['message']['entities'][0]['offset']
            self.command_length = update['message']['entities'][0]['length']
            self.command = self.text[self.command_offset:self.command_offset + self.command_length]
