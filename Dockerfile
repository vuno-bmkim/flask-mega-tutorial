FROM python:3.6-alpine

RUN adduser -D microblog

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN apk add --no-cache --virtual .build-deps gcc musl-dev 
RUN venv/bin/pip3 install -r requirements.txt
RUN apk del .build-deps gcc musl-dev

RUN venv/bin/pip3 install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]