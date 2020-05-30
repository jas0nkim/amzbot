#
# bot
#

FROM python:3.7-slim

ENV SCRAPY_SETTINGS_MODULE=pwbot.settings
ENV USER mydk

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
