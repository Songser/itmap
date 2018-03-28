FROM node:9.9.0-alpine
MAINTAINER songcser

RUN mkdir /web
WORKDIR /web

COPY package.json /web
RUN npm install --registry=https://registry.npm.taobao.org --chromedriver_cdnurl=http://cdn.npm.taobao.org/dist/chromedriver
