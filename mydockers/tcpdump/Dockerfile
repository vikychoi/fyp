FROM alpine

RUN apk add --update --no-cache tcpdump && rm -rf /var/cache/apk/*

ENTRYPOINT [ "/usr/sbin/tcpdump" ]
