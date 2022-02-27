FROM python:3.8.1

WORKDIR /home/config

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install django-user-agents
RUN pip install python-memcached

# copy project
COPY . .



