FROM python:3.9.1
ADD . /python-flask
WORKDIR /python-flask
RUN pip install -e .
RUN export FLASK_APP=flaskr


