############################################################
# Dockerfile to build compiler server for compiling user code
# Based on Ubuntu
############################################################

FROM ubuntu:18.04

#Update the apt-get package
RUN apt-get update

#Install all the languages/compilers we are supporting.
RUN apt-get install -y gcc
RUN apt-get install -y g++

#prepare for Java download
RUN apt-get install -y python-software-properties
RUN apt-get install -y software-properties-common

#grab oracle java (auto accept licence)
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections
RUN apt-get install -y oracle-java8-installer