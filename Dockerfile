FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

COPY . .

RUN mkdir -p /usr/src/app/staticfiles

RUN chmod +x /usr/src/app/docker-entrypoint.sh

CMD ["sh", "docker-entrypoint.sh"]