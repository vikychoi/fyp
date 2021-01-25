#!/bin/bash

function esbulk() {
  curl -H content-type:application/x-ndjson -X POST -H "Tranfer-Encoding: chunked" \
    "http://${ELASTICSEARCH_HOSTS}:9200/_bulk?filter_path=took,errors,items.*.error" \
    -s -w "\n" --data-binary "@-" -u ${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD}
}

tshark -I -i /tcpdump/tcpdump-pipe -T ek > esbulk
tail -f /dev/null
