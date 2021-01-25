FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
apt install -y libwww-perl libjson-perl ethtool libyaml-dev systemd iproute2 wget sudo

COPY moloch_2.7.1-1_amd64.deb /root
RUN apt install -y /root/moloch_2.7.1-1_amd64.deb && rm -rf /var/lib/apt/lists/*

COPY config.ini /data/moloch/etc/config.ini
RUN /data/moloch/bin/moloch_add_user.sh elastic "Admin User" myfyp@123 --admin && /data/moloch/bin/moloch_update_geo.sh && mkdir /data/moloch/raw && chmod 755 /data/moloch/raw
#CMD tail -f /dev/null
CMD /data/moloch/bin/moloch-capture --pcapfile /tcpdump/tcpdump-pipe --copy --flush -o offlineDispatchAfter=1