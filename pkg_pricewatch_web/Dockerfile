#
# web (django)
#

FROM python:3.7-slim

ENV USER mydk
ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV PYTHONPATH="/app/"
ENV DJANGO_SETTINGS_MODULE=pwweb.settings

RUN mkdir -p /usr/local/etc/pricewatch/ \
    && mkdir /app/ \
    && useradd -m -d /home/${USER}/ ${USER} \
    && chown -R ${USER} /home/${USER}/ \
    && chown -R ${USER} /app/ \
    && chown -R ${USER} /usr/local/etc/pricewatch/
USER ${USER}
WORKDIR /home/${USER}/

COPY --chown=${USER}:${USER} ./requirements.txt requirements.txt
COPY --chown=${USER}:${USER} ./src/ /app/

RUN pip install -r requirements.txt

WORKDIR /app/

VOLUME [ "/usr/local/etc/pricewatch/", "/app/" ]

### DEBUGGER ###
# RUN pip install ptvsd
# CMD ["python", "-m", "ptvsd", "--host", "0.0.0.0", "--port", "5678", "--wait", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# https://docs.gunicorn.org/en/stable/
# gunicorn -b 127.0.0.1:8000 pwweb.wsgi:application
