
# Use official Python image
FROM python:3.12.6

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app 

# Copy and install dependencies first (cache optimization)
COPY requirements.txt .  
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose port 8000 (same as Django default)
EXPOSE 8000

# Run Gunicorn instead of Django's runserver
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "blogsphere.wsgi:application"]
