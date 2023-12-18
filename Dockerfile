# Use the latest official Python runtime as a base image
FROM python:latest

# Install Git and Python 3 development package
RUN apt-get update && \
    apt-get install -y git python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Remove Git to reduce image size
RUN apt-get remove -y git && \
    apt-get autoremove -y && \
    apt-get clean

# Expose the port on which the Flask app will run
EXPOSE 5000
ENV FLASK_APP=server.py

# Define the command to run your application
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]
