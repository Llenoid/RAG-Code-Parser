up:
	docker compose up --build -d
down:
	docker compose down
log:
	docker compose logs -f app

run:
	make down
	make up
	make log
