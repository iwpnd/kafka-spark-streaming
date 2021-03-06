FROM openjdk:8-alpine

RUN apk --update add wget tar bash

RUN apk add --no-cache --update \
    git \
    bash \
    wget \
    tar \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    build-base \
    linux-headers
    # https://github.com/pyenv/pyenv/issues/1229

# Set Python version
ARG PYTHON_VERSION='3.7.5'
# Set pyenv home
ARG PYENV_HOME=/root/.pyenv

# Install pyenv, then install python versions
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_HOME && \
    rm -rfv $PYENV_HOME/.git

ENV PATH $PYENV_HOME/shims:$PYENV_HOME/bin:$PATH

RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION
RUN pip install --upgrade pip && pyenv rehash

RUN wget http://apache.mirror.iphh.net/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz
RUN tar -xzf spark-2.4.5-bin-hadoop2.7.tgz && \
    mv spark-2.4.5-bin-hadoop2.7 /spark && \
    rm spark-2.4.5-bin-hadoop2.7.tgz

COPY /scripts/start-spark-master.sh /start-spark-master.sh
COPY /scripts/start-spark-worker.sh /start-spark-worker.sh

COPY requirements.txt requirements.txt
COPY ./ /consumer
RUN pip install -r requirements.txt
RUN pip install -e consumer/

# Clean
RUN rm -rf ~/.cache/pip
