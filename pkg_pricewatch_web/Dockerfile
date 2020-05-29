#
# web (django)
#

FROM python:3.7-slim

ENV DJANGO_SETTINGS_MODULE=pwweb.settings
ENV USER mydk

RUN useradd -m -d /home/${USER} ${USER} \
    && chown -R ${USER} /home/${USER}
USER ${USER}
WORKDIR /home/${USER}/

COPY --chown=${USER}:${USER} ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /home/${USER}/app/
WORKDIR /home/${USER}/app/

COPY --chown=${USER}:${USER} ./src/ /home/${USER}/app/

### DEBUGGER ###
# RUN pip install ptvsd
# CMD ["python", "-m", "ptvsd", "--host", "0.0.0.0", "--port", "5678", "--wait", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# https://docs.gunicorn.org/en/stable/
# gunicorn -b 127.0.0.1:8000 pwweb.wsgi:application
