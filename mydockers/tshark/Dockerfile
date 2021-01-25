FROM alpine

RUN apk add --update --no-cache tshark curl bash&& rm -rf /var/cache/apk/*
COPY push.sh /root
WORKDIR /root
RUN chmod 555 push.sh
ENTRYPOINT ["/root/push.sh"]
