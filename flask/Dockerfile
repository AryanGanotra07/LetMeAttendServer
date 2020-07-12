FROM python:3.8.0

WORKDIR /src

ADD . /src

RUN pip install -r requirements.txt

CMD [ "uwsgi", "app.ini" ]
