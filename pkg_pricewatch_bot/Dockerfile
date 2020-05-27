#
# bot
#

FROM python:3.7-slim as base

COPY ./requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

RUN mkdir /app/
WORKDIR /app/

COPY ./src/ /app/
ENV SCRAPY_SETTINGS_MODULE=pwbot.settings

######## START NEW IMAGE : DEBUGGER ########
FROM base as debug
RUN pip install ptvsd

WORKDIR /app/

######## START NEW IMAGE : PRODUCTION ########
FROM base as prod

WORKDIR /app/
