FROM alpine:latest as build

RUN apk update && apk add --no-cache \ 
    autoconf build-base binutils cmake curl file gcc g++ git libgcc libtool linux-headers make musl-dev ninja tar unzip wget

RUN cd /tmp \
    && git clone https://github.com/fmadio/pcap2json\ 
    && cd pcap2json \
    && make all

FROM alpine:latest as runtime

RUN apk update && apk add --no-cache \ 
    libstdc++

RUN mkdir /usr/local/pcap2json
COPY --from=build /tmp/pcap2json/pcap2json /usr/local/pcap2json
RUN chmod +x /usr/local/pcap2json

