.PHONY: prod start build run down clean drop_db prune

prod:
	@if [ $$(docker ps -q -f name=backend_app) ]; then \
			docker compose stop backend_app; \
			docker compose rm -f backend_app; \
	fi
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

clean:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs sudo rm -rf
	
drop_db: down
	docker volume rm $(shell basename $(PWD))_postgres-data-cats 

prune: down
	docker system prune -a
	docker volume prune -a
