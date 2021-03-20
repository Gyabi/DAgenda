FROM python:3.6
ADD . /myapp
WORKDIR /myapp
RUN apt install libpq-dev
RUN pip install -r requirements.txt