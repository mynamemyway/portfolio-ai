# Stage 1: Builder - Install dependencies
FROM python:3.12-slim as builder

# Set environment variables
# Prevents Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures that the python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
# This is done in a separate step to leverage Docker's layer caching.
# The dependencies will only be re-installed if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final - Create the final lightweight image
FROM python:3.12-slim as final

WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy the application code
COPY . .

# Command to run the application
CMD ["python", "main.py"]