FROM shmulya/telegram-bot:raw

WORKDIR /bot
COPY . .
RUN pip3 install -r requirements.txt
CMD python3 main.py
