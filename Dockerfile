FROM python:3.4-onbuild

RUN pip install psycopg2-binary

RUN apt-get update && apt-get install netcat -y
