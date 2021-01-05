FROM alpine

RUN apk add --update --no-cache tshark curl bash&& rm -rf /var/cache/apk/*
COPY push.sh /root
COPY root  /etc/crontabs/root
RUN chmod 555 /root/push.sh
CMD crond && tail -f /dev/null
