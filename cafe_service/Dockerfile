FROM python:3.9-slim-buster

# Create a new directory for the app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required system packages and Python packages
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential wget && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY . .

# Change to the directory where manage.py is located
WORKDIR /app

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ENTRYPOINT ["dockerize", "-wait", "tcp://db:3306", "-timeout", "20s"]

# Run the Django development server on all available network interfaces
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
