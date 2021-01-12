from bot import Bot, Update

token = '1520012046:AAFmCjltg7rosLi0aFktva42rbaezCkD-Z8'
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
            else:
                bot.send_message(update.chat_id, update.text)

        updates = bot.get_updates(offset)
        offset = updates['last_update_id'] + 1