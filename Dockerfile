FROM python:3.7
ADD . /code
WORKDIR /code
RUN pipenv install --system --deploy --ignore-pipfile

RUN apt-get update && apt-get install -y ffmpeg

CMD ["python", "manage.py runserver"]