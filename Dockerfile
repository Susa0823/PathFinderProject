FROM python:3.11-alpine3.16

# No buffered std output from python is ensured by the following line
ENV PYTHONUNBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /PathFinder

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
# apk -> Alpine Package Keeper
RUN apk add --no-cache --update postgresql-client && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache --update postgresql-client && \
    apk add --no-cache --update --virtual .tmp-build-deps
    # RUN python -m venv /py && \
#     apk update && \
#     /py/bin/pip install --upgrade pip && \
#     apk add --virtual build-deps gcc python3-dev musl-dev && \
#     apk add --no-cache --update postgresql-client && \
#     apk add --no-cache --update --virtual .tmp-build-deps \
#     build-base postgresql-dev &&\
#     /py/bin/pip install -r /requirements.txt && \
#     apk del .tmp-build-deps && \
#     adduser --disabled-password --no-create-home PathFinderDevUser


#CMD python manage.py runserver 0.0.0.0:8000
# ENV PATH="/py/bin:$PATH"
# USER PathFinderDevUser

# CMD ["python3 manage.py runserver &"]

# EXPOSE 2375
