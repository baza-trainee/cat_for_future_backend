.PHONY: prod start build run down clean drop_db prune

prod:
	docker compose stop backend_app
	docker compose rm -f backend_app
	docker compose up -d --build

down:
	docker compose down

run: down 
	docker compose up postgres redis -d 
	sleep 2
	alembic upgrade head
	uvicorn src.main:app --reload

start:
	uvicorn src.main:app --reload

build: down
	docker compose up -d --build

open-redis:
	docker exec -it redis_cats redis-cli

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf

drop_db: down
	docker volume rm cats_postgres-data-cats 

prune: down
	docker system prune -a
	docker volume prune -a
