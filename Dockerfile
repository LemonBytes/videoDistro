# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim as base

user root

RUN  apt-get update \
  && apt-get install -y wget unzip gnupg2 sudo \ 
  && rm -rf /var/lib/apt/lists/*

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
# install chromedriver
RUN apt-get install -yqq unzip
RUN apt-get -y update
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chromedriver-linux64.zip
RUN unzip -o /tmp/\*.zip  -d /usr/local/bin/

RUN apt-get install -y ffmpeg

RUN apt-get -y install cron

# Copy run-script file to the cron.d directory
COPY run-script /etc/cron.d/run-script
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/run-script

# Apply cron job
RUN crontab /etc/cron.d/run-script
 
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1


WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user


# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN  --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt



# Copy the source code into the container.
COPY . .

RUN export PYTHONPATH="$PWD/app"

# Expose the port that the application listens on.
EXPOSE 8000


# Run the command on container startup
CMD ["cron", "-f"]