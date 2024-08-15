# context is set by docker-compose.yml:
# ./obsfeare-server

FROM python:3.12.5-alpine3.19

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r build/requirements.txt

ENTRYPOINT ["sh", "./build/entrypoint.sh"]
