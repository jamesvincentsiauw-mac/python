# Use the official Python base image with the desired architecture
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Copy the server code into the container
COPY server.py /app/server.py

# Copy the grading script into the container
COPY client.py /app/client.py

# Install the required dependencies
RUN pip install jsonschema

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["/app/entrypoint.sh"]
