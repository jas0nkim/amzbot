#
# mod Dockerfile from scrapyd:py3 (support python 3.7)
# https://github.com/vimagick/dockerfiles/blob/master/scrapyd/py3/Dockerfile
#

FROM debian:stretch

COPY ./requirements.txt /root/
RUN set -xe \
    && apt-get update \
    && apt-get install -y autoconf \
                          build-essential \
                          curl \
                          git \
                          libffi-dev \
                          libssl-dev \
                          libtool \
                          libxml2 \
                          libxml2-dev \
                          libxslt1.1 \
                          libxslt1-dev \
                          vim-tiny \
    && apt-get install -y libtiff5 \
                          libtiff5-dev \
                          libfreetype6-dev \
                          libjpeg62-turbo \
                          libjpeg62-turbo-dev \
                          liblcms2-2 \
                          liblcms2-dev \
                          libwebp6 \
                          libwebp-dev \
                          zlib1g \
                          zlib1g-dev \
                          libncurses5-dev \
                          libgdbm-dev \
                          libnss3-dev \
                          libreadline-dev \
                          libpq-dev \
    && curl -O https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tar.xz \
    && tar -xf Python-3.7.6.tar.xz \
    && cd Python-3.7.6 \
    && ./configure --enable-optimizations \
    && make -j 8 \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.7.6 \
    && pip install scrapyd \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove autoconf \
                                      build-essential \
                                      libffi-dev \
                                      libssl-dev \
                                      libtool \
                                      libxml2-dev \
                                      libxslt1-dev \
    && apt-get purge -y --auto-remove libtiff5-dev \
                                      libfreetype6-dev \
                                      libjpeg62-turbo-dev \
                                      liblcms2-dev \
                                      libwebp-dev \
                                      zlib1g-dev \
                                      libncurses5-dev \
                                      libgdbm-dev \
                                      libnss3-dev \
                                      libreadline-dev \
                                      libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./scrapyd.conf /etc/scrapyd/
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
EXPOSE 6800

CMD ["scrapyd", "--pidfile="]
