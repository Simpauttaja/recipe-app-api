# Base image we are gonna pull from dockerhub which we are gonna build upon
FROM python:3.9-alpine3.13

# Whoever is gonna be maintaining this image
LABEL maintainer="M.U."

# It tells python you don't want to buffer output, but rather want it to be printed directly
# to the console
ENV PYTHONUNBUFFERED 1

# Copy requirements from our local machine into tmp
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app 
EXPOSE 8000


# Make a virtual image inside docker image. This is useful in case
# the base image will have some conflicting dependencies with my project.
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user