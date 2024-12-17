FROM python:3.13

WORKDIR /app

ADD app /app

RUN apt install gcc -y

RUN apt install python3

RUN /usr/local/bin/python -m pip install --upgrade pip

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]