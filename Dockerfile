FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements/* /code/
RUN ls -la
RUN pip install -r requirements_docker.txt
COPY . /code/