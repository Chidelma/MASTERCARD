test:
	docker compose down
	docker compose -f ./test.docker-compose.yml -f ./docker-compose.yml up --build --renew-anon-volumes --abort-on-container-exit

run:
	docker compose down
	docker compose -f ./docker-compose.yml up --build --renew-anon-volumes --abort-on-container-exit
