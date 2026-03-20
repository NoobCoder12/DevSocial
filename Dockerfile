FROM python:3.12-slim
# Use this image as a container base

WORKDIR /app
# Set root dir

COPY requirements.txt .
# COPY <source> <targer>

RUN pip install --no-cache-dir -r requirements.txt
# With --no-cache-dir Docker creates lighter image

COPY . .
# Copy all backend to app

EXPOSE 8000
# Information for Docker on what port listen to

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# 0.0.0.0 - bind on all available interfaces