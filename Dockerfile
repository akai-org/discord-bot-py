FROM python:3.9.14

LABEL maintainer="radoslaw.winiecki@akai.org.pl"

COPY . .

RUN pip install -r requirements.txt

RUN python main.py wipe load