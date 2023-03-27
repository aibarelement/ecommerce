FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get -qqy update && apt-get -qqy install gettext

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN useradd -m -d /proj -s /bin/bash app
COPY . /proj
WORKDIR /proj
RUN chown -R app:app /proj/*
RUN chmod +x /proj/bin/*
ENV PATH "$PATH:/proj/bin"
USER app