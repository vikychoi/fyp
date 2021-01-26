# use --compatibility to support cpu/memory limit
start:
	docker-compose --compatibility up -d
	sudo sh ../outbound_limiting.sh

startbuild:
	docker-compose --compatibility up -d --build
	sudo sh ../outbound_limiting.sh

stop:
	docker-compose stop
