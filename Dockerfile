# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /Portfolio

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile Pipfile.lock /Portfolio/
RUN pipenv install --system

#ADD requirements.txt /Portfolio/
#RUN pip install -r requirements.txt

# Copy project
ADD . /Portfolio/