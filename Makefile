init:
	pip install -r requirements.txt
format:
	black ./src
lint:
	pytest src/ --pylint --flake8 --mypy
docker-build:
	docker build -f Dockerfile . --tag anencore9494/clubhouse-github-action:${TAG}
docker-push:
	docker push anencore9494/clubhouse-github-action:${TAG}
