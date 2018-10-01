FROM python:3.6-alpine

# Installing packages
RUN apk update
RUN pip install --no-cache-dir pipenv

RUN adduser -D aktdirekt

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock start.sh ./
COPY akt_direkt_proxy ./akt_direkt_proxy
RUN chown -R aktdirekt:aktdirekt ./

USER aktdirekt

# Install application and dependencies
RUN pipenv install

# Start app
EXPOSE 5000
ENTRYPOINT ["pipenv", "run", "./start.sh"]
