FROM ubuntu:20.04

LABEL maintainer="radoslaw.winiecki@akai.org.pl"

RUN apt-get update -y &&\
    apt-get install -y python3-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]