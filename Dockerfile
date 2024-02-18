FROM python:latest

WORKDIR /bot
COPY ./src ./bot

RUN pip3 install gspread python-telegram-bot

EXPOSE 5000