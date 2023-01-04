# Specify parent image from which we build
FROM ubuntu:20.04

# Set the current working directory
WORKDIR /usr/app

# Install python
RUN apt-get update && apt-get install -y python3.9 python3.9-dev

# Copy app files from host to current working directory
COPY . .

# Install dependancies/modules
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

# Run app shell core `run.py`
CMD ["python3.9", "./run.py"]