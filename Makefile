up:
	docker compose up --build -d

down:
	docker compose down

log:
	docker compose logs -f app

ps:
	docker compose ps -a

run:
	make down
	make up
	make log
