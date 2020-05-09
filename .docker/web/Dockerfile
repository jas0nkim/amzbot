#
# web (django)
#

FROM python:3.7-slim

COPY ./requirements.txt /requirements.txt
RUN pip install -r ./requirements.txt

RUN mkdir /app/
WORKDIR /app/
VOLUME /app/
