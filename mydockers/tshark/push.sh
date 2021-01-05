#!/bin/bash

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


for file in /in/*; do
  echo "reading file $file"
  size=$(wc -c $file | awk -F " " '{print $1}')
  now=$(date +%s)
  last_modified=$(date -r $file +%s)
  let untouched_duration=$now-$last_modified
  echo "ud = $untouched_duration"
  echo "size = $size"
  if(($size>=${MAX_FILE_SIZE} && $untouched_duration>60));then	#upload the dump file if it reaches max size
    echo "uploading $file"
    tshark -r $file -T ek | esbulk > /dev/null
  fi
done
