# Dockerfile

# Pull base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POSTGRES_USER postgres
ENV POSTGRES_PASS postgres
ENV CLOUDINARY_URL cloudinary://739827826451467:yNBblvo0p_1x0BYD0Jotif5q4DY@dkc7uggjy


# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system

RUN apt-get update -y
RUN apt-get -y install apt-utils binutils libproj-dev gdal-bin


# Copy project
COPY . /code/
