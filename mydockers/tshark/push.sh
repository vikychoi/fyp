#!/bin/sh

function esbulk() {
  curl -H content-type:application/x-ndjson -X POST \
    "http://${ELASTICSEARCH_HOSTS}:9200/_bulk?filter_path=took,errors,items.*.error" \
    -s -w "\n" --data-binary "@-" -u ${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD}
}
function esput() {
  curl -H content-type:application/x-ndjson -X PUT \
    "http://${ELASTICSEARCH_HOSTS}:9200/${1#/}?filter_path=took,errors,items.*.error" \
    -s -w "\n" --data-binary "@-"
}

tshark -r $1 -T ek | esbulk && echo "success"
