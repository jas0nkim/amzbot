#
# web (django)
#

FROM python:3.7-slim

COPY ./requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

RUN mkdir /app/
WORKDIR /app/
VOLUME /app/
