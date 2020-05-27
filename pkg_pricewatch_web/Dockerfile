#
# web (django)
#

FROM python:3.7-slim as base

COPY ./requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

RUN mkdir /app/
WORKDIR /app/

COPY ./src/ /app/
ENV DJANGO_SETTINGS_MODULE=pwweb.settings

######## START NEW IMAGE : DEBUGGER ########
FROM base as debug
RUN pip install ptvsd

WORKDIR /app/
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait manage.py runserver 0.0.0.0:8000

######## START NEW IMAGE : PRODUCTION ########
FROM base as prod

WORKDIR /app/
CMD python manage.py runserver 0.0.0.0:8000
# https://docs.gunicorn.org/en/stable/
# gunicorn -b 127.0.0.1:8000 pwweb.wsgi:application
