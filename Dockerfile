# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11.9-bullseye

ARG OPENAI_API_KEY

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

ENV OPENAI_API_KEY  $OPENAI_API_KEY

# create root directory for our project in the container
RUN mkdir /ingredients-api

# Set the working directory to /music_service
WORKDIR /ingredients-api

# Copy the current directory contents into the container at /music_service
ADD . /ingredients-api/

EXPOSE 8000

RUN python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]