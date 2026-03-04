up:
	docker compose up --build

down:
	docker compose down

enter:
	docker compose exec -it app bash

test:
	docker compose -f docker-compose.test.yaml run --rm app

log:
	docker compose logs -f app

ps:
	docker compose ps -a

run:
	docker compose run -it --rm app
