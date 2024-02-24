FROM python:3.12.2-slim-bookworm

WORKDIR /bot

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

CMD ["python", "src/main.py"]