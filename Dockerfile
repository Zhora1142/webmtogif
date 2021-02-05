FROM shmulya/telegram-bot:raw

WORKDIR /bot
COPY . .
RUN pip3 install -r requirements.py
CMD python3 main.py
