up:
	docker compose up --build

down:
	docker compose down

log:
	docker compose logs -f app

ps:
	docker compose ps -a

run:
	docker compose run -it --rm app
