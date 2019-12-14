FROM python:3.7-alpine

RUN apk update
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
COPY src/application ./application
COPY src/server.py ./server.py

RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 5000
CMD [ "python", "-u", "server.py" ]