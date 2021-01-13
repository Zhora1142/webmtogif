from modules.bot import Bot, Update

token = ''
bot = Bot(token)


if __name__ == '__main__':
    updates = bot.get_updates()
    offset = updates['last_update_id'] + 1
    print('Bot started')
    while True:
        for i in updates['updates']:
            update = Update(i)
            if update.text == '/start':
                bot.send_message(update.chat_id, 'Приветствую!')
            elif update.text:
                bot.send_message(update.chat_id, update.text)
            else:
                bot.send_message(update.chat_id, 'что это')

        updates = bot.get_updates(offset)
        offset = updates['last_update_id'] + 1
