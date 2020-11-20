app:
	docker-compose up --build

run-brokers:
	docker-compose up --build rabbit zookeeper broker

run-services:
	docker-compose up --build ping pong api

run-ping-localhost:
	cd ping && nameko run --config config.localhost.yml ping --broker amqp://guest:guest@localhost

run-pong-localhost:
	cd pong && nameko run --config config.localhost.yml pong --broker amqp://guest:guest@localhost
