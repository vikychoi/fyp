FROM alpine

RUN apk add --update --no-cache tshark curl && rm -rf /var/cache/apk/*
COPY push.sh /root
RUN chmod +x /root/push.sh
