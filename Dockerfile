FROM python:3.11-slim-buster

# Buildable docker image for production
# No buffered std output from python is ensured by the following line
ENV PYTHONUNBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

WORKDIR /PathFinder
COPY ./requirements.prod.txt .
COPY . .

RUN buildDeps='gcc' \
    && set -x \
    && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
    && apt-get install -y libc6-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.prod.txt \
    && apt-get purge -y --auto-remove $buildDep
