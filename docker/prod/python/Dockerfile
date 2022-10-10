FROM python:3.7
MAINTAINER ferid.maghraoui@gmail.com
ENV PYTHONUNBUFFERED 1
COPY ./app /app

RUN echo $(python --version)
RUN apt-get update
RUN apt-get -y install xvfb
RUN  apt-get -y install libfontconfig
RUN  apt-get -y install wkhtmltopdf

WORKDIR /app
COPY ./requirements /requirements

RUN pip install -r /requirements/prod.txt

COPY ./docker/prod/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
EXPOSE 8081
ENTRYPOINT ["/entrypoint.sh"]