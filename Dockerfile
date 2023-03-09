FROM python:3.11.0
ENV PYTHONUNBUFFERED=1
RUN mkdir /PathFinder
WORKDIR /PathFinder
ADD . /PathFinder/

RUN pip install -r requirements.txt

ENV env $env

CMD ["python3 manage.py runserver &"]

EXPOSE 8000