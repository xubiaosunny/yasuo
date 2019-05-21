FROM python:3.7
RUN mkdir /code

ADD . /code
WORKDIR /code

RUN apt-get update && apt-get install -y ffmpeg gettext

RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
