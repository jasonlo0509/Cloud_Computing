############################################################
# Dockerfile to build client for sending code and monitor close event
# Based on Ubuntu
############################################################

FROM ubuntu:16.04
MAINTAINER  Yunchen Lo (NTHU|email:yunchen.lo@gapp.nthu.edu.tw)

#Update the apt-get package
RUN apt-get update

#prepare pip and twisted
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install -q build-essential && \
    apt-get -y install -q python-dev libffi-dev libssl-dev python-pip
RUN pip install service_identity pycrypto && \
    pip install twisted==14.0.0
RUN pip install pyinotify

RUN mkdir -p /app/client/result

#set environment
WORKDIR /app
ADD . /app


CMD ["python", "client.py"]
