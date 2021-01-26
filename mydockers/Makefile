# use --compatibility to support cpu/memory limit
start:
	docker-compose --compatibility up -d

startbuild:
	docker rm -vf $(docker ps -a -q)
	docker-compose --compatibility up -d --build

stop:
	docker-compose stop
