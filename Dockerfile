FROM python:3.9-slim-buster

WORKDIR /app
COPY src/main.py main.py

CMD ["python", "/app/main.py"]
