FROM mcr.microsoft.com/playwright:focal

RUN apt update && apt-get install -y python3-pip
RUN pip3 install TikTokApi
RUN python3 -m playwright install
COPY . .
RUN pip3 install -r requirements.txt