FROM python:3.11.2-alpine3.16

# No buffered std output from python is ensured by the following line
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt
COPY ./PathFinder /PathFinder

WORKDIR /PathFinder

# apk -> Alpine Package Keeper
RUN python -m venv /py && \
    apk update && \
    /py/bin/pip install --upgrade pip && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache --update postgresql-client && \
    apk add --no-cache --update --virtual .tmp-build-deps \
    build-base postgresql-dev &&\
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-build-deps && \
    adduser --disabled-password --no-create-home PathFinderDevUser

ENV PATH="/py/bin:$PATH"
USER PathFinderDevUser

CMD ["python3 manage.py runserver &"]

EXPOSE 8000
