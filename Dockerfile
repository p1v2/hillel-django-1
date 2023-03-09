FROM python:3.11

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# /app is the working (home) directory of the container
WORKDIR /app

# Run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
