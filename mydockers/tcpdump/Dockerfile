FROM alpine

RUN apk add --update --no-cache tcpdump bash && rm -rf /var/cache/apk/*

COPY entry.sh /

RUN chmod 555 /entry.sh

ENTRYPOINT [ "/entry.sh" ]
