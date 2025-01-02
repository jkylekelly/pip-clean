# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the target directory into the container
COPY . /app

# Change to the target directory inside the container
WORKDIR /app/target_project

# Install pipenv to manage dependencies
RUN pip install pipenv

# Install dependencies from the Pipfile
RUN pipenv install

# Specify the script to run
CMD ["pipenv", "run", "python", "-c", "from importlib.metadata import packages_distributions; print(packages_distributions())"]
