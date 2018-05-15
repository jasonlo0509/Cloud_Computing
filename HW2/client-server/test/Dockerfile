############################################################
# Dockerfile to build compiler server for compiling user code
# Based on Ubuntu
############################################################

FROM ubuntu:14.04
MAINTAINER  Yunchen Lo (NTHU|email:yunchen.lo@gapp.nthu.edu.tw)

#Update the apt-get package
RUN apt-get update

#Install all the languages/compilers we are supporting.
RUN add-apt-repository ppa:jonathonf/gcc-7.1
RUN apt-get update

RUN apt-get install -y gcc-7 g++-7

#prepare for Java download
RUN apt-get install -y python-software-properties
RUN apt-get install -y software-properties-common

#grab oracle java (auto accept licence)
RUN add-apt-repository ppa:linuxuprising/java
RUN apt-get update
RUN echo oracle-java10-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get install -y oracle-java10-installer

#prepare pip and twisted
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install -q build-essential && \
    apt-get -y install -q python-dev libffi-dev libssl-dev python-pip
RUN pip install service_identity pycrypto && \
    pip install twisted==14.0.0

CMD ["python", "server.py"]
