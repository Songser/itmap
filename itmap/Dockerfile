FROM python:3.6-alpine3.6

RUN mkdir /itmap
WORKDIR /itmap

ADD requirements.txt /itmap
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache gcc libc-dev postgresql-dev \
    && pip install -i 'http://pypi.douban.com/simple' --trusted-host pypi.douban.com -r requirements.txt \
    &&rm -rf /var/cache/apk/* /tmp/* /var/tmp/* $HOME/.cache

#WORKDIR /
