# fyp

## Todo
Configure host network setting
`iptable route host 22 port to 3000 port`

## 

## Requirements
`docker`
`docker-compose`

## Details
The container sshmitm exposes port 3000.

Credentials: `root:123456`

### Accessing the logs

`docker ps | grep mydockers_sshmitm`
You will get a container id
`docker exec -it <container_id> /bin/sh`
`cat sshmitm.log`


## Starting the containers
`make start`

## Build/Rebuild the containers
`make startbuild`

## Stop the containers

