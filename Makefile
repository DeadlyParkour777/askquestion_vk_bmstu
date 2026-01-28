.PHONY: compose-up compose-down compose-build compose-logs app-shell migrate createsuperuser fill-db fill-db-local

compose-up:
	docker compose up --build

compose-down:
	docker compose down

compose-build:
	docker compose build

compose-logs:
	docker compose logs -f

app-shell:
	docker compose exec app /bin/sh

migrate:
	docker compose exec app python manage.py migrate

createsuperuser:
	docker compose exec app python manage.py createsuperuser

fill-db:
	docker compose exec app python manage.py fill_db 10

fill-db-local:
	python manage.py fill_db 10
