FROM python:3.12.2-slim-bookworm

WORKDIR /bot

COPY ./requirements.txt /bot
RUN pip install -r requirements.txt

COPY . /bot

EXPOSE 5000

CMD ["python", "main.py"]