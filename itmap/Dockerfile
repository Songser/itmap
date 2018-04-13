FROM python:3.6.5-alpine
MAINTAINER songcser

RUN mkdir /server
WORKDIR /server

ADD requirements.txt /server

RUN pip install -i 'http://pypi.douban.com/simple' --trusted-host pypi.douban.com -r requirements.txt
