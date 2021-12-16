FROM python:rc-alpine3.14
ENV JIRA_URL="https://projects.grosver.com"
ENV TB_TOKEN="5077479764:AAGa4mqeq6zdmSz6XOaHqF7XrHCZkTiZJ_4"
RUN apk add gcc make build-base
RUN pip install --upgrade pip
RUN pip install aiogram==2.17.1 SQLAlchemy==1.4.28 requests
WORKDIR /usr/src/app
COPY ./*.py .
COPY ./*.db .

ENTRYPOINT [ "/usr/local/bin/python" ]
CMD ["telegram.py"]