#
# bot
#

FROM python:3.7-slim

ENV SCRAPY_SETTINGS_MODULE=pwbot.settings
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
