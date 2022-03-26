# Makefile for standalone Music service (S2)

VER=v0.8

SERVER=`docker inspect S3 --format '{{.NetworkSettings.IPAddress}}'`
PORT=30003

build-pcli:
	docker image build -f Dockerfile -t pcli:$(VER) .

run-pcli:
	docker container run -it --rm --name pcli pcli:$(VER) python3 pcli.py $(SERVER) $(PORT)