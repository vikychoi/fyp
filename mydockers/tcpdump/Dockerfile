FROM ubuntu:20.04

RUN apt update && \
apt install -y tcpdump bash

COPY entry.sh /

RUN chmod 555 /entry.sh

ENTRYPOINT [ "/entry.sh" ]
