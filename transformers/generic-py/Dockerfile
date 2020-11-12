FROM python:3.8.5-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir /code
WORKDIR /code
COPY server.py server.py
COPY trans.py trans.py
ENV PYTHONUNBUFFERED True
EXPOSE 80
