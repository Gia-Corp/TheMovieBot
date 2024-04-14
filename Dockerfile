# Dockerfile for development docker image
FROM python:3.12.2-slim-bookworm
WORKDIR /bot

# Install git
RUN apt-get -y update
RUN apt-get -y install git

# Copy root directory and install project dependencies
ADD . .
RUN pip install --no-cache-dir -r requirements.txt