help:
	cat Makefile
	echo '======================================'
	cat README.md
web:
	bash -c '(source .env && python -m soa)'
services: database redis
	docker ps
export:
	poetry export -f requirements.txt -o requirements.txt
database:
	docker run --rm -e "POSTGRES_PASSWORD=password" -p 5431:5432 --name soa_db -d postgres
redis:
	docker run --rm -d -p 6379:6379 --name soa_redis redis
stop:
	docker stop soa_db soa_redis
