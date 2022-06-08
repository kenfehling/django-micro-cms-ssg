FROM python:3.9-slim

RUN apt-get update
RUN apt-get install -y \
    git

WORKDIR /app

CMD ["bash", "scripts/init.sh"]
