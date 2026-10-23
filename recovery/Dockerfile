
FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ansible curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install the official Docker CLI
RUN curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-29.1.5.tgz \
    | tar -xz --strip-components=1 -C /usr/local/bin docker/docker

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
