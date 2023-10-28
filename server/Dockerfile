# Use the official Python image with version 3.10.12 as the base image
FROM python:3.10.12

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create and set the working directory
WORKDIR /app

COPY requirements.txt /app/
COPY app.py /app/
COPY circuits/* /app/circuits/

# Install any needed packages specified in requirements.txt
RUN pip install pip -U --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python3", "app.py", "--host", "0.0.0.0", "--port", "8080"]