# Specify parent image from which we build
FROM ubuntu:20.04

# Set the current working directory
WORKDIR /usr/bluech

# Install system dependancies
#
# Python
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install -y python3.9 python3.9-distutils python3.9-venv libpq-dev && \
    python3.9 -m ensurepip && \
    apt-get install -y postgresql postgresql-contrib

# Copy app files from host to current working directory
COPY . .

# Install requirements
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

# Run tests
CMD ["python3.9", "shell.py"]