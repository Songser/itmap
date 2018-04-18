FROM cheewai/py3-psycopg2
MAINTAINER songcser

RUN mkdir /itmap
WORKDIR /itmap

ADD requirements.txt /itmap

RUN pip install -i 'http://pypi.douban.com/simple' --trusted-host pypi.douban.com -r requirements.txt
