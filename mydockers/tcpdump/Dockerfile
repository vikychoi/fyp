FROM alpine

RUN apk add --update --no-cache tcpdump && rm -rf /var/cache/apk/*

COPY entry.sh /entry.sh
RUN chmod +x /entry.sh

CMD /entry.sh && tail -f /dev/null