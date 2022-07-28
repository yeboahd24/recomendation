FROM python:3.9
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt /requirements.txt
RUN python -m pip install -r /requirements.txt && rm /requirements.txt
ADD . /app
WORKDIR /app
ENV PYTHONPATH=/app