#
# bot
#

FROM python:3.7-slim

COPY ./requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

RUN mkdir /app/
WORKDIR /app/

COPY ./src/ /app/
### DEBUGGER ###
# RUN pip install ptvsd
ENV SCRAPY_SETTINGS_MODULE=pwbot.settings
