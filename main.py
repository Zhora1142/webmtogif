import yaml
from modules.bot import Bot, Update
from modules.converter import Converter
from threading import Thread
import re

config = yaml.load(open('./config/config.yml', 'r').read())
bot = Bot(config['token'])


def gif(u):
    c = Converter()
    result = re.search('((http|https)://\S+)', u.text)
    if result is None:
        bot.send_message(u.chat_id, 'В сообщении нужно указать ссылку')
    else:
        url = result.group(0)
        msg_id = bot.send_message(u.chat_id, 'Скачивание файла...')['message_id']
        try:
            path = c.download(url)['path']
        except:
            bot.edit_message(u.chat_id, msg_id, 'Не удалось скачать файл. Возможно, Вы указали неверную ссылку.')
        else:
            bot.edit_message(u.chat_id, msg_id, 'Конвертирование файла...')
            try:
                path2 = c.to_gif(path)['path']
            except:
                bot.edit_message(u.chat_id, msg_id, 'Не удалось конвертировать файл.')
                c.delete(path)
            else:
                bot.edit_message(u.chat_id, msg_id, 'Отправка файла...')
                try:
                    bot.send_animation(u.chat_id, path2)
                except:
                    bot.edit_message(u.chat_id, msg_id, 'Не удалось отправить файл.')
                else:
                    bot.delete_message(u.chat_id, msg_id)
                    c.delete(path)
                    c.delete(path2)


def mp4(u):
    c = Converter()
    result = re.search('((http|https)://\S+)', u.text)
    if result is None:
        bot.send_message(u.chat_id, 'В сообщении нужно указать ссылку')
    else:
        url = result.group(0)
        msg_id = bot.send_message(u.chat_id, 'Скачивание файла...')['message_id']
        try:
            path = c.download(url)['path']
        except:
            bot.edit_message(u.chat_id, msg_id, 'Не удалось скачать файл. Возможно, Вы указали неверную ссылку.')
        else:
            bot.edit_message(u.chat_id, msg_id, 'Конвертирование файла...')
            try:
                path2 = c.to_mp4(path)['path']
            except:
                bot.edit_message(u.chat_id, msg_id, 'Не удалось конвертировать файл.')
                c.delete(path)
            else:
                bot.edit_message(u.chat_id, msg_id, 'Отправка файла...')
                try:
                    bot.send_video(u.chat_id, path2)
                except:
                    bot.edit_message(u.chat_id, msg_id, 'Не удалось отправить файл.')
                else:
                    bot.delete_message(u.chat_id, msg_id)
                    c.delete(path)
                    c.delete(path2)


if __name__ == '__main__':
    updates = bot.get_updates()
    if updates['status'] != 'ok':
        raise Exception(updates['error'])
    updates['updates'] = [updates['updates'][-1]]
    offset = updates['last_update_id'] + 1
    print('Bot started')
    while True:
        # Обработка полученных обновлений
        for i in updates['updates']:
            if 'message' in i:  # Проверка наличия ключа "message" в обрабатываемом обновлении
                update = Update(i)
                if update.text:  # Проверка наличия текста в сообщении
                    if update.isCommand:  # Проверка наличия команды в сообщении

                        if update.command == '/start':  # Команда start
                            bot.send_message(update.chat_id, 'Введи /help для просмотра списка команд')

                        elif update.command == '/help':  # Комнда load
                            message = 'Список доступных команд:\n\n' \
                                      '/help - посмотреть список команд\n' \
                                      '/mp4 url - конвертировать webm в mp4\n' \
                                      '/gif url - конвертировать webm в gif'
                            bot.send_message(update.chat_id, message)

                        elif update.command == '/mp4':
                            process = Thread(target=mp4, args=(update,))
                            process.start()

                        elif update.command == '/gif':
                            process = Thread(target=gif, args=(update,))
                            process.start()

        updates = bot.get_updates(offset)
        offset = updates['last_update_id'] + 1
