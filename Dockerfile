FROM python:3.10-alpine as build
COPY . .
RUN apk update
RUN apk --no-cache add openjdk8-jre msttcorefonts-installer libreoffice-writer && rm -rf /var/cache/apk/* && rm -rf /tmp/*
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /var/cache/apk/*

ENV PORT 6000

CMD ["python", "main.py"]
